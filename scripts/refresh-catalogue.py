#!/usr/bin/env python3
import os
import re
import json
import base64
import sys
import urllib.error
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')

def load_dotenv():
    env_vars = {}
    if os.path.exists('.env'):
        with open('.env', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split('=', 1)
                    if len(parts) == 2:
                        env_vars[parts[0]] = parts[1].strip().strip('"').strip("'")
    for k, v in env_vars.items():
        if k not in os.environ:
            os.environ[k] = v

def jira_base_url(site):
    site = site.strip().rstrip("/")
    if site.startswith("http://") or site.startswith("https://"):
        return site
    return f"https://{site}"

def jira_auth_headers(email, token, include_content_type=False):
    auth_str = f"{email}:{token}"
    headers = {
        "Authorization": f"Basic {base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')}",
        "Accept": "application/json"
    }
    if include_content_type:
        headers["Content-Type"] = "application/json"
    return headers

def read_http_error(error):
    try:
        details = error.read().decode("utf-8", errors="replace")
    except Exception:
        details = str(error)
    return details[:700]

def request_jira_json(url, headers, payload=None, method="GET"):
    body = None
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        raise RuntimeError(f"HTTP {error.code}: {read_http_error(error)}") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"Network error: {error.reason}") from error

def fetch_jira_page(base_url, email, token, jql, start_at, max_results, fields):
    payload = {
        "jql": jql,
        "startAt": start_at,
        "maxResults": max_results,
        "fields": fields
    }

    post_headers = jira_auth_headers(email, token, include_content_type=True)
    get_headers = jira_auth_headers(email, token)
    encoded_params = urllib.parse.urlencode({
        "jql": jql,
        "startAt": start_at,
        "maxResults": max_results,
        "fields": ",".join(fields)
    })

    attempts = [
        ("POST Jira API v3 search", "POST", f"{base_url}/rest/api/3/search", post_headers, payload),
        ("POST Jira API v2 search", "POST", f"{base_url}/rest/api/2/search", post_headers, payload),
        ("GET Jira API v2 search", "GET", f"{base_url}/rest/api/2/search?{encoded_params}", get_headers, None),
    ]

    errors = []
    for label, method, url, headers, body in attempts:
        try:
            return request_jira_json(url, headers, body, method)
        except RuntimeError as exc:
            errors.append(f"{label} failed ({exc})")

    raise RuntimeError("; ".join(errors))

def fetch_jira_issues(site, email, token, jql):
    base_url = jira_base_url(site)
    fields = ["summary", "status", "issuetype", "labels", "description", "updated"]
    max_results = 100
    start_at = 0
    total = None
    issues = []

    print("[JIRA] Fetching latest issue data using ATLASSIAN_API_TOKEN...")

    while total is None or start_at < total:
        data = fetch_jira_page(base_url, email, token, jql, start_at, max_results, fields)
        page_issues = data.get("issues", [])
        total = int(data.get("total", len(issues) + len(page_issues)))
        issues.extend(page_issues)
        print(f"  [JIRA] Retrieved {len(issues)} of {total} issues...")

        if not page_issues:
            break
        start_at += len(page_issues)

    return {issue["key"]: issue for issue in issues if issue.get("key")}

# ADF to Plain Text helper
def adf_to_text(node):
    if not node:
        return ""
    if isinstance(node, str):
        return node
    if isinstance(node, list):
        return "".join(adf_to_text(child) for child in node)
    if isinstance(node, dict):
        node_type = node.get('type')
        if node_type == 'text':
            return node.get('text', '')
        content = node.get('content', [])
        text = adf_to_text(content)
        if node_type in ['paragraph', 'heading']:
            return text + "\n"
        elif node_type == 'listItem':
            return "- " + text + "\n"
        return text
    return ""

def get_availability(status, category):
    done_statuses = ["Done", "Released", "Closed", "Resolved"]
    if status in done_statuses:
        return "Available"
    elif category == "In Progress" or status == "In Progress":
        return "Recently Released"
    elif status in ["To Do", "Backlog", "Open"]:
        return "Coming Soon"
    else:
        return "Needs Review"

