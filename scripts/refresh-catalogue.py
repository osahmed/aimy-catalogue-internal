#!/usr/bin/env python3
"""
AiMY Catalogue refresh pipeline.

Jira is the internal source of truth (evidence). The website is the pitch.
This script:
  1. Fetches AiMY Jira issues using secure environment variables.
  2. Binds a hand-curated, customer-safe catalogue (scripts/catalogue_map.py)
     to live Jira issues by matching epic/story titles.
  3. Resolves a display date per item (fixVersion -> resolution -> updated).
  4. Writes three files:
       - data/catalogue-public.json          (customer-safe, deployed)
       - data/catalogue-internal-evidence.json (private traceability)
       - data/catalogue-review-needed.json     (private, human triage queue)
  5. Runs a real safety check that FAILS on any internal Jira leak.
  6. Regenerates internal-review-notes.md and prints a summary.

It NEVER publishes raw Jira data. Anything not in the curated map is routed to
the private evidence/review files only.
"""
import os
import re
import sys
import json
import base64
import urllib.error
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')

# Import the curated catalogue. The script may run from repo root or scripts/.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalogue_map import CURATED_FEATURES, MODULE_IDS  # noqa: E402

MONTHS = ["", "January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]


# ─────────────────────────────── env / http ──────────────────────────────
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


def fetch_jira_page(base_url, email, token, jql, max_results, fields, next_page_token=None):
    payload = {
        "jql": jql,
        "maxResults": max_results,
        "fields": fields,
        "fieldsByKeys": True
    }
    if next_page_token:
        payload["nextPageToken"] = next_page_token
    headers = jira_auth_headers(email, token, include_content_type=True)
    url = f"{base_url}/rest/api/3/search/jql"
    try:
        return request_jira_json(url, headers, payload, "POST")
    except RuntimeError as exc:
        raise RuntimeError(f"POST Jira API v3 enhanced search failed ({exc})") from exc


def fetch_jira_issues(site, email, token, jql):
    base_url = jira_base_url(site)
    # fixVersions / resolutiondate / created are required by the date rules.
    fields = ["summary", "status", "issuetype", "labels", "description",
              "updated", "created", "resolutiondate", "fixVersions", "components"]
    max_results = 100
    next_page_token = None
    issues = []
    print("[JIRA] Fetching latest issue data using ATLASSIAN_API_TOKEN...")
    while True:
        data = fetch_jira_page(base_url, email, token, jql, max_results, fields, next_page_token)
        page_issues = data.get("issues", [])
        issues.extend(page_issues)
        total = data.get("total")
        if total is not None:
            print(f"  [JIRA] Retrieved {len(issues)} of {total} issues...")
        else:
            print(f"  [JIRA] Retrieved {len(issues)} issues...")
        if not page_issues:
            break
        if data.get("isLast"):
            break
        next_page_token = data.get("nextPageToken")
        if not next_page_token:
            break
    return {issue["key"]: issue for issue in issues if issue.get("key")}


# ───────────────────────────── ADF / dates ───────────────────────────────
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


def iso_date_only(value):
    """Return YYYY-MM-DD from a Jira datetime/date string, or None."""
    if not value or not isinstance(value, str):
        return None
    m = re.match(r'(\d{4})-(\d{2})-(\d{2})', value)
    return m.group(0) if m else None


def display_from_date(date_str, kind):
    """kind is 'Released' or 'Updated'. Returns 'Released June 2026' etc."""
    if not date_str:
        return None
    m = re.match(r'(\d{4})-(\d{2})-\d{2}', date_str)
    if not m:
        return None
    year, month = int(m.group(1)), int(m.group(2))
    return f"{kind} {MONTHS[month]} {year}"


def resolve_dates(issues):
    """Given the list of bound Jira issue dicts for one feature, return
    (release_date, last_change_date, display_date, source) per spec precedence."""
    release_dates, resolved_dates, updated_dates = [], [], []
    for issue in issues:
        f = issue.get('fields', {})
        for fv in (f.get('fixVersions') or []):
            rd = iso_date_only(fv.get('releaseDate'))
            if rd:
                release_dates.append(rd)
        rs = iso_date_only(f.get('resolutiondate'))
        if rs:
            resolved_dates.append(rs)
        up = iso_date_only(f.get('updated'))
        if up:
            updated_dates.append(up)

    last_change = max(updated_dates) if updated_dates else (
        max(resolved_dates) if resolved_dates else None)

    if release_dates:
        rd = max(release_dates)
        return rd, last_change or rd, display_from_date(rd, "Released"), "fixVersion.releaseDate"
    if resolved_dates:
        rs = max(resolved_dates)
        return None, last_change or rs, display_from_date(rs, "Updated"), "resolutiondate"
    if updated_dates:
        up = max(updated_dates)
        return None, up, display_from_date(up, "Updated"), "updated"
    return None, None, None, "none"


# ──────────────────────── curated catalogue binding ──────────────────────
def bind_feature_to_issues(feature, cache):
    """Find cached issues whose summary contains any epic_match substring."""
    matchers = [m.lower() for m in feature.get('epic_match', [])]
    bound = []
    for key, issue in cache.items():
        summary = (issue.get('fields', {}).get('summary') or '').lower()
        if any(m in summary for m in matchers):
            bound.append((key, issue))
    return bound


EXCLUDE_TYPES = {"Bug", "Subtask", "Sub-task", "Devops", "Task", "Research"}
EXCLUDE_SUMMARY_MARKERS = [
    "[dynamic system]", "failed :", "failed:", "sentry", "refactor", "regression",
    "cleanup", "migration", "infrastructure", "docker", "ci/cd", "deprecated",
    "tech stuff", "defects", "test", "duplicate", "yard", "data model",
]


def looks_customer_facing(issue):
    f = issue.get('fields', {})
    itype = f.get('issuetype', {}).get('name', '')
    summary = (f.get('summary') or '').lower()
    if itype in EXCLUDE_TYPES:
        return False
    if any(marker in summary for marker in EXCLUDE_SUMMARY_MARKERS):
        return False
    return True  # Epic / Story / Enhancement / UI-UX that reads cleanly


def suggest_module(summary):
    s = summary.lower()
    if 'qa' in s:
        return "AiMY QA"
    if 'voice' in s or 'call' in s or 'phone' in s or 'twilio' in s:
        return "AiMY Voice"
    if 'connect' in s or 'escalation' in s or 'queue' in s or 'sla' in s:
        return "AiMY Connect"
    if 'sales' in s or 'bdr' in s or 'pipeline' in s or 'outreach' in s:
        return "AiMY Sales — BDR Mode"
    if 'integration' in s or 'zendesk' in s or 'freshdesk' in s:
        return "Platform / Integrations"
    return "AiMY Knowledge"


# ──────────────────────────── output schema ──────────────────────────────
def build_output_schema():
    """Tracks + module shells (no features). Features get attached at runtime."""
    return {
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
            {"id": "knowledge", "name": "AiMY Knowledge", "track": "Support + Sales", "status": "Available foundation",
             "oneLiner": "A unified knowledge layer that grounds AiMY answers in your real content.",
             "problem": "Teams lose time hunting for the right answer, policy, case study, or process note.",
             "whatItDoes": "Connects to approved knowledge sources and gives agents or reps fast, consistent, contextual answers.",
             "worksWith": ["SOPs", "FAQs", "Product documentation", "Sales collateral", "Playbooks", "Competitive intelligence", "Case studies"],
             "integrations": ["SharePoint", "Confluence", "Google Drive", "Notion", "Helpdesk knowledge bases", "CRM-linked knowledge bases"],
             "outcome": "A single operating baseline: fewer guessed answers, faster ramp-up, and more consistent customer conversations.",
             "releaseThemes": ["Knowledge document ingestion", "FAQ and task surfaces", "Grounded product expert experiences"], "features": []},
            {"id": "voice", "name": "AiMY Voice", "track": "Support + Sales", "status": "Activation track",
             "oneLiner": "Turns calls into searchable, coachable, structured operational data.",
             "problem": "Voice conversations are usually a black box, even though they contain the richest customer signals.",
             "whatItDoes": "Captures call context, supports live assistance, and feeds transcripts and outcomes into QA, knowledge, and follow-up workflows.",
             "worksWith": ["Inbound calls", "Outbound calls", "Call recordings", "Live transcripts", "IVR interaction logs"],
             "integrations": ["Existing telephony", "CRM caller context", "Voice infrastructure", "Call transcription services"],
             "outcome": "Calls stop disappearing after they end; they become part of the same improvement loop as tickets and chats.",
             "releaseThemes": ["Native voice infrastructure", "Active call screen", "Post-call intelligence", "Caller context and follow-up actions"], "features": []},
            {"id": "qa", "name": "AiMY QA", "track": "L1 Support", "status": "Capability track",
             "oneLiner": "Continuous QA coverage across support conversations.",
             "problem": "Manual QA reviews a sample, catches issues late, and misses recurring patterns.",
             "whatItDoes": "Analyses interactions against quality standards, flags risks, and turns repeated failures into coaching and knowledge signals.",
             "worksWith": ["Support tickets", "Chat transcripts", "Email threads", "Call recordings", "Voice transcripts", "Agent response data"],
             "integrations": ["Zendesk", "Freshdesk", "ServiceNow", "Salesforce Service Cloud", "Voice data from AiMY Voice"],
             "outcome": "Quality becomes a live signal instead of a delayed audit process.",
             "releaseThemes": ["Written interaction ingestion", "AI evaluation engine", "Supervisor coaching canvas", "Knowledge gap detection"], "features": []},
            {"id": "connect", "name": "AiMY Connect", "track": "Support Operations", "status": "Supervisor layer",
             "oneLiner": "A real-time operating view for supervisors and managers.",
             "problem": "Supervisors often discover problems only after escalation, SLA risk, or quality drift has already happened.",
             "whatItDoes": "Brings operational signals together so supervisors can see performance, queue pressure, escalation patterns, and coaching needs.",
             "worksWith": ["Agent activity", "Queue metrics", "Ticket trends", "Escalation logs", "QA scores", "Flagged interactions"],
             "integrations": ["Helpdesk platforms", "Workforce management tools", "CRM systems", "Operational data sources"],
             "outcome": "Supervisors move from firefighting to proactive operations management.",
             "releaseThemes": ["Urgency and escalation intelligence", "Event-based notifications", "Queue management", "Operational risk views"], "features": []},
            {"id": "sales-bdr", "name": "AiMY Sales — BDR Mode", "track": "Sales", "status": "Sales activation track",
             "oneLiner": "AI-assisted outreach grounded in your ICP, messaging, and playbooks.",
             "problem": "Every rep runs a slightly different version of the sales motion, making scale and quality hard to manage.",
             "whatItDoes": "Helps reps draft, sequence, and follow up using approved messaging, account context, and playbook logic.",
             "worksWith": ["Prospect data", "Account data", "ICP definitions", "Outreach templates", "Historical engagement data"],
             "integrations": ["Salesforce", "HubSpot", "Sales engagement tools", "Prospecting and enrichment sources"],
             "outcome": "A repeatable outbound motion that helps new reps ramp faster and keeps experienced reps focused on conversations.",
             "releaseThemes": ["Sales engagement tracking", "Follow-up intelligence", "Contact enrichment", "Next-best-action sequencing"], "features": []},
            {"id": "sales-manager", "name": "AiMY Sales — Manager Mode", "track": "Sales Leadership", "status": "Sales leadership layer",
             "oneLiner": "Queryable pipeline visibility for sales managers.",
             "problem": "Managers rely on stale CRM updates, gut-feel forecasting, and manual rep check-ins.",
             "whatItDoes": "Gives sales leadership a natural-language way to inspect pipeline risk, stalled deals, activity gaps, and rep performance signals.",
             "worksWith": ["CRM pipeline data", "Deal stages", "Activity logs", "Engagement history", "Forecast data", "Quota and rep metrics"],
             "integrations": ["Salesforce", "HubSpot", "Revenue intelligence tools", "Forecasting tools"],
             "outcome": "Forecasting and coaching become evidence-based instead of reactive.",
             "releaseThemes": ["Sales ops hub", "Pipeline health views", "BDR activity dashboard", "Campaign execution health"], "features": []},
            {"id": "loop", "name": "Continuous Improvement Loop", "track": "Platform Layer", "status": "Cross-module value loop",
             "oneLiner": "AiMY learns from real outcomes and feeds improvements back into the operating model.",
             "problem": "Most operations improve only during manual reviews, retraining cycles, or after problems become visible.",
             "whatItDoes": "Turns QA findings, call outcomes, deal patterns, and knowledge gaps into reviewed improvement actions.",
             "worksWith": ["QA signals", "Low-confidence answers", "Won/lost outcomes", "Objection patterns", "Manager-flagged coaching moments"],
             "integrations": ["Runs across AiMY Knowledge, Voice, QA, Connect, and Sales layers"],
             "outcome": "The system compounds: every conversation and deal can improve the next one.",
             "releaseThemes": ["Knowledge gap detection", "Draft article workflow", "Sales pattern feedback", "Recurring failure analysis"], "features": []},
        ],
        "whatsNew": []
    }


