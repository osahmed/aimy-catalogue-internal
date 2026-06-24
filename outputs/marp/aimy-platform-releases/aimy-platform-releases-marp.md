---
marp: true
theme: default
size: 16:9
paginate: false
html: true
title: AiMY Platform Release & Delivery Update
description: Dynamic presentation of AiMY Support and Sales releases backed by Jira evidence.
---

<style>
  :root {
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
  }

  section {
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
  }

  section.dark {
    background:
      radial-gradient(circle at 88% 14%, rgba(111, 223, 226, 0.28), transparent 24%),
      linear-gradient(135deg, #101828 0%, #1a1550 48%, #0066ff 130%);
    color: var(--white);
  }

  h1, h2, h3, p {
    letter-spacing: 0;
  }

  h1 {
    max-width: 920px;
    margin: 0;
    font-size: 54px;
    line-height: 1.05;
    font-weight: 800;
  }

  h2 {
    max-width: 980px;
    margin: 0 0 16px;
    font-size: 38px;
    line-height: 1.12;
    font-weight: 760;
  }

  h3 {
    margin: 0 0 8px;
    font-size: 20px;
    font-weight: 700;
  }

  p {
    font-size: 19px;
    line-height: 1.45;
    color: var(--muted);
  }

  section.dark p {
    color: rgba(255, 255, 255, 0.78);
  }

  section.dark h1,
  section.dark h2,
  section.dark h3 {
    color: var(--white);
  }

  .brand {
    position: absolute;
    top: 32px;
    left: 48px;
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 14px;
    font-weight: 700;
    color: inherit;
  }

  .brand > img {
    width: 34px !important;
    height: 34px !important;
    max-width: 34px !important;
    max-height: 34px !important;
    object-fit: contain;
  }

  .eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 24px;
    font-size: 13px;
    font-weight: 800;
    text-transform: uppercase;
    color: var(--blue);
  }

  .eyebrow::before {
    content: "";
    width: 10px;
    height: 10px;
    border-radius: 3px;
    background: linear-gradient(135deg, var(--purple), var(--blue));
  }

  section.dark .eyebrow {
    color: var(--cyan);
  }

  .gradient-text {
    background: linear-gradient(135deg, var(--purple), var(--blue));
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
  }

  section.dark .gradient-text {
    background: linear-gradient(135deg, #8c4ff4 0%, #6fdfe2 58%, #ffffff 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
  }

  .lead {
    max-width: 860px;
    margin-top: 18px;
    font-size: 21px;
  }

  .kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-top: 40px;
  }

  .kpi {
    background: var(--white);
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 20px 24px;
    box-shadow: 0 14px 34px rgba(16, 24, 40, 0.06);
  }

  .kpi strong {
    display: block;
    margin-bottom: 6px;
    font-size: 40px;
    line-height: 1;
    font-weight: 800;
  }

  .kpi span {
    color: var(--muted);
    font-size: 14px;
    font-weight: 600;
    line-height: 1.3;
    display: block;
  }

  .kpi em {
    font-style: normal;
    font-size: 12px;
    color: var(--purple);
    font-weight: 700;
    display: block;
    margin-top: 4px;
  }

  .grid-2 {
    display: grid;
    grid-template-columns: 1.15fr 1.85fr;
    gap: 36px;
    margin-top: 28px;
    align-items: start;
  }

  .side-panel {
    border-radius: 18px;
    padding: 24px;
    background: var(--white);
    border: 1px solid var(--line);
    box-shadow: 0 16px 38px rgba(16, 24, 40, 0.08);
  }

  .side-panel h3 {
    margin: 0 0 6px 0;
    font-size: 16px;
    text-transform: uppercase;
    color: var(--muted);
    letter-spacing: 0.5px;
  }

  .side-panel p {
    font-size: 15px;
    line-height: 1.45;
    margin: 0 0 16px 0;
    color: #475467;
  }

  .side-panel .stat-highlight {
    background: var(--soft);
    border-radius: 10px;
    padding: 14px 18px;
    margin-top: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .side-panel .stat-highlight span {
    font-size: 14px;
    font-weight: 700;
    color: var(--ink);
  }

  .side-panel .stat-highlight strong {
    font-size: 24px;
    color: var(--blue);
    font-weight: 800;
  }

  .ticket-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
    max-height: 440px;
    overflow-y: auto;
  }

  .ticket-card {
    background: var(--white);
    border: 1px solid var(--line);
    border-radius: 10px;
    padding: 12px 16px;
    box-shadow: 0 4px 12px rgba(16, 24, 40, 0.03);
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .ticket-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .ticket-id {
    font-size: 12px;
    font-weight: 800;
    color: var(--muted);
  }

  .ticket-title {
    font-size: 15px;
    font-weight: 760;
    color: var(--ink);
    margin: 2px 0;
  }

  .ticket-desc {
    font-size: 12.5px;
    line-height: 1.35;
    color: var(--muted);
    margin: 0;
  }

  .ticket-owner {
    font-size: 11px;
    font-weight: 700;
    color: var(--purple);
    align-self: flex-end;
  }

  .sprint-timeline {
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
  }

  .sprint-timeline th {
    background: linear-gradient(135deg, var(--purple), var(--blue));
    color: var(--white);
    padding: 12px 14px;
    font-weight: 700;
    font-size: 12px;
    text-transform: uppercase;
    text-align: left;
  }

  .sprint-timeline td {
    padding: 12px 14px;
    border-top: 1px solid var(--line);
    vertical-align: top;
    color: #344054;
    line-height: 1.4;
  }

  .sprint-timeline tr:nth-child(odd) td {
    background: #fbfcff;
  }

  .badge {
    display: inline-block;
    padding: 2px 6px;
    font-size: 10px;
    font-weight: 800;
    border-radius: 4px;
    text-transform: uppercase;
    text-align: center;
  }
  .badge.released { background: #ecfdf5; color: #047857; }
  .badge.updated { background: #e0f2fe; color: #0369a1; }
  .badge.soon { background: #fef3c7; color: #d97706; }
  .badge.review { background: #fee2e2; color: #b91c1c; }

  .footer {
    position: absolute;
    left: 64px;
    right: 64px;
    bottom: 28px;
    display: flex;
    justify-content: space-between;
    color: #7a8496;
    font-size: 12px;
  }

  section.dark .footer {
    color: rgba(255, 255, 255, 0.62);
  }
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
  <span>Jira project AIMY - refreshed 24 June 2026</span>
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
    <strong class="gradient-text">6</strong>
    <span>Shipped Features</span>
    <em>Live on Production</em>
  </div>
  <div class="kpi">
    <strong class="gradient-text" style="background: linear-gradient(135deg, var(--light-blue), var(--purple)); -webkit-background-clip: text; color: transparent;">124</strong>
    <span>Jira Evidence Tickets</span>
    <em>Bound to Curated Core</em>
  </div>
  <div class="kpi">
    <strong class="gradient-text" style="background: linear-gradient(135deg, var(--blue), var(--cyan)); -webkit-background-clip: text; color: transparent;">102</strong>
    <span>Feature Updates</span>
    <em>Enhancements Completed</em>
  </div>
  <div class="kpi">
    <strong class="gradient-text" style="background: linear-gradient(135deg, var(--cyan), var(--success)); -webkit-background-clip: text; color: transparent;">22</strong>
    <span>Quality Fixes</span>
    <em>Resolved & Tested</em>
  </div>
</div>

<div class="footer">
  <span>AiMY Platform Release Dashboard - 24 June 2026</span>
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
      <strong>61 Items</strong>
    </div>
    <div class="stat-highlight" style="margin-top: 10px;">
      <span>Last Release</span>
      <span style="font-weight: 700; font-size: 14px; color: var(--purple);">24 June 2026</span>
    </div>
  </div>
  
  <div class="ticket-list">
    <div class="ticket-card">
      <div class="ticket-header">
        <span class="ticket-id">AiMY Connect</span>
        <span class="badge updated">Recently Updated</span>
      </div>
      <div class="ticket-title">Supervisor Operations Hub</div>
      <p class="ticket-desc">A real-time operating view of queue pressure, agent state, and risk for supervisors, stakeholders, and clients.</p>
      <span class="ticket-owner">Verified on 24 June 2026 • 38 updates, 10 bugs</span>
    </div>
    <div class="ticket-card">
      <div class="ticket-header">
        <span class="ticket-id">AiMY Voice</span>
        <span class="badge released">Coming Soon</span>
      </div>
      <div class="ticket-title">Active Call Assist Screen</div>
      <p class="ticket-desc">A live call screen that shows transcription and matching knowledge side-by-side while an agent is on a call.</p>
      <span class="ticket-owner">Verified on 02 June 2026 • 11 updates, 0 bugs</span>
    </div>
    <div class="ticket-card">
      <div class="ticket-header">
        <span class="ticket-id">AiMY Knowledge</span>
        <span class="badge released">Released</span>
      </div>
      <div class="ticket-title">Roles & Access Management</div>
      <p class="ticket-desc">Controls who can see and manage knowledge, entities, and permissions across teams.</p>
      <span class="ticket-owner">Verified on 23 June 2026 • 1 updates, 0 bugs</span>
    </div>
  </div>
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
      <strong>63 Items</strong>
    </div>
    <div class="stat-highlight" style="margin-top: 10px;">
      <span>Last Release</span>
      <span style="font-weight: 700; font-size: 14px; color: var(--purple);">24 June 2026</span>
    </div>
  </div>
  
  <div class="ticket-list">
    <div class="ticket-card">
      <div class="ticket-header">
        <span class="ticket-id">AiMY Sales — BDR Mode</span>
        <span class="badge released">Released</span>
      </div>
      <div class="ticket-title">Sales Playbooks & Collateral Layer</div>
      <p class="ticket-desc">Gives reps one grounded place for approved messaging, positioning, battlecards, and collateral.</p>
      <span class="ticket-owner">Verified on 24 June 2026 • 49 updates, 12 bugs</span>
    </div>
    <div class="ticket-card">
      <div class="ticket-header">
        <span class="ticket-id">AiMY Sales — Manager Mode</span>
        <span class="badge soon">Coming Soon</span>
      </div>
      <div class="ticket-title">Natural-Language Pipeline Visibility for Managers</div>
      <p class="ticket-desc">Sales managers can ask natural-language questions about pipeline movement, stalled deals, recent activity, and coaching opportunities.</p>
      <span class="ticket-owner">Verified on 18 June 2026 • 2 updates, 0 bugs</span>
    </div>
  </div>
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
    <tr>
      <td><strong>Supervisor Operations Hub</strong></td>
      <td>AiMY Connect</td>
      <td><span class="badge updated">Recently Updated</span></td>
      <td>24 June 2026</td>
      <td>10</td>
      <td>38</td>
    </tr>
    <tr>
      <td><strong>Active Call Assist Screen</strong></td>
      <td>AiMY Voice</td>
      <td><span class="badge soon">Coming Soon</span></td>
      <td>02 June 2026</td>
      <td>0</td>
      <td>11</td>
    </tr>
    <tr>
      <td><strong>Roles & Access Management</strong></td>
      <td>AiMY Knowledge</td>
      <td><span class="badge released">Released</span></td>
      <td>23 June 2026</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <td><strong>Helpdesk Integrations</strong></td>
      <td>AiMY Knowledge</td>
      <td><span class="badge soon">Coming Soon</span></td>
      <td>02 June 2026</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <td><strong>Sales Playbooks & Collateral Layer</strong></td>
      <td>AiMY Sales — BDR Mode</td>
      <td><span class="badge released">Released</span></td>
      <td>24 June 2026</td>
      <td>12</td>
      <td>49</td>
    </tr>
    <tr>
      <td><strong>Natural-Language Pipeline Visibility for Managers</strong></td>
      <td>AiMY Sales — Manager Mode</td>
      <td><span class="badge soon">Coming Soon</span></td>
      <td>18 June 2026</td>
      <td>0</td>
      <td>2</td>
    </tr>
  </tbody>
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
    <tr>
      <td><strong>Native Calling Infrastructure</strong></td>
      <td>AiMY Voice</td>
      <td><span class="badge soon">Coming Soon</span></td>
      <td>A reliable voice foundation that the rest of the improvement loop can build on.</td>
    </tr>
    <tr>
      <td><strong>Post-Call Intelligence</strong></td>
      <td>AiMY Voice</td>
      <td><span class="badge soon">Coming Soon</span></td>
      <td>Every call feeds QA, knowledge, and follow-up without manual write-up.</td>
    </tr>
    <tr>
      <td><strong>AI Evaluation Engine</strong></td>
      <td>AiMY QA</td>
      <td><span class="badge soon">Coming Soon</span></td>
      <td>Critical risks and tone issues are flagged within minutes of a conversation closing.</td>
    </tr>
    <tr>
      <td><strong>SLA-Aware Triage & Routing</strong></td>
      <td>AiMY Connect</td>
      <td><span class="badge soon">Coming Soon</span></td>
      <td>Protects key accounts by getting the right cases to the right people first.</td>
    </tr>
  </tbody>
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