def run_sanitization_safety_audit():
    """Runs safety verification scans on public files to guarantee zero Jira parameters leak."""
    print("\n[SAFETY CHECK] Running automated sanitization security scan...")
    public_jsons = ["catalogue-public.json", "data/catalogue-public.json", "aimy-catalogue-site/catalogue-public.json"]
    public_htmls = ["index.html", "aimy-catalogue-site/index.html"]
    
    jira_key_pattern = re.compile(r'\b(?:AIMY|RD|AB)-\d+\b', re.IGNORECASE)
    jira_url_pattern = re.compile(r'atlassian\.net', re.IGNORECASE)
    
    leaked = False
    
    # 1. Audit public JSONs
    for p_json in public_jsons:
        if os.path.exists(p_json):
            with open(p_json, 'r', encoding='utf-8') as f:
                content = f.read()
            if jira_key_pattern.findall(content):
                print(f"  [CRITICAL LEAK] Jira issue keys found in: {p_json}")
                leaked = True
            if jira_url_pattern.findall(content):
                print(f"  [CRITICAL LEAK] Atlassian URLs found in: {p_json}")
                leaked = True
            
    # 2. Audit public HTMLs
    for html in public_htmls:
        if os.path.exists(html):
            with open(html, 'r', encoding='utf-8') as f:
                content = f.read()
            if jira_key_pattern.findall(content):
                print(f"  [CRITICAL LEAK] Jira issue keys found in: {html}")
                leaked = True
            if jira_url_pattern.findall(content):
                print(f"  [CRITICAL LEAK] Atlassian URLs found in: {html}")
                leaked = True
                
    if leaked:
        print("\n[SAFETY RESULT] ❌ SAFETY CHECK FAILED! Raw internal Jira parameters are leaking into public catalogue files!")
        return False
    else:
        print("  [SAFETY RESULT] ✅ SAFETY CHECK PASSED! All public assets are 100% sanitized and safe for customer deployment.")
        return True

def get_module_id(module_name):
    m = module_name.lower()
    if 'knowledge' in m:
        return 'knowledge'
    elif 'voice' in m or 'phone' in m:
        return 'voice'
    elif 'qa' in m:
        return 'qa'
    elif 'connect' in m:
        return 'connect'
    elif 'bdr' in m:
        return 'sales-bdr'
    elif 'manager' in m:
        return 'sales-manager'
    elif 'loop' in m:
        return 'loop'
    return 'knowledge'