# ─────────────────────────────── safety ──────────────────────────────────
BANNED_PATTERNS = [
    (re.compile(r'\b[A-Z]{2,}-\d+\b'), "Jira issue key"),
    (re.compile(r'atlassian\.net', re.I), "Atlassian URL"),
    (re.compile(r'\baccountId\b', re.I), "accountId field"),
    (re.compile(r'\bassignee\b', re.I), "assignee field"),
    (re.compile(r'\breporter\b', re.I), "reporter field"),
    (re.compile(r'\bAuthorization\b'), "Authorization header"),
    (re.compile(r'\bBearer\b'), "Bearer token"),
    (re.compile(r'ATLASSIAN_API_TOKEN'), "API token name"),
    (re.compile(r'\.env\b'), ".env reference"),
    (re.compile(r'\[Dynamic System\]', re.I), "raw engineering wording"),
    (re.compile(r'Failed\s*:', re.I), "raw test-case wording"),
    (re.compile(r'\bSentry\b', re.I), "internal tooling reference"),
    (re.compile(r'\bSubtask\b', re.I), "raw issue-type wording"),
    (re.compile(r'\bDevops\b', re.I), "raw issue-type wording"),
    (re.compile(r'Traceback \(most recent call last\)'), "stack trace"),
]

PUBLIC_LOCATIONS = [
    "catalogue-public.json",
    "data/catalogue-public.json",
    "aimy-catalogue-site/catalogue-public.json",
]


