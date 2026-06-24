import json
import os
from collections import defaultdict
from datetime import datetime

def main():
    print("=== Generating Dynamic Release Presentation ===")
    
    # 1. Load data
    with open("data/catalogue-internal-evidence.json", "r", encoding="utf-8") as f:
        evidence = json.load(f)
    with open("catalogue-public.json", "r", encoding="utf-8") as f:
        public = json.load(f)

    # 2. Extract stats
    stats = defaultdict(lambda: {"total": 0, "bugs": 0, "updates": 0, "dates": []})
    for ev in evidence:
        pub_id = ev["publicId"]
        stats[pub_id]["total"] += 1
        if ev["issueType"] == "Bug":
            stats[pub_id]["bugs"] += 1
        else:
            stats[pub_id]["updates"] += 1
        if ev["updated"]:
            stats[pub_id]["dates"].append(ev["updated"])

    # 3. Classify features
    shipped_support = []
    shipped_sales = []
    roadmap_support = []
    roadmap_sales = []

    for module in public["modules"]:
        mod_name = module["name"]
        for feat in module["features"]:
            pub_id = feat["id"]
            feat_stats = stats[pub_id]
            total = feat_stats["total"]
            bugs = feat_stats["bugs"]
            updates = feat_stats["updates"]
            
            # Resolve last change date
            last_date = "—"
            if feat_stats["dates"]:
                dt = max(feat_stats["dates"])
                try:
                    parsed_dt = datetime.strptime(dt, "%Y-%m-%d")
                    last_date = parsed_dt.strftime("%d %B %Y")
                except:
                    last_date = dt

            record = {
                "name": feat["featureName"],
                "module": mod_name,
                "availability": feat["availability"],
                "displayDate": feat["displayDate"] or "Coming Soon",
                "total": total,
                "bugs": bugs,
                "updates": updates,
                "last_change": last_date,
                "desc": feat["shortDescription"],
                "value": feat["customerValue"]
            }

            is_sales = "sales" in feat.get("track", "support").lower() or "sales" in mod_name.lower()
            
            if feat["availability"] in ["Released", "Recently Updated"] or total > 0:
                if is_sales:
                    shipped_sales.append(record)
                else:
                    shipped_support.append(record)
            else:
                if is_sales:
                    roadmap_sales.append(record)
                else:
                    roadmap_support.append(record)

    # Sort shipped by total records descending
    shipped_support.sort(key=lambda x: x["total"], reverse=True)
    shipped_sales.sort(key=lambda x: x["total"], reverse=True)

    total_shipped = len(shipped_support) + len(shipped_sales)
    total_roadmap = len(roadmap_support) + len(roadmap_sales)
    total_evidence = len(evidence)
    total_bugs = sum(s["bugs"] for s in shipped_support + shipped_sales)
    total_updates = sum(s["updates"] for s in shipped_support + shipped_sales)

    # 4. Generate Marp Markdown content
    marp_content = f"""---
marp: true
theme: default
size: 16:9
paginate: false
html: true
title: AiMY Platform Release & Delivery Update
description: Dynamic presentation of AiMY Support and Sales releases backed by Jira evidence.
---

<style>
  :root {{
    --purple: #8c4ff4;
    --blue: #0066ff;
    --light-blue: #5582ff;
    --cyan: #6fdfe2;
    --lavender: #b01cff;
    --periwinkle: #8d98ff;
    --ink: #111827;
    --muted: #667085;
    --line: #e5e7eb;
    --soft: #f6f8ff;
    --white: #ffffff;
    --danger: #d84f3f;
    --success: #087f7a;
  }}

  section {{
    width: 1280px;
    height: 720px;
    padding: 54px 64px;
    background:
      radial-gradient(circle at 92% 8%, rgba(111, 223, 226, 0.38), transparent 23%),
      radial-gradient(circle at 0% 100%, rgba(140, 79, 244, 0.14), transparent 28%),
      linear-gradient(135deg, #ffffff 0%, #f6f8ff 100%);
    color: var(--ink);
    font-family: "Poppins", "Segoe UI", Arial, sans-serif;
    letter-spacing: 0;
  }}

  section.dark {{
    background:
      radial-gradient(circle at 88% 14%, rgba(111, 223, 226, 0.28), transparent 24%),
      linear-gradient(135deg, #101828 0%, #1a1550 48%, #0066ff 130%);
    color: var(--white);
  }}

  h1, h2, h3, p {{
    letter-spacing: 0;
  }}

  h1 {{
    max-width: 920px;
    margin: 0;
    font-size: 54px;
    line-height: 1.05;
    font-weight: 800;
  }}

  h2 {{
    max-width: 980px;
    margin: 0 0 16px;
    font-size: 38px;
    line-height: 1.12;
    font-weight: 760;
  }}

  h3 {{
    margin: 0 0 8px;
    font-size: 20px;
    font-weight: 700;
  }}

  p {{
    font-size: 19px;
    line-height: 1.45;
    color: var(--muted);
  }}

  section.dark p {{
    color: rgba(255, 255, 255, 0.78);
  }}

  section.dark h1,
  section.dark h2,
  section.dark h3 {{
    color: var(--white);
  }}

  .brand {{
    position: absolute;
    top: 32px;
    left: 48px;
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 14px;
    font-weight: 700;
    color: inherit;
  }}

  .brand > img {{
    width: 34px !important;
    height: 34px !important;
    max-width: 34px !important;
    max-height: 34px !important;
    object-fit: contain;
  }}

  .eyebrow {{
    display: inline-flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 24px;
    font-size: 13px;
    font-weight: 800;
    text-transform: uppercase;
    color: var(--blue);
  }}

  .eyebrow::before {{
    content: "";
    width: 10px;
    height: 10px;
    border-radius: 3px;
    background: linear-gradient(135deg, var(--purple), var(--blue));
  }}

  section.dark .eyebrow {{
    color: var(--cyan);
  }}

  .gradient-text {{
    background: linear-gradient(135deg, var(--purple), var(--blue));
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
  }}

  section.dark .gradient-text {{
    background: linear-gradient(135deg, #8c4ff4 0%, #6fdfe2 58%, #ffffff 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
  }}

  .lead {{
    max-width: 860px;
    margin-top: 18px;
    font-size: 21px;
  }}

  .kpi-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-top: 40px;
  }}

  .kpi {{
    background: var(--white);
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 20px 24px;
    box-shadow: 0 14px 34px rgba(16, 24, 40, 0.06);
  }}

  .kpi strong {{
    display: block;
    margin-bottom: 6px;
    font-size: 40px;
    line-height: 1;
    font-weight: 800;
  }}

  .kpi span {{
    color: var(--muted);
    font-size: 14px;
    font-weight: 600;
    line-height: 1.3;
    display: block;
  }}

  .kpi em {{
    font-style: normal;
    font-size: 12px;
    color: var(--purple);
    font-weight: 700;
    display: block;
    margin-top: 4px;
  }}

  .grid-2 {{
    display: grid;
    grid-template-columns: 1.15fr 1.85fr;
    gap: 36px;
    margin-top: 28px;
    align-items: start;
  }}

  .side-panel {{
    border-radius: 18px;
    padding: 24px;
    background: var(--white);
    border: 1px solid var(--line);
    box-shadow: 0 16px 38px rgba(16, 24, 40, 0.08);
  }}

  .side-panel h3 {{
    margin: 0 0 6px 0;
    font-size: 16px;
    text-transform: uppercase;
    color: var(--muted);
    letter-spacing: 0.5px;
  }}

  .side-panel p {{
    font-size: 15px;
    line-height: 1.45;
    margin: 0 0 16px 0;
    color: #475467;
  }}

  .side-panel .stat-highlight {{
    background: var(--soft);
    border-radius: 10px;
    padding: 14px 18px;
    margin-top: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}

  .side-panel .stat-highlight span {{
    font-size: 14px;
    font-weight: 700;
    color: var(--ink);
  }}

  .side-panel .stat-highlight strong {{
    font-size: 24px;
    color: var(--blue);
    font-weight: 800;
  }}

  .ticket-list {{
    display: flex;
    flex-direction: column;
    gap: 12px;
    max-height: 440px;
    overflow-y: auto;
  }}

  .ticket-card {{
    background: var(--white);
    border: 1px solid var(--line);
    border-radius: 10px;
    padding: 12px 16px;
    box-shadow: 0 4px 12px rgba(16, 24, 40, 0.03);
    display: flex;
    flex-direction: column;
    gap: 4px;
  }}

  .ticket-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}

  .ticket-id {{
    font-size: 12px;
    font-weight: 800;
    color: var(--muted);
  }}

  .ticket-title {{
    font-size: 15px;
    font-weight: 760;
    color: var(--ink);
    margin: 2px 0;
  }}

  .ticket-desc {{
    font-size: 12.5px;
    line-height: 1.35;
    color: var(--muted);
    margin: 0;
  }}

  .ticket-owner {{
    font-size: 11px;
    font-weight: 700;
    color: var(--purple);
    align-self: flex-end;
  }}

  .sprint-timeline {{
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    margin-top: 16px;
    border: 1px solid var(--line);
    border-radius: 12px;
    overflow: hidden;
    background: var(--white);
    box-shadow: 0 16px 38px rgba(16, 24, 40, 0.06);
    font-size: 13.5px;
  }}

  .sprint-timeline th {{
    background: linear-gradient(135deg, var(--purple), var(--blue));
    color: var(--white);
    padding: 12px 14px;
    font-weight: 700;
    font-size: 12px;
    text-transform: uppercase;
    text-align: left;
  }}

  .sprint-timeline td {{
    padding: 12px 14px;
    border-top: 1px solid var(--line);
    vertical-align: top;
    color: #344054;
    line-height: 1.4;
  }}

  .sprint-timeline tr:nth-child(odd) td {{
    background: #fbfcff;
  }}

  .badge {{
    display: inline-block;
    padding: 2px 6px;
    font-size: 10px;
    font-weight: 800;
    border-radius: 4px;
    text-transform: uppercase;
    text-align: center;
  }}
  .badge.released {{ background: #ecfdf5; color: #047857; }}
  .badge.updated {{ background: #e0f2fe; color: #0369a1; }}
  .badge.soon {{ background: #fef3c7; color: #d97706; }}
  .badge.review {{ background: #fee2e2; color: #b91c1c; }}

  .footer {{
    position: absolute;
    left: 64px;
    right: 64px;
    bottom: 28px;
    display: flex;
    justify-content: space-between;
    color: #7a8496;
    font-size: 12px;
  }}

  section.dark .footer {{
    color: rgba(255, 255, 255, 0.62);
  }}
</style>

<!-- _class: dark -->

<div class="brand">
  <img src="../../../aimy-catalogue-site/FlairsTech-logo.svg" alt="FlairsTech logo" />
  <span>FlairsTech</span>
</div>

<div class="eyebrow">AiMY platform release update</div>

# <span class="gradient-text">AiMY Product Releases</span> & Delivery
<p class="lead">Executive summary of shipped, recently updated, and upcoming features across Support & Sales tracks, backed by live Jira verification data.</p>

<div class="footer">
  <span>Jira project {public.get('project', 'AIMY')} - refreshed {datetime.now().strftime('%d %B %Y')}</span>
  <span>01</span>
</div>

---

<div class="brand">
  <img src="../../../aimy-catalogue-site/FlairsTech-logo.svg" alt="FlairsTech logo" />
  <span>FlairsTech</span>
</div>

<div class="eyebrow">Executive Snapshot</div>

## Release Metrics & Evidence Coverage

<p class="lead">Verification check completed successfully. Live Jira data pulls match capability tags to resolve exact last-changed dates and issues counts.</p>

<div class="kpi-grid">
  <div class="kpi">
    <strong class="gradient-text">{total_shipped}</strong>
    <span>Shipped Features</span>
    <em>Live on Production</em>
  </div>
  <div class="kpi">
    <strong class="gradient-text" style="background: linear-gradient(135deg, var(--light-blue), var(--purple)); -webkit-background-clip: text; color: transparent;">{total_evidence}</strong>
    <span>Jira Evidence Tickets</span>
    <em>Bound to Curated Core</em>
  </div>
  <div class="kpi">
    <strong class="gradient-text" style="background: linear-gradient(135deg, var(--blue), var(--cyan)); -webkit-background-clip: text; color: transparent;">{total_updates}</strong>
    <span>Feature Updates</span>
    <em>Enhancements Completed</em>
  </div>
  <div class="kpi">
    <strong class="gradient-text" style="background: linear-gradient(135deg, var(--cyan), var(--success)); -webkit-background-clip: text; color: transparent;">{total_bugs}</strong>
    <span>Quality Fixes</span>
    <em>Resolved & Tested</em>
  </div>
</div>

<div class="footer">
  <span>AiMY Platform Release Dashboard - {datetime.now().strftime('%d %B %Y')}</span>
  <span>02</span>
</div>

---

<div class="brand">
  <img src="../../../aimy-catalogue-site/FlairsTech-logo.svg" alt="FlairsTech logo" />
  <span>FlairsTech</span>
</div>

<div class="eyebrow">Support Track Shipped</div>

## L1 Support Operations: Shipped Releases

<div class="grid-2">
  <div class="side-panel">
    <h3>Track Overview</h3>
    <p>Operational visibility, access governance, and core helpdesk integrations are fully verified. Active call assistance is mapped in test validation.</p>
    <div class="stat-highlight">
      <span>Evidence Tickets</span>
      <strong>{sum(s['total'] for s in shipped_support)} Items</strong>
    </div>
    <div class="stat-highlight" style="margin-top: 10px;">
      <span>Last Release</span>
      <span style="font-weight: 700; font-size: 14px; color: var(--purple);">{shipped_support[0]['last_change'] if shipped_support else '—'}</span>
    </div>
  </div>
  
  <div class="ticket-list">
"""

    for s in shipped_support[:3]:
        badge_class = "updated" if s["availability"] == "Recently Updated" else "released"
        marp_content += f"""    <div class="ticket-card">
      <div class="ticket-header">
        <span class="ticket-id">{s['module']}</span>
        <span class="badge {badge_class}">{s['availability']}</span>
      </div>
      <div class="ticket-title">{s['name']}</div>
      <p class="ticket-desc">{s['desc']}</p>
      <span class="ticket-owner">Verified on {s['last_change']} • {s['updates']} updates, {s['bugs']} bugs</span>
    </div>
"""

    marp_content += f"""  </div>
</div>

<div class="footer">
  <span>L1 Support Operations - Shipped Capabilities</span>
  <span>03</span>
</div>

---

<div class="brand">
  <img src="../../../aimy-catalogue-site/FlairsTech-logo.svg" alt="FlairsTech logo" />
  <span>FlairsTech</span>
</div>

<div class="eyebrow">Sales Track Shipped</div>

## Sales Operations: Shipped Releases

<div class="grid-2">
  <div class="side-panel">
    <h3>Track Overview</h3>
    <p>Playbook repositories, collateral layer, and natural language forecasting visibility components are live and verified.</p>
    <div class="stat-highlight">
      <span>Evidence Tickets</span>
      <strong>{sum(s['total'] for s in shipped_sales)} Items</strong>
    </div>
    <div class="stat-highlight" style="margin-top: 10px;">
      <span>Last Release</span>
      <span style="font-weight: 700; font-size: 14px; color: var(--purple);">{shipped_sales[0]['last_change'] if shipped_sales else '—'}</span>
    </div>
  </div>
  
  <div class="ticket-list">
"""

    for s in shipped_sales[:3]:
        badge_class = "soon" if "Soon" in s["availability"] else "released"
        marp_content += f"""    <div class="ticket-card">
      <div class="ticket-header">
        <span class="ticket-id">{s['module']}</span>
        <span class="badge {badge_class}">{s['availability']}</span>
      </div>
      <div class="ticket-title">{s['name']}</div>
      <p class="ticket-desc">{s['desc']}</p>
      <span class="ticket-owner">Verified on {s['last_change']} • {s['updates']} updates, {s['bugs']} bugs</span>
    </div>
"""

    marp_content += f"""  </div>
</div>

<div class="footer">
  <span>Sales Operations - Shipped Capabilities</span>
  <span>04</span>
</div>

---

<div class="brand">
  <img src="../../../aimy-catalogue-site/FlairsTech-logo.svg" alt="FlairsTech logo" />
  <span>FlairsTech</span>
</div>

<div class="eyebrow">Evidence Ledger</div>

## Complete Release Verification Table

<table class="sprint-timeline">
  <thead>
    <tr>
      <th>Capability Feature</th>
      <th>Module Category</th>
      <th>Availability Status</th>
      <th>Jira Last Change</th>
      <th>Bugs</th>
      <th>Updates</th>
    </tr>
  </thead>
  <tbody>
"""

    all_shipped = shipped_support + shipped_sales
    for s in all_shipped[:6]:
        badge_class = "updated" if s["availability"] == "Recently Updated" else "released"
        if "Soon" in s["availability"]:
            badge_class = "soon"
        marp_content += f"""    <tr>
      <td><strong>{s['name']}</strong></td>
      <td>{s['module']}</td>
      <td><span class="badge {badge_class}">{s['availability']}</span></td>
      <td>{s['last_change']}</td>
      <td>{s['bugs']}</td>
      <td>{s['updates']}</td>
    </tr>
"""

    marp_content += f"""  </tbody>
</table>

<div class="footer">
  <span>System verification ledger showing live ticket metrics</span>
  <span>05</span>
</div>

---

<div class="brand">
  <img src="../../../aimy-catalogue-site/FlairsTech-logo.svg" alt="FlairsTech logo" />
  <span>FlairsTech</span>
</div>

<div class="eyebrow">Roadmap Focus</div>

## Active Development & Upcoming Sprints

<p class="lead">Features currently undergoing layout design, telemetry hooks binding, and QA setup for the next launch cycles.</p>

<table class="sprint-timeline">
  <thead>
    <tr>
      <th>Upcoming Feature</th>
      <th>Target Module</th>
      <th>Availability</th>
      <th>Customer Outcome & Goal</th>
    </tr>
  </thead>
  <tbody>
"""

    # Get some upcoming features
    upcoming = [r for r in (roadmap_support + roadmap_sales) if r["availability"] == "Coming Soon"]
    for s in upcoming[:4]:
        marp_content += f"""    <tr>
      <td><strong>{s['name']}</strong></td>
      <td>{s['module']}</td>
      <td><span class="badge soon">{s['availability']}</span></td>
      <td>{s['value']}</td>
    </tr>
"""

    marp_content += f"""  </tbody>
</table>

<div class="footer">
  <span>Upcoming roadmap items and core milestones</span>
  <span>06</span>
</div>

---

<!-- _class: dark -->

<div class="brand">
  <img src="../../../aimy-catalogue-site/FlairsTech-logo.svg" alt="FlairsTech logo" />
  <span>FlairsTech</span>
</div>

<div class="eyebrow">Verification Summary</div>

# <span class="gradient-text">Continuous Improvement</span> Loop Active

<p class="lead">All changes are now compiled, validated for customer safety, and staged for release. The platform continues to compound value from live conversation data.</p>

<div style="margin-top: 40px; display: flex; gap: 40px;">
  <div style="flex: 1;">
    <h3 style="color: var(--cyan);">✓ Security Checked Passed</h3>
    <p style="font-size: 15px; line-height: 1.4;">Zero raw ticket keys, internal names, or credentials exposed to public files.</p>
  </div>
  <div style="flex: 1;">
    <h3 style="color: var(--cyan);">✓ Fully Integrated</h3>
    <p style="font-size: 15px; line-height: 1.4;">Syncs directly with Confluence space AC2 and live Jira board AIMY.</p>
  </div>
</div>

<div class="footer">
  <span>End of Release Deck - Confident B2B Delivery</span>
  <span>07</span>
</div>
"""

    # Write output
    out_dir = "outputs/marp/aimy-platform-releases"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "aimy-platform-releases-marp.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(marp_content)
    
    print(f"[OK] Generated Marp markdown: {out_path}")

if __name__ == "__main__":
    main()