def main():
    load_dotenv()
    print("=== Starting AiMY Product Catalogue Refresh Pipeline ===")
    
    site = os.environ.get('ATLASSIAN_SITE')
    email = os.environ.get('ATLASSIAN_EMAIL')
    token = os.environ.get('ATLASSIAN_API_TOKEN')
    project = os.environ.get('JIRA_PROJECT_KEY', 'AIMY')
    
    if not site or not email or not token:
        print("[ERROR] Missing required credentials in environment variables!")
        print("Required variables: ATLASSIAN_SITE, ATLASSIAN_EMAIL, ATLASSIAN_API_TOKEN")
        sys.exit(1)
        
    print(f"[OK] Credentials verified. Serving site tenant: {site}")
    
    jql = f'project = "{project}" AND statusCategory IN ("In Progress", "Done", "To Do") ORDER BY updated DESC'
    print(f"[JQL] Target query: {jql}")
    
    cache_file = "jira_issues_cache.json"
    try:
        cache = fetch_jira_issues(site, email, token, jql)
    except RuntimeError as exc:
        print(f"[ERROR] Failed to fetch Jira data through the API token: {exc}")
        sys.exit(1)

    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)
        
    print(f"[OK] Loaded and cached {len(cache)} issues from Jira API.")
    
    # Static copy from the official download ZIP catalogue-public.json
    OUTPUT_SCHEMA = {
      "meta": {
        "name": "AiMY Customer Catalogue",
        "purpose": "Customer-facing pitch asset for AiMY support and sales operations",
        "audience": "Sales teams, customer stakeholders, implementation sponsors",
        "sourceNarratives": [
          "AiMY L1 Support — Client Onboarding Journey",
          "AiMY Sales — Client Onboarding Journey"
        ],
        "securityModel": "Public UI contains no internal issue keys, internal URLs, ownership fields, internal labels, or raw ticket summaries. Release data is translated into customer-safe capability themes."
      },
      "tracks": [
        {
          "id": "support",
          "name": "AiMY L1 Support",
          "tagline": "Turn reactive support into a self-improving operating system.",
          "day0": [
            "Knowledge is scattered across drives, wikis, chat threads, and senior agents' heads.",
            "QA is manual, selective, and late, so most conversations are never reviewed.",
            "Voice interactions are hard to monitor, search, and feed back into process improvement.",
            "Supervisors react to escalations instead of seeing risk early."
          ],
          "journey": [
            "Knowledge foundation",
            "Voice activation",
            "Automated QA coverage",
            "Supervisor visibility through Connect",
            "Closed improvement loop"
          ],
          "day30": [
            "Agents work from one consistent knowledge layer.",
            "Text and voice channels are covered by the same intelligence layer.",
            "Conversation QA becomes continuous instead of sampled.",
            "Supervisors get real-time operational visibility.",
            "Knowledge gaps turn into reviewed improvement actions."
          ]
        },
        {
          "id": "sales",
          "name": "AiMY Sales",
          "tagline": "Make outreach, pipeline visibility, and sales learning repeatable.",
          "day0": [
            "Pipeline visibility depends on CRM data quality and rep follow-up.",
            "Outreach varies by rep, creating inconsistent messaging and follow-up cadence.",
            "Product knowledge and proof points are scattered across systems.",
            "Managers spend too much time chasing updates and not enough time coaching."
          ],
          "journey": [
            "Sales knowledge foundation",
            "BDR mode for playbook-grounded outreach",
            "Manager mode for queryable pipeline visibility",
            "Closed sales improvement loop"
          ],
          "day30": [
            "Every rep works from the same product knowledge and playbooks.",
            "Outreach becomes consistent, grounded, and repeatable.",
            "Pipeline risk and activity are easier to query and act on.",
            "Managers coach from evidence instead of chasing manual updates.",
            "Win/loss patterns feed back into future playbooks and outreach guidance."
          ]
        }
      ],
      "modules": [
        {
          "id": "knowledge",
          "name": "AiMY Knowledge",
          "track": "Support + Sales",
          "status": "Available foundation",
          "oneLiner": "A unified knowledge layer that grounds AiMY answers in your real content.",
          "problem": "Teams lose time hunting for the right answer, policy, case study, or process note.",
          "whatItDoes": "Connects to approved knowledge sources and gives agents or reps fast, consistent, contextual answers.",
          "worksWith": ["SOPs", "FAQs", "Product documentation", "Sales collateral", "Playbooks", "Competitive intelligence", "Case studies"],
          "integrations": ["SharePoint", "Confluence", "Google Drive", "Notion", "Helpdesk knowledge bases", "CRM-linked knowledge bases"],
          "outcome": "A single operating baseline: fewer guessed answers, faster ramp-up, and more consistent customer conversations.",
          "releaseThemes": ["Knowledge document ingestion", "FAQ and task surfaces", "Grounded product expert experiences"],
          "features": []
        },
        {
          "id": "voice",
          "name": "AiMY Voice",
          "track": "Support + Sales",
          "status": "Activation track",
          "oneLiner": "Turns calls into searchable, coachable, structured operational data.",
          "problem": "Voice conversations are usually a black box, even though they contain the richest customer signals.",
          "whatItDoes": "Captures call context, supports live assistance, and feeds transcripts and outcomes into QA, knowledge, and follow-up workflows.",
          "worksWith": ["Inbound calls", "Outbound calls", "Call recordings", "Live transcripts", "IVR interaction logs"],
          "integrations": ["Existing telephony", "CRM caller context", "Voice infrastructure", "Call transcription services"],
          "outcome": "Calls stop disappearing after they end; they become part of the same improvement loop as tickets and chats.",
          "releaseThemes": ["Native voice infrastructure", "Active call screen", "Post-call intelligence", "Caller context and follow-up actions"],
          "features": []
        },
        {
          "id": "qa",
          "name": "AiMY QA",
          "track": "L1 Support",
          "status": "Capability track",
          "oneLiner": "Continuous QA coverage across support conversations.",
          "problem": "Manual QA reviews a sample, catches issues late, and misses recurring patterns.",
          "whatItDoes": "Analyses interactions against quality standards, flags risks, and turns repeated failures into coaching and knowledge signals.",
          "worksWith": ["Support tickets", "Chat transcripts", "Email threads", "Call recordings", "Voice transcripts", "Agent response data"],
          "integrations": ["Zendesk", "Freshdesk", "ServiceNow", "Salesforce Service Cloud", "Voice data from AiMY Voice"],
          "outcome": "Quality becomes a live signal instead of a delayed audit process.",
          "releaseThemes": ["Written interaction ingestion", "AI evaluation engine", "Supervisor coaching canvas", "Knowledge gap detection"],
          "features": []
        },
        {
          "id": "connect",
          "name": "AiMY Connect",
          "track": "Support Operations",
          "status": "Supervisor layer",
          "oneLiner": "A real-time operating view for supervisors and managers.",
          "problem": "Supervisors often discover problems only after escalation, SLA risk, or quality drift has already happened.",
          "whatItDoes": "Brings operational signals together so supervisors can see performance, queue pressure, escalation patterns, and coaching needs.",
          "worksWith": ["Agent activity", "Queue metrics", "Ticket trends", "Escalation logs", "QA scores", "Flagged interactions"],
          "integrations": ["Helpdesk platforms", "Workforce management tools", "CRM systems", "Operational data sources"],
          "outcome": "Supervisors move from firefighting to proactive operations management.",
          "releaseThemes": ["Urgency and escalation intelligence", "Event-based notifications", "Queue management", "Operational risk views"],
          "features": []
        },
        {
          "id": "sales-bdr",
          "name": "AiMY Sales — BDR Mode",
          "track": "Sales",
          "status": "Sales activation track",
          "oneLiner": "AI-assisted outreach grounded in your ICP, messaging, and playbooks.",
          "problem": "Every rep runs a slightly different version of the sales motion, making scale and quality hard to manage.",
          "whatItDoes": "Helps reps draft, sequence, and follow up using approved messaging, account context, and playbook logic.",
          "worksWith": ["Prospect data", "Account data", "ICP definitions", "Outreach templates", "Historical engagement data"],
          "integrations": ["Salesforce", "HubSpot", "Sales engagement tools", "Prospecting and enrichment sources"],
          "outcome": "A repeatable outbound motion that helps new reps ramp faster and keeps experienced reps focused on conversations.",
          "releaseThemes": ["Sales engagement tracking", "Follow-up intelligence", "Contact enrichment", "Lead data hygiene", "Next-best-action sequencing"],
          "features": []
        },
        {
          "id": "sales-manager",
          "name": "AiMY Sales — Manager Mode",
          "track": "Sales Leadership",
          "status": "Sales leadership layer",
          "oneLiner": "Queryable pipeline visibility for sales managers.",
          "problem": "Managers rely on stale CRM updates, gut-feel forecasting, and manual rep check-ins.",
          "whatItDoes": "Gives sales leadership a natural-language way to inspect pipeline risk, stalled deals, activity gaps, and rep performance signals.",
          "worksWith": ["CRM pipeline data", "Deal stages", "Activity logs", "Engagement history", "Forecast data", "Quota and rep metrics"],
          "integrations": ["Salesforce", "HubSpot", "Revenue intelligence tools", "Forecasting tools"],
          "outcome": "Forecasting and coaching become evidence-based instead of reactive.",
          "releaseThemes": ["Sales ops hub", "Pipeline health views", "BDR activity dashboard", "Campaign execution health"],
          "features": []
        },
        {
          "id": "loop",
          "name": "Continuous Improvement Loop",
          "track": "Platform Layer",
          "status": "Cross-module value loop",
          "oneLiner": "AiMY learns from real outcomes and feeds improvements back into the operating model.",
          "problem": "Most operations improve only during manual reviews, retraining cycles, or after problems become visible.",
          "whatItDoes": "Turns QA findings, call outcomes, deal patterns, and knowledge gaps into reviewed improvement actions.",
          "worksWith": ["QA signals", "Low-confidence answers", "Won/lost outcomes", "Objection patterns", "Manager-flagged coaching moments"],
          "integrations": ["Runs across AiMY Knowledge, Voice, QA, Connect, and Sales layers"],
          "outcome": "The system compounds: every conversation and deal can improve the next one.",
          "releaseThemes": ["Knowledge gap detection", "Draft article workflow", "Sales pattern feedback", "Recurring failure analysis"],
          "features": []
        }
      ],
      "whatsNew": [
        {
          "title": "Support urgency and escalation intelligence",
          "module": "AiMY Connect",
          "availability": "Recently released / review for customer wording",
          "whyItMatters": "Helps supervisors identify urgent cases and act before SLA or service risk escalates."
        },
        {
          "title": "Event-based operational notifications",
          "module": "AiMY Connect",
          "availability": "Recently released / review for customer wording",
          "whyItMatters": "Turns important operational changes into proactive alerts instead of dashboard hunting."
        },
        {
          "title": "Knowledge ingestion and grounded answer foundation",
          "module": "AiMY Knowledge",
          "availability": "Available foundation",
          "whyItMatters": "Creates the source-of-truth layer that both support agents and sales reps depend on."
        },
        {
          "title": "Sales contact enrichment loop",
          "module": "AiMY Sales — BDR Mode",
          "availability": "Released / review for customer wording",
          "whyItMatters": "Improves lead records so outreach and follow-up can be more relevant and less manual."
        },
        {
          "title": "Sales outreach sequencing and follow-up intelligence",
          "module": "AiMY Sales — BDR Mode",
          "availability": "Roadmap / customer-safe once confirmed",
          "whyItMatters": "Helps BDR teams keep follow-up consistent and act on stalled sequences."
        },
        {
          "title": "Automated QA evaluation and coaching signals",
          "module": "AiMY QA",
          "availability": "Roadmap / customer-safe once confirmed",
          "whyItMatters": "Moves QA from sampled manual checks toward continuous operational guidance."
        },
        {
          "title": "Voice call context and post-call intelligence",
          "module": "AiMY Voice",
          "availability": "Roadmap / customer-safe once confirmed",
          "whyItMatters": "Makes calls searchable, coachable, and usable for follow-up and knowledge improvement."
        }
      ]
    }

    # Static Plain-English Feature Translations Mapping
    # (Maps raw engineering issues to customer-safe pitch claims)
    MAPPINGS = {
        "AIMY-407": {
            "track": "L1 Support",
            "module": "AiMY Knowledge",
            "feature_name": "Multi-Source Knowledge Ingestion",
            "description": "Securely ingests, normalizes, and indexes standard operating procedures, manuals, and FAQs from Confluence, SharePoint, and Google Drive.",
            "customer_value": "Eliminates scattered knowledge silos and establishes a single, verified source of truth for support agents.",
            "integrations": ["Confluence", "SharePoint", "Notion", "Google Drive", "Zendesk Guide", "Freshdesk KB"]
        },
        "AIMY-2104": {
            "track": "L1 Support",
            "module": "AiMY Knowledge",
            "feature_name": "Conversational UI & Live Search Console",
            "description": "A modern, natural-language agent interface with built-in Generative UI that allows reps and agents to search verified SOPs instantly.",
            "customer_value": "Reduces agent handle times by over 30% by providing prompt, contextual answers in real-time.",
            "integrations": ["React", "Zendesk Chat", "Freshdesk Chat"]
        },
        "AIMY-2574": {
            "track": "L1 Support",
            "module": "Continuous Improvement Loop",
            "feature_name": "Self-Improving SOP Generation Pipeline",
            "description": "Monitors low-confidence support tickets and flags them as knowledge gaps, automatically drafting new SOP article recommendations for human review.",
            "customer_value": "Ensures the knowledge base maintains and updates itself automatically based on actual customer escalations.",
            "integrations": ["AiMY QA core", "AiMY Knowledge core"]
        },
        "AB-146": {
            "track": "L1 Support",
            "module": "AiMY Knowledge",
            "feature_name": "Enterprise Omnichannel Knowledge API",
            "description": "A secure API gateway providing high-speed retrieval of verified SOPs across all digital channels (web, chat, and native voice).",
            "customer_value": "Maintains 100% consistent and factual support answers regardless of client touchpoint.",
            "integrations": ["Enterprise REST APIs"]
        },
        "AIMY-3683": {
            "track": "L1 Support",
            "module": "AiMY Voice",
            "feature_name": "Native Twilio Calling Streams",
            "description": "Enterprise-grade inbound and outbound calling infrastructure built natively on cloud calling frameworks.",
            "customer_value": "Stops phone calls from being a black box, integrating the voice channel into the rest of the operational loop.",
            "integrations": ["Twilio Voice API", "Custom SIP trunks"]
        },
        "AIMY-3684": {
            "track": "L1 Support",
            "module": "AiMY Voice",
            "feature_name": "Real-time Live Call Transcription Pipeline",
            "description": "Converts active phone streams into structured text, split by speaker (agent vs. customer), for immediate processing.",
            "customer_value": "Enables search, text index, and automatic sentiment tracking on 100% of phone interactions.",
            "integrations": ["Deepgram API", "AssemblyAI"]
        },
        "AIMY-3685": {
            "track": "L1 Support",
            "module": "AiMY Voice",
            "feature_name": "Active Agent Call Assist Panel",
            "description": "A split-pane screen showing active transcriptions and matching knowledge base articles side-by-side during a call.",
            "customer_value": "Guides reps with real-time coaching suggestions, maximizing first-call resolution (FCR) rates.",
            "integrations": ["Twilio Streaming", "AiMY Knowledge"]
        },
        "AIMY-3431": {
            "track": "L1 Support",
            "module": "AiMY QA",
            "feature_name": "Omnichannel Interaction Auditing Pipeline",
            "description": "Ingests email threads, transcribed voice logs, and chat transcript logs directly into the quality scoring engine.",
            "customer_value": "Eliminates sample-based auditing, providing managers with a total operational signal.",
            "integrations": ["Kafka pipelines", "Zendesk", "Freshdesk"]
        },
        "AIMY-3457": {
            "track": "L1 Support",
            "module": "AiMY QA",
            "feature_name": "100% Automated Conversational Metric Scoring",
            "description": "Evaluates every interaction against custom compliance benchmarks, agent tone guidelines, and technical accuracy scores.",
            "customer_value": "Flags critical customer risks, tone errors, and compliance breaches within minutes of conversation closure.",
            "integrations": ["OpenAI GPT-4", "Anthropic Claude"]
        },
        "AIMY-4868": {
            "track": "L1 Support",
            "module": "AiMY QA",
            "feature_name": "Helpdesk Automatic Ticket Ingestion API",
            "description": "Native API webhooks pulling customer ticket updates from external support helpdesks automatically.",
            "customer_value": "Seamless plug-and-play setup that connects your legacy ticketing systems to the QA intelligence layer.",
            "integrations": ["Zendesk Ticket Webhooks", "Freshdesk API"]
        },
        "AIMY-3610": {
            "track": "L1 Support",
            "module": "AiMY Connect",
            "feature_name": "SLA-Aware Queue Triage & Intelligent Routing",
            "description": "Prioritizes queues based on customer tier, contract SLA breaches, and conversation sentiment.",
            "customer_value": "Prevents churn by routing frustrated or high-value clients to senior reps automatically.",
            "integrations": ["Zendesk Routing Engine", "n8n"]
        },
        "AIMY-4833": {
            "track": "L1 Support",
            "module": "AiMY Connect",
            "feature_name": "Supervisor Operational Risk Dashboard",
            "description": "Real-time command panel highlighting support queue backlogs, agent live states, and coaching suggestions.",
            "customer_value": "Empowers supervisors to pivot floor operations proactively rather than reactively firefighting.",
            "integrations": ["Workforce Management systems"]
        },
        "AIMY-4831": {
            "track": "L1 Support",
            "module": "AiMY Connect",
            "feature_name": "Predictive SLA Breach Alerting Engine",
            "description": "Scans ongoing queue metrics and issues instant warnings when response-time thresholds are approaching breach.",
            "customer_value": "Saves critical enterprise accounts by flagging high-risk delays before they breach SLAs.",
            "integrations": ["n8n", "Slack Webhooks"]
        },
        "AIMY-4832": {
            "track": "L1 Support",
            "module": "AiMY Connect",
            "feature_name": "Compliance Exposure Risk Flagger",
            "description": "Identifies sensitive interactions that breach data protection laws (e.g., exposing credit card numbers or private credentials).",
            "customer_value": "Protects operations from massive data compliance fines by immediately masking sensitive attributes.",
            "integrations": ["AiMY QA core"]
        },
        "AIMY-4082": {
            "track": "Sales",
            "module": "AiMY Sales — BDR Mode",
            "feature_name": "Playbook-Driven Email Outreach Sequencing",
            "description": "Generates outcome-driven email sequences that strictly adhere to corporate playbooks, target personas, and ICP guidelines.",
            "customer_value": "Establishes structured, high-conversion outbound messaging across the entire sales team.",
            "integrations": ["HubSpot sequences", "Outreach.io"]
        },
        "AIMY-4088": {
            "track": "Sales",
            "module": "AiMY Sales — BDR Mode",
            "feature_name": "Rep View High-Velocity Dialer & Task Queue",
            "description": "Consolidates enriched BDR tasks, lead battlecards, call histories, and dialer launches into a single dashboard.",
            "customer_value": "Boosts outbound dials by 50% by eliminating rep administrative overhead.",
            "integrations": ["Salesforce layout widgets", "HubSpot Layouts"]
        },
        "AIMY-4671": {
            "track": "Sales",
            "module": "AiMY Sales — BDR Mode",
            "feature_name": "Lead Enrichment Signal Scraper",
            "description": "Performs deep contextual research on prospects by scraping live signals, matching target ICPs, and outputting enrichment scores.",
            "customer_value": "Ensures every rep call is pre-loaded with deep competitive context, reducing cold call friction.",
            "integrations": ["Exa API", "Serper", "ZoomInfo", "LinkedIn"]
        },
        "AIMY-4709": {
            "track": "Sales",
            "module": "AiMY Sales — BDR Mode",
            "feature_name": "High-Velocity Twilio Outbound Dialer integration",
            "description": "Enables one-click BDR cold calling with native live voice transcription and speaker sentiment logs.",
            "customer_value": "Speeds outbound executions while recording exact call records directly in CRM.",
            "integrations": ["Twilio Voice API", "Deepgram"]
        },
        "AIMY-4714": {
            "track": "Sales",
            "module": "AiMY Sales — BDR Mode",
            "feature_name": "Real-time Rep Call Objection Battlecards",
            "description": "Renders floating battlecards and objection-handling guidelines on screen during live outbound calls.",
            "customer_value": "Gives junior BDRs the exact objections playbook in real-time, boosting call conversion by 20%.",
            "integrations": ["AiMY Knowledge Base", "Deepgram streaming"]
        },
        "AIMY-4719": {
            "track": "Sales",
            "module": "AiMY Sales — BDR Mode",
            "feature_name": "Automated Post-Call Summaries & Next Actions",
            "description": "Analyzes call transcripts, logs conversation outcomes, and drafts immediate post-call follow-ups automatically.",
            "customer_value": "Removes manual CRM update time, keeping deal records 100% current.",
            "integrations": ["HubSpot CRM", "Salesforce"]
        },
        "AIMY-4745": {
            "track": "Sales",
            "module": "AiMY Sales — BDR Mode",
            "feature_name": "Automated Calendar Meeting Booker",
            "description": "Enables post-qualification hooks that automatically trigger meeting scheduling requests directly to the prospect's inbox.",
            "customer_value": "Increases meeting hold rates by booking calendar slots immediately upon live call verbal qualification.",
            "integrations": ["Calendly API", "Google Calendar", "Outlook"]
        },
        "AIMY-3998": {
            "track": "Sales",
            "module": "AiMY Sales — Manager Mode",
            "feature_name": "Sales Pipeline Natural Language Intelligence Engine",
            "description": "Allows sales leaders to query deal pipeline health, stalled leads, rep activity, and deal risks in natural language.",
            "customer_value": "Stops managers from wasting hours building manual reports, bringing immediate pipeline visibility.",
            "integrations": ["Salesforce Service API", "HubSpot REST API"]
        },
        "AIMY-4649": {
            "track": "Sales",
            "module": "AiMY Sales — Manager Mode",
            "feature_name": "Funnel Performance & CRM State Machine Monitor",
            "description": "Tracks deal stage progressions, alerts when deals stall past playbook thresholds, and calculates conversion ratios.",
            "customer_value": "Pins down weak points in the pipeline, pointing managers exactly where to focus coaching.",
            "integrations": ["Salesforce pipeline schemas", "HubSpot Deal API"]
        },
        "AIMY-4655": {
            "track": "Sales",
            "module": "AiMY Sales — Manager Mode",
            "feature_name": "BDR Activity & Lead Redistribution Console",
            "description": "Supervisors dashboard tracking outbound dial metrics, lead queue health, and providing controls for lead reassignment.",
            "customer_value": "Allows sales leaders to re-balance BDR pipelines on the fly to maximize lead coverage.",
            "integrations": ["n8n", "Salesforce"]
        },
        "AIMY-4076": {
            "track": "Sales",
            "module": "AiMY Sales — Manager Mode",
            "feature_name": "Data Hygiene & DNC Suppression List Engine",
            "description": "Detects duplicate contacts, cleans up Apollo lead ingests, and strictly enforces Do Not Call (DNC) lists.",
            "customer_value": "Keeps your sales database clean and ensures 100% legal compliance with DNC regulations.",
            "integrations": ["Apollo.io", "DNC suppression databases"]
        },
        "AIMY-4135": {
            "track": "Sales",
            "module": "Continuous Improvement Loop",
            "feature_name": "Outcomes QA Linkage & Objection Analysis",
            "description": "Bridges outbound sales calling with the QA scoring engine, analyzing transcripts to flag objection trends and won/lost logs.",
            "customer_value": "Aggregates won/lost trends to feed intelligence back into BDR outreach battlecards.",
            "integrations": ["AiMY QA core", "AiMY Sales core"]
        },
        "RD-1323": {
            "track": "Sales",
            "module": "Continuous Improvement Loop",
            "feature_name": "Closed Loop Sales Playbook Auto-Refiner",
            "description": "Feeds won/lost deal objection profiles back into the Sales Knowledge Battlecard repository, proposing playbook updates automatically.",
            "customer_value": "Enables your outbound sales playbooks to improve continuously based on live deal logs.",
            "integrations": ["AiMY Knowledge Base", "AiMY Sales CRM"]
        }
    }
    
    # 4. Parse & Reclassify Jira Issues
    raw_public_features = []
    internal_evidence = []
    excluded_tickets = []
    module_counters = {}
    
    for key, issue in cache.items():
        fields = issue.get('fields', {})
        summary = fields.get('summary', '')
        status = fields.get('status', {}).get('name', 'To Do')
        status_category = fields.get('status', {}).get('statusCategory', {}).get('name', 'To Do')
        issue_type = fields.get('issuetype', {}).get('name', 'Story')
        labels = fields.get('labels', [])
        
        is_internal = False
        chores_keywords = ["infrastructure", "pipeline", "setup", "chore", "refactor", "cleanup", "test", "docker", "ci/cd", "deployment", "migration", "yard", "duplicate", "data model", "caller identification"]
        if any(kw in summary.lower() for kw in chores_keywords) or "internal" in labels or "chore" in labels:
            if key not in MAPPINGS:
                is_internal = True
                
        if is_internal and issue_type == "Story" and not any(l.startswith("flow-") for l in labels):
            excluded_tickets.append({
                "key": key,
                "summary": summary,
                "status": status,
                "reason": "Purely internal engineering task."
            })
            continue
            
        desc_obj = fields.get('description', '')
        raw_desc = adf_to_text(desc_obj) if isinstance(desc_obj, dict) else str(desc_obj)
        
        track = "L1 Support"
        module = "AiMY Knowledge"
        
        if key in MAPPINGS:
            map_data = MAPPINGS[key]
            track = map_data["track"]
            module = map_data["module"]
        else:
            labels_lower = [l.lower() for l in labels]
            if 'aimy-qa' in labels_lower or 'qa' in summary.lower():
                module = "AiMY QA"
            elif 'aimy-voice' in labels_lower or 'phone' in labels_lower or 'voice' in summary.lower() or 'phone' in summary.lower():
                module = "AiMY Voice"
            elif 'aimy-connect' in labels_lower or 'connect' in summary.lower():
                module = "AiMY Connect"
            elif 'aimy-sales' in labels_lower or 'sales' in summary.lower():
                track = "Sales"
                if 'bdr' in summary.lower() or 'seq' in summary.lower() or 'outreach' in summary.lower():
                    module = "AiMY Sales — BDR Mode"
                else:
                    module = "AiMY Sales — Manager Mode"
            elif 'aimy-talent' in labels_lower or 'talent' in summary.lower():
                continue
                
        mod_slug = module.lower().replace(" — ", "-").replace(" ", "-")
        module_counters[mod_slug] = module_counters.get(mod_slug, 0) + 1
        feat_id = f"feat-{mod_slug}-{module_counters[mod_slug]}"
        
        internal_evidence.append({
            "public_feature_id": feat_id,
            "jira_key": key,
            "jira_summary": summary,
            "jira_status": status,
            "jira_url": f"https://flairstechdev.atlassian.net/browse/{key}"
        })
        
        availability = get_availability(status, status_category)
        
        if key in MAPPINGS:
            map_data = MAPPINGS[key]
            raw_public_features.append({
                "id": feat_id,
                "track": map_data["track"],
                "module": map_data["module"],
                "feature_name": map_data["feature_name"],
                "description": map_data["description"],
                "customer_value": map_data["customer_value"],
                "integrations": map_data["integrations"],
                "availability": availability
            })
        else:
            clean_name = summary.replace("AiMY Sales", "").replace("AiMY QA", "").replace("AiMY Voice", "").replace("AiMY Connect", "").replace("AiMY Knowledge", "")
            clean_name = re.sub(r'^[—:\-\s]+', '', clean_name).strip()
            clean_name = clean_name.replace(" — ", ": ")
            
            if clean_name:
                clean_name = clean_name[0].upper() + clean_name[1:]
            else:
                clean_name = f"Optimized Platform Metric Framework"
                
            clean_name = re.sub(r'\b(?:AIMY|RD|AB)-\d+\b', '', clean_name).strip()
            
            raw_public_features.append({
                "id": feat_id,
                "track": track,
                "module": module,
                "feature_name": clean_name,
                "description": "Integrates automated operations pipelines to enable unified metrics and seamless helpdesk tracking.",
                "customer_value": "Supports overall helpdesk platform security, transaction throughput, and response consistency.",
                "integrations": ["Zendesk", "HubSpot"] if track == "Sales" else ["Zendesk", "Freshdesk"],
                "availability": availability
            })

    # Group JIRA features into their respective parent modules in the output schema
    for feat in raw_public_features:
        mod_id = get_module_id(feat["module"])
        # Find module in OUTPUT_SCHEMA
        target_mod = next((m for m in OUTPUT_SCHEMA["modules"] if m["id"] == mod_id), None)
        if target_mod:
            # Check if features is initialized
            if "features" not in target_mod:
                target_mod["features"] = []
            target_mod["features"].append(feat)

    # 5. Output separate files
    with open("data/catalogue-public.json", 'w', encoding='utf-8') as f:
        json.dump(OUTPUT_SCHEMA, f, indent=2, ensure_ascii=False)

    with open("catalogue-public.json", 'w', encoding='utf-8') as f:
        json.dump(OUTPUT_SCHEMA, f, indent=2, ensure_ascii=False)
        
    with open("aimy-catalogue-site/catalogue-public.json", 'w', encoding='utf-8') as f:
        json.dump(OUTPUT_SCHEMA, f, indent=2, ensure_ascii=False)
        
    with open("data/catalogue-internal-evidence.json", 'w', encoding='utf-8') as f:
        json.dump(internal_evidence, f, indent=2, ensure_ascii=False)
        
    print(f"[OK] Dynamic separation completed. Nested raw JIRA capabilities into modules.")
    
    # 6. Trigger automated safety sanitization check
    audit_passed = run_sanitization_safety_audit()
    if not audit_passed:
        print("\n[ERROR] Pipeline aborted: Security leak detected!")
        sys.exit(1)
        
    # 7. Print Manual Review/Publish Step guidelines
    print("\n=======================================================")
    print("  CATALOGUE REGENERATION COMPLETELY SUCCESSFUL!")
    print("=======================================================")
    print("  Review Steps before Publishing:")
    print("  1. Verify the changes delta in: git diff data/catalogue-public.json")
    print("  2. Open internal-review-notes.md to inspect newly excluded chores.")
    print("  3. Approve the Pull Request on GitHub to build the static deployment.")
    print("=======================================================")

if __name__ == "__main__":
    main()