def run_safety_check():
    print("\n[SAFETY CHECK] Scanning public assets for internal Jira leaks...")
    leaked = False
    for path in PUBLIC_LOCATIONS:
        if not os.path.exists(path):
            continue
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        for pattern, label in BANNED_PATTERNS:
            hits = pattern.findall(content)
            if hits:
                sample = list(dict.fromkeys(hits))[:5]
                print(f"  [LEAK] {label} in {path}: {sample}")
                leaked = True
    if leaked:
        print("\n[SAFETY RESULT] X FAILED — internal data is leaking into public files.")
        return False
    print("  [SAFETY RESULT] OK — public assets are customer-safe.")
    return True


# ───────────────────────────── LLM (later) ───────────────────────────────
def maybe_draft_with_llm(review_items):
    """Optional future step. No-op unless ANTHROPIC_API_KEY is set.

    When a key is present this would draft review-needed items into curated
    feature CANDIDATES written to data/catalogue-llm-drafts.json for human
    approval. Drafts are NEVER auto-published — a human must move an approved
    draft into scripts/catalogue_map.py.
    """
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return False
    print("[LLM] ANTHROPIC_API_KEY detected, but auto-drafting is not enabled yet.")
    print("      (Scaffold present; implement drafting into data/catalogue-llm-drafts.json.)")
    return False


