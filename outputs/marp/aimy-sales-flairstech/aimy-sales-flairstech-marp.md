---
marp: true
theme: default
size: 16:9
paginate: false
html: true
title: AiMY Sales Jira Delivery Roadmap
description: Agile delivery roadmap for AiMY Sales, styled with FlairsTech B2B UI/UX.
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
  .badge.uat { background: #e0f2fe; color: #0369a1; }
  .badge.rft { background: #ecfdf5; color: #047857; }
  .badge.ip { background: #fef3c7; color: #d97706; }
  .badge.cr { background: #e0e7ff; color: #4338ca; }
  .badge.qf { background: #fee2e2; color: #b91c1c; }
  .badge.pl { background: #f3f4f6; color: #374151; }
  .badge.bl { background: #ffedd5; color: #c2410c; }

  .grid-3 {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
    margin-top: 24px;
  }

  .member-card {
    background: var(--white);
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 16px 20px;
    box-shadow: 0 10px 24px rgba(16, 24, 40, 0.04);
  }

  .member-card h3 {
    margin: 0 0 4px;
    font-size: 17px;
    color: var(--blue);
    font-weight: 760;
  }

  .member-card .role {
    font-size: 11px;
    font-weight: 800;
    color: var(--purple);
    text-transform: uppercase;
    margin-bottom: 8px;
    display: block;
  }

  .member-card p {
    margin: 0;
    font-size: 12.5px;
    line-height: 1.4;
    color: var(--muted);
  }

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

<div class="eyebrow">AiMY Sales update</div>

# `<span class="gradient-text">`Product Delivery Roadmap & Sprints

<p class="lead">Structured Agile delivery schedule for AiMY Sales: 30 active, planned, and quality-fix tickets mapped to 2-week sprint increments (8-week timeline).</p>

<div class="footer">
  <span>Jira project AIMY - refreshed 10 June 2026</span>
  <span>01</span>
</div>

---

<div class="brand">
  <img src="../../../aimy-catalogue-site/FlairsTech-logo.svg" alt="FlairsTech logo" />
  <span>FlairsTech</span>
</div>

<div class="eyebrow">Agile Velocity</div>

## Mapped Sprints & Release Plan Summary

<p class="lead">30 unique Jira tickets mapped across 4 logical sprints. Focused on testing first, completing active features second, stabilizing quality third, and launching dashboards fourth.</p>

<div class="kpi-grid">
  <div class="kpi">
    <strong class="gradient-text">Sprint 1</strong>
    <span>Testing & Early Release</span>
    <em>8 Tickets (W1-2)</em>
  </div>
  <div class="kpi">
    <strong class="gradient-text" style="background: linear-gradient(135deg, var(--light-blue), var(--purple)); -webkit-background-clip: text; color: transparent;">Sprint 2</strong>
    <span>Core Development</span>
    <em>8 Tickets (W3-4)</em>
  </div>
  <div class="kpi">
    <strong class="gradient-text" style="background: linear-gradient(135deg, var(--blue), var(--cyan)); -webkit-background-clip: text; color: transparent;">Sprint 3</strong>
    <span>Quality Stabilization</span>
    <em>7 Tickets (W5-6)</em>
  </div>
  <div class="kpi">
    <strong class="gradient-text" style="background: linear-gradient(135deg, var(--cyan), var(--success)); -webkit-background-clip: text; color: transparent;">Sprint 4</strong>
    <span>Dashboards & CRM Sync</span>
    <em>7 Tickets (W7-8)</em>
  </div>
</div>

<div class="footer">
  <span>Agile Delivery Roadmap - 8-Week Timeline</span>
  <span>02</span>
</div>

---

<div class="brand">
  <img src="../../../aimy-catalogue-site/FlairsTech-logo.svg" alt="FlairsTech logo" />
  <span>FlairsTech</span>
</div>

<div class="eyebrow">Sprint 1 (Weeks 1-2)</div>

## Sprint 1: Testing & Early Release Validation

<div class="grid-2">
  <div class="side-panel">
    <h3>Focus Area</h3>
    <p>Validating ready-to-test components, confirming LinkedIn integration pipelines, and running UAT checks on the redesigned client interface.</p>
    <div class="stat-highlight">
      <span>Sprint Scope</span>
      <strong>8 Tickets</strong>
    </div>
    <div class="stat-highlight" style="margin-top: 10px;">
      <span>Target Timeline</span>
      <span style="font-weight: 700; font-size: 14px; color: var(--purple);">June 10 - June 24</span>
    </div>
  </div>

<div class="ticket-list">
    <div class="ticket-card">
      <div class="ticket-header">
        <span class="ticket-id">AIMY-45</span>
        <span class="badge uat">UAT</span>
      </div>
      <div class="ticket-title">New AiMY Sales Visual Design</div>
      <p class="ticket-desc">Complete visual redesign of the sales layout, menu structures, and page hierarchy for BDRs.</p>
      <span class="ticket-owner">Engy Yasser</span>
    </div>
    <div class="ticket-card">
      <div class="ticket-header">
        <span class="ticket-id">AIMY-182</span>
        <span class="badge rft">Ready For Testing</span>
      </div>
      <div class="ticket-title">Enhanced Prospect Search (Exa + Apollo)</div>
      <p class="ticket-desc">Combines two search data providers into a single UI view for BDR outreach lists.</p>
      <span class="ticket-owner">Menna Mostafa</span>
    </div>
    <div class="ticket-card">
      <div class="ticket-header">
        <span class="ticket-id">AIMY-225 & AIMY-224</span>
        <span class="badge rft">Ready For Testing</span>
      </div>
      <div class="ticket-title">Job Search & LinkedIn Hiring Signal Integration</div>
      <p class="ticket-desc">Auto-surface companies posting hiring needs directly on LinkedIn as target leads.</p>
      <span class="ticket-owner">Menna Mostafa</span>
    </div>
  </div>
</div>

<div class="footer">
  <span>UAT and Quality Assurance of Ready Codebases</span>
  <span>03</span>
</div>

---

<div class="brand">
  <img src="../../../aimy-catalogue-site/FlairsTech-logo.svg" alt="FlairsTech logo" />
  <span>FlairsTech</span>
</div>

<div class="eyebrow">Sprint 2 (Weeks 3-4)</div>

## Sprint 2: Core Feature & Business Logic Development

<div class="grid-2">
  <div class="side-panel">
    <h3>Focus Area</h3>
    <p>Finishing development and conducting reviews for BDR workflow logic, lead routing, and manager recording review screens.</p>
    <div class="stat-highlight">
      <span>Sprint Scope</span>
      <strong>8 Tickets</strong>
    </div>
    <div class="stat-highlight" style="margin-top: 10px;">
      <span>Target Timeline</span>
      <span style="font-weight: 700; font-size: 14px; color: var(--purple);">June 24 - July 08</span>
    </div>
  </div>

<div class="ticket-list">
    <div class="ticket-card">
      <div class="ticket-header">
        <span class="ticket-id">AIMY-202</span>
        <span class="badge ip">In Progress</span>
      </div>
      <div class="ticket-title">Manager Access to Call Recordings</div>
      <p class="ticket-desc">Enables sales managers to listen to BDR conversations directly in the portal for coaching.</p>
      <span class="ticket-owner">Omar Nawar</span>
    </div>
    <div class="ticket-card">
      <div class="ticket-header">
        <span class="ticket-id">AIMY-194</span>
        <span class="badge ip">In Progress</span>
      </div>
      <div class="ticket-title">Contact List Assignment to BDRs</div>
      <p class="ticket-desc">Distribute outbound lists to team members evenly based on individual workloads.</p>
      <span class="ticket-owner">Menna Mostafa</span>
    </div>
    <div class="ticket-card">
      <div class="ticket-header">
        <span class="ticket-id">AIMY-184</span>
        <span class="badge ip">In Progress</span>
      </div>
      <div class="ticket-title">AI Meeting Booking Prompt During Live Calls</div>
      <p class="ticket-desc">Real-time prompt listening for buyer commitment indicators to schedule meetings immediately.</p>
      <span class="ticket-owner">Khaled Sherif</span>
    </div>
  </div>
</div>

<div class="footer">
  <span>Development of active backlog and code review features</span>
  <span>04</span>
</div>

---

<div class="brand">
  <img src="../../../aimy-catalogue-site/FlairsTech-logo.svg" alt="FlairsTech logo" />
  <span>FlairsTech</span>
</div>

<div class="eyebrow">Sprint 3 (Weeks 5-6)</div>

## Sprint 3: Quality Stabilization & Bug Fixing

<div class="grid-2">
  <div class="side-panel">
    <h3>Focus Area</h3>
    <p>Eliminating data saving bugs, correcting table sorting and layouts, and deploying push-notification fixes to prevent data credit leaks.</p>
    <div class="stat-highlight">
      <span>Sprint Scope</span>
      <strong>7 Tickets</strong>
    </div>
    <div class="stat-highlight" style="margin-top: 10px;">
      <span>Target Timeline</span>
      <span style="font-weight: 700; font-size: 14px; color: var(--purple);">July 08 - July 22</span>
    </div>
  </div>

<div class="ticket-list">
    <div class="ticket-card">
      <div class="ticket-header">
        <span class="ticket-id">AIMY-476 & AIMY-464</span>
        <span class="badge qf">Quality Fix</span>
      </div>
      <div class="ticket-title">Telephone Number Lookup & Storing Fixes</div>
      <p class="ticket-desc">Saves prospect numbers to prevent credit-wasting re-lookups and fixes mismatched data maps.</p>
      <span class="ticket-owner">Fadia Ghareeb</span>
    </div>
    <div class="ticket-card">
      <div class="ticket-header">
        <span class="ticket-id">AIMY-486 & AIMY-488</span>
        <span class="badge qf">Quality Fix</span>
      </div>
      <div class="ticket-title">In-App Notifications & Chat History Persistence</div>
      <p class="ticket-desc">Restores missing action notifications on-screen and prevents first messages from disappearing.</p>
      <span class="ticket-owner">Apdo Nasser / Mohamed Nabil</span>
    </div>
    <div class="ticket-card">
      <div class="ticket-header">
        <span class="ticket-id">AIMY-511 & AIMY-512</span>
        <span class="badge qf">Quality Fix</span>
      </div>
      <div class="ticket-title">Company Size Column Mapping & Sorting Fixes</div>
      <p class="ticket-desc">Fixes headcount table columns showing URLs and corrects ascending/descending sorting.</p>
      <span class="ticket-owner">Unassigned</span>
    </div>
  </div>
</div>

<div class="footer">
  <span>System stabilization, sorting corrections, and performance validation</span>
  <span>05</span>
</div>

---

<div class="brand">
  <img src="../../../aimy-catalogue-site/FlairsTech-logo.svg" alt="FlairsTech logo" />
  <span>FlairsTech</span>
</div>

<div class="eyebrow">Sprint 4 (Weeks 7-8)</div>

## Sprint 4: Dashboards & Salesforce CRM Integration

<div class="grid-2">
  <div class="side-panel">
    <h3>Focus Area</h3>
    <p>Constructing visual panels for managers and sales supervisors, enabling budget tracking, and validating production CRM synchronization.</p>
    <div class="stat-highlight">
      <span>Sprint Scope</span>
      <strong>7 Tickets</strong>
    </div>
    <div class="stat-highlight" style="margin-top: 10px;">
      <span>Target Timeline</span>
      <span style="font-weight: 700; font-size: 14px; color: var(--purple);">July 22 - Aug 05</span>
    </div>
  </div>

<div class="ticket-list">
    <div class="ticket-card">
      <div class="ticket-header">
        <span class="ticket-id">AIMY-520 & AIMY-192</span>
        <span class="badge pl">Planned</span>
      </div>
      <div class="ticket-title">Operations Hub BDR Dashboard & Outcome Strips</div>
      <p class="ticket-desc">High-visibility tracking screens for managers showing daily dials, meetings, and active logs.</p>
      <span class="ticket-owner">Mariam Galal / Apdo Nasser</span>
    </div>
    <div class="ticket-card">
      <div class="ticket-header">
        <span class="ticket-id">AIMY-57 & AIMY-5</span>
        <span class="badge pl">Planned</span>
      </div>
      <div class="ticket-title">Salesforce Ticket Status Sync & Integration Validation</div>
      <p class="ticket-desc">Bi-directional status sync between AiMY and Salesforce; validated live in production.</p>
      <span class="ticket-owner">Habeba Kamel / Unassigned</span>
    </div>
    <div class="ticket-card">
      <div class="ticket-header">
        <span class="ticket-id">AIMY-206</span>
        <span class="badge pl">Planned</span>
      </div>
      <div class="ticket-title">Usage & Cost Tracking per BDR</div>
      <p class="ticket-desc">Detailed logs of lookup requests and APIs per BDR to monitor credit budgets.</p>
      <span class="ticket-owner">Mohammed Hany Shokry</span>
    </div>
  </div>
</div>

<div class="footer">
  <span>Net-new planned dashboard capabilities and final Salesforce release</span>
  <span>06</span>
</div>

---

<div class="brand">
  <img src="../../../aimy-catalogue-site/FlairsTech-logo.svg" alt="FlairsTech logo" />
  <span>FlairsTech</span>
</div>

<div class="eyebrow">Roadmap Timeline</div>

## Integrated Agile Release Timeline

<table class="sprint-timeline">
  <thead>
    <tr>
      <th>Sprint / Week</th>
      <th>Timeline</th>
      <th>Primary Sprint Focus</th>
      <th>Key Features & Deliverables</th>
      <th>Agile Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Sprint 1</strong> (W 1-2)</td>
      <td>June 10 - June 24</td>
      <td>Testing & Early Release</td>
      <td>Visual design UAT, LinkedIn signals, Apollo/Exa prospect search, call history flags.</td>
      <td><span class="badge rft">Ready / Testing</span></td>
    </tr>
    <tr>
      <td><strong>Sprint 2</strong> (W 3-4)</td>
      <td>June 24 - July 08</td>
      <td>Core Workflow Build</td>
      <td>Manager call recordings playback, list workloads, AI booking prompts, live call stats.</td>
      <td><span class="badge ip">Development</span></td>
    </tr>
    <tr>
      <td><strong>Sprint 3</strong> (W 5-6)</td>
      <td>July 08 - July 22</td>
      <td>Quality & Stabilization</td>
      <td>Save phone numbers fix, app notifications, chat history, headcounts, blocker checks.</td>
      <td><span class="badge qf">Stabilization</span></td>
    </tr>
    <tr>
      <td><strong>Sprint 4</strong> (W 7-8)</td>
      <td>July 22 - Aug 05</td>
      <td>Operations & CRM Sync</td>
      <td>Manager Operations Hub screens, outcomes strip, Salesforce bi-sync, BDR billing.</td>
      <td><span class="badge pl">Planned</span></td>
    </tr>
  </tbody>
</table>

<div class="footer">
  <span>Each cycle includes 2 weeks of development, testing, and progressive release</span>
  <span>07</span>
</div>

---

<div class="brand">
  <img src="../../../aimy-catalogue-site/FlairsTech-logo.svg" alt="FlairsTech logo" />
  <span>FlairsTech</span>
</div>

<div class="eyebrow">Agile Team</div>

## Resource Allocation & Feature Ownership

<div class="grid-3">
  <div class="member-card">
    <h3>Menna Mostafa</h3>
    <span class="role">Lead Search & Filter</span>
    <p>Responsible for prospect filters, bulk generation, LinkedIn integration, and prospect flags (8 tickets, S1-S2 focus).</p>
  </div>
  <div class="member-card">
    <h3>Khaled Sherif</h3>
    <span class="role">Call Logic Developer</span>
    <p>Implements decision maker tickboxes, AI booking prompts, and hung up duration markers (3 tickets, S1-S2 focus).</p>
  </div>
  <div class="member-card">
    <h3>Apdo Nasser</h3>
    <span class="role">Operations Hub Dev</span>
    <p>Owns real-time statistics cards, message history logs, and manager outcomes strip (3 tickets, S2-S4 focus).</p>
  </div>
</div>

<div class="grid-3" style="margin-top: 16px;">
  <div class="member-card">
    <h3>Mariam / Omar</h3>
    <span class="role">UX & Recordings</span>
    <p>Implement core frontend UI changes, recordings playback access, and Operations Hub dashboards (3 tickets).</p>
  </div>
  <div class="member-card">
    <h3>Fadia / Nabil</h3>
    <span class="role">CRM & Phone Integr.</span>
    <p>Deliver phone number caching, notifications, and phone requests (AIMY-268 blocked ticket) (4 tickets).</p>
  </div>
  <div class="member-card">
    <h3>Quality / PM (Unassigned)</h3>
    <span class="role">Roadmap Support</span>
    <p>Covering Salesforce validations, web scanning tests (Habeba, Hany), and unassigned status syncs (9 tickets).</p>
  </div>
</div>

<div class="footer">
  <span>Workloads aligned to specific expertise: Search, Calling UI, and Manager Operations</span>
  <span>08</span>
</div>