# ──────────────────────────────── main ───────────────────────────────────
def main():
    load_dotenv()
    print("=== AiMY Customer Catalogue Refresh Pipeline ===")

    site = os.environ.get('ATLASSIAN_SITE')
    email = os.environ.get('ATLASSIAN_EMAIL')
    token = os.environ.get('ATLASSIAN_API_TOKEN')
    project = os.environ.get('JIRA_PROJECT_KEY', 'AIMYIMP')

    use_cache_only = "--cache-only" in sys.argv
    cache_file = "jira_issues_cache.json"

    if use_cache_only:
        if not os.path.exists(cache_file):
            print("[ERROR] --cache-only set but no jira_issues_cache.json found.")
            sys.exit(1)
        with open(cache_file, 'r', encoding='utf-8') as f:
            cache = json.load(f)
        print(f"[OK] Loaded {len(cache)} issues from local cache (offline mode).")
    else:
        if not site or not email or not token:
            print("[ERROR] Missing credentials. Required: ATLASSIAN_SITE, ATLASSIAN_EMAIL, ATLASSIAN_API_TOKEN")
            sys.exit(1)
        print(f"[OK] Credentials verified for tenant: {site}")
        jql = (f'project = "{project}" AND statusCategory IN ("In Progress", "Done", "To Do") '
               f'ORDER BY updated DESC')
        print(f"[JQL] {jql}")
        try:
            cache = fetch_jira_issues(site, email, token, jql)
        except RuntimeError as exc:
            print(f"[ERROR] Failed to fetch Jira data: {exc}")
            sys.exit(1)
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache, f, indent=2, ensure_ascii=False)
        print(f"[OK] Fetched and cached {len(cache)} issues from Jira.")

    base = jira_base_url(site) if site else "https://your-tenant.atlassian.net"

    schema = build_output_schema()
    module_by_id = {m["id"]: m for m in schema["modules"]}

    public_features = []          # full spec records (with render aliases)
    internal_evidence = []        # one per (feature, jira key)
    bound_keys = set()            # jira keys consumed by curated features
    review_questions = []

    # 1) Bind curated features to live Jira evidence.
    for feat in CURATED_FEATURES:
        bound = bind_feature_to_issues(feat, cache)
        bound_issues = [i for _, i in bound]
        for k, _ in bound:
            bound_keys.add(k)

        release_date, last_change, display_date, source = resolve_dates(bound_issues)
        availability = feat["availability"]

        # If we promised a release but found no evidence/date, flag for review.
        if availability == "Released" and not display_date:
            availability = "Needs Review"
            review_questions.append(
                f'"{feat["featureName"]}" is marked Released but no Jira evidence/date matched '
                f'(epic_match={feat["epic_match"]}). Confirm the source title.')

        # Roadmap items show "Coming Soon", not an internal last-updated date
        # (the lastChangeDate is still kept privately in evidence).
        if availability == "Coming Soon":
            display_date = None

        record = {
            "id": feat["id"],
            "module": feat["module"],
            "featureName": feat["featureName"],
            "shortDescription": feat["shortDescription"],
            "customerProblem": feat["customerProblem"],
            "customerValue": feat["customerValue"],
            "whatChanged": feat["whatChanged"],
            "availability": availability,
            "releaseDate": release_date,
            "lastChangeDate": last_change,
            "displayDate": display_date or ("Coming Soon" if availability == "Coming Soon" else None),
            "bestFor": feat.get("bestFor", []),
            "tags": feat.get("tags", []),
            # Render-contract aliases consumed by the current website JS.
            "feature_name": feat["featureName"],
            "description": feat["shortDescription"],
            "customer_value": feat["customerValue"],
            "track": feat.get("track", "support"),
        }
        public_features.append(record)

        # Evidence: one private record per bound Jira key (never published).
        for key, issue in bound:
            f = issue.get('fields', {})
            status = f.get('status', {}).get('name', '')
            cat = f.get('status', {}).get('statusCategory', {}).get('name', '')
            internal_evidence.append({
                "publicId": feat["id"],
                "jiraKey": key,
                "jiraUrl": f"{base}/browse/{key}",
                "issueType": f.get('issuetype', {}).get('name', ''),
                "rawSummary": f.get('summary', ''),
                "rawStatus": status,
                "statusCategory": cat,
                "fixVersions": [v.get('name') for v in (f.get('fixVersions') or [])],
                "components": [c.get('name') for c in (f.get('components') or [])],
                "labels": f.get('labels', []),
                "created": iso_date_only(f.get('created')),
                "updated": iso_date_only(f.get('updated')),
                "resolved": iso_date_only(f.get('resolutiondate')),
                "releaseDateSource": source,
                "publishDecision": "Published" if availability != "Needs Review" else "Needs Review",
                "decisionReason": f"Bound to curated feature '{feat['featureName']}' via title match.",
            })

        if not bound:
            review_questions.append(
                f'"{feat["featureName"]}" matched no Jira issues — it is published from '
                f'curated copy only, with no live evidence.')

    # 2) Attach features to their module shells.
    for rec in public_features:
        mod_id = MODULE_IDS.get(rec["module"], "knowledge")
        module_by_id[mod_id]["features"].append(rec)

    # 3) Rebuild What's New from shipped curated features, newest first.
    shipped = [r for r in public_features if r["availability"] in ("Released", "Recently Updated")]
    shipped.sort(key=lambda r: r["lastChangeDate"] or "", reverse=True)
    schema["whatsNew"] = [{
        "id": r["id"],
        "title": r["featureName"],
        "module": r["module"],
        "availability": r["availability"],
        "displayDate": r["displayDate"],
        "whyItMatters": r["customerValue"],
    } for r in shipped[:7]]

    # 4) Build the private review-needed queue from unbound, customer-facing issues.
    review_needed = []
    excluded_count = 0
    for key, issue in cache.items():
        if key in bound_keys:
            continue
        if not looks_customer_facing(issue):
            excluded_count += 1
            continue
        f = issue.get('fields', {})
        summary = f.get('summary', '')
        review_needed.append({
            "jiraKey": key,
            "rawSummary": summary,
            "reason": "Customer-facing candidate not yet curated into the public catalogue.",
            "suggestedModule": suggest_module(summary),
            "suggestedMarketingName": "",
            "missingInfo": ["customer value", "marketing name", "module confirmation"],
        })

    # 5) Optional LLM scaffold (no-op unless ANTHROPIC_API_KEY set).
    maybe_draft_with_llm(review_needed)

    # 6) Write outputs.
    os.makedirs("data", exist_ok=True)
    os.makedirs("aimy-catalogue-site", exist_ok=True)
    public_json = json.dumps(schema, indent=2, ensure_ascii=False)
    for path in PUBLIC_LOCATIONS:
        with open(path, 'w', encoding='utf-8') as fp:
            fp.write(public_json)
    with open("data/catalogue-internal-evidence.json", 'w', encoding='utf-8') as fp:
        json.dump(internal_evidence, fp, indent=2, ensure_ascii=False)
    with open("data/catalogue-review-needed.json", 'w', encoding='utf-8') as fp:
        json.dump(review_needed, fp, indent=2, ensure_ascii=False)

    # 7) Internal review notes.
    modules_covered = sorted({r["module"] for r in public_features})
    write_review_notes(public_features, internal_evidence, review_needed,
                       excluded_count, modules_covered, review_questions)

    # 8) Safety check (must pass).
    safe = run_safety_check()

    # 9) Summary.
    print("\n" + "=" * 60)
    print("  AiMY CATALOGUE PIPELINE — SUMMARY")
    print("=" * 60)
    print(f"  1. Jira items processed      : {len(cache)}")
    print(f"  2. Public features created   : {len(public_features)}")
    print(f"  3. Items excluded (internal) : {excluded_count}")
    print(f"  4. Items needing review      : {len(review_needed)}")
    print(f"  5. Modules covered           : {len(modules_covered)} -> {', '.join(modules_covered)}")
    print(f"  6. Files changed             : catalogue-public.json (x3), "
          f"data/catalogue-internal-evidence.json, data/catalogue-review-needed.json, internal-review-notes.md")
    print(f"  7. Public safety check       : {'PASSED' if safe else 'FAILED'}")
    print(f"  8. Human review questions    : {len(review_questions)}")
    for q in review_questions[:10]:
        print(f"       - {q}")
    print("=" * 60)

    if not safe:
        print("\n[ERROR] Pipeline aborted: safety check failed. Do NOT publish.")
        sys.exit(1)
    print("\n[OK] Pipeline complete. Review internal-review-notes.md, then push when ready.")


def write_review_notes(public_features, evidence, review_needed,
                       excluded_count, modules_covered, questions):
    by_avail = {}
    for r in public_features:
        by_avail.setdefault(r["availability"], []).append(r)
    lines = []
    lines.append("# AiMY Catalogue — Internal Review Notes")
    lines.append("")
    lines.append("> Auto-generated by `scripts/refresh-catalogue.py`. Private — do not deploy.")
    lines.append("")
    lines.append("## Summary")
    lines.append(f"- Public features published: **{len(public_features)}**")
    lines.append(f"- Jira evidence records: **{len(evidence)}**")
    lines.append(f"- Items in review-needed queue: **{len(review_needed)}**")
    lines.append(f"- Internal items excluded: **{excluded_count}**")
    lines.append(f"- Modules covered: {', '.join(modules_covered)}")
    lines.append("")
    lines.append("## Published features by availability")
    for avail in ["Released", "Recently Updated", "Coming Soon", "Needs Review"]:
        items = by_avail.get(avail, [])
        if not items:
            continue
        lines.append(f"### {avail} ({len(items)})")
        for r in items:
            date = r["displayDate"] or "—"
            lines.append(f"- **{r['featureName']}** ({r['module']}) — {date}")
        lines.append("")
    lines.append("## Open human-review questions")
    if questions:
        for q in questions:
            lines.append(f"- {q}")
    else:
        lines.append("- None.")
    lines.append("")
    lines.append("## Review-needed queue (top 25 customer-facing candidates)")
    for item in review_needed[:25]:
        lines.append(f"- [{item['jiraKey']}] {item['rawSummary']} "
                     f"(suggested: {item['suggestedModule']})")
    if len(review_needed) > 25:
        lines.append(f"- ...and {len(review_needed) - 25} more in data/catalogue-review-needed.json")
    lines.append("")
    with open("internal-review-notes.md", 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
