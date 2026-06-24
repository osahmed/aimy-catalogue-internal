---
marp: true
theme: default
size: 16:9
paginate: false
html: true
title: FlairsTech AI-Enabled CX & AIMY-Powered BDR Commercial Model
description: B2B Commercial Model Strategy styled with official FlairsTech Brand Guidelines.
---

<style>
  @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800;900&display=swap');

  :root {
    --purple: #8c4ff4;
    --blue: #0066ff;
    --light-blue: #5582ff;
    --cyan: #6fdfe2;
    --lavender: #b0c1ff;
    --periwinkle: #8d98ff;
    --ink: #111827;
    --muted: #667085;
    --line: #e5e7eb;
    --soft: #f6f8ff;
    --white: #ffffff;
    --success: #087f7a;
  }

  section {
    width: 1280px;
    height: 720px;
    padding: 36px 64px 48px; /* Optimized top/bottom padding to prevent vertical overflow */
    background:
      radial-gradient(circle at 92% 8%, rgba(111, 223, 226, 0.38), transparent 23%),
      radial-gradient(circle at 0% 100%, rgba(140, 79, 244, 0.14), transparent 28%),
      linear-gradient(135deg, #ffffff 0%, #f6f8ff 100%);
    color: var(--ink);
    font-family: "Poppins", Arial, sans-serif;
    letter-spacing: 0;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: stretch;
    box-sizing: border-box;
  }

  section.dark {
    background:
      radial-gradient(circle at 88% 14%, rgba(111, 223, 226, 0.28), transparent 24%),
      linear-gradient(135deg, #101828 0%, #1a1550 48%, #0066ff 130%);
    color: var(--white);
    justify-content: center;
    align-items: center;
    padding: 0;
  }

  h1, h2, h3, p {
    letter-spacing: 0;
    margin: 0;
  }

  h1 {
    font-size: 44px;
    line-height: 1.1;
    font-weight: 800;
    color: var(--white);
    margin-bottom: 8px;
  }

  h2 {
    font-size: 30px; /* Sized down slightly from 32px for elegance */
    line-height: 1.1;
    font-weight: 800;
    color: var(--blue);
  }

  h3 {
    font-size: 16px; /* Sized down slightly from 18px */
    font-weight: 700;
    color: var(--ink);
  }

  p {
    font-size: 14px; /* Sized down from 14.5px */
    line-height: 1.4;
    color: var(--muted);
  }

  section.dark p {
    color: rgba(255, 255, 255, 0.8);
  }

  .brand {
    position: absolute;
    top: 32px;
    left: 64px;
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 14px;
    font-weight: 700;
    color: inherit;
  }

  .brand > img {
    width: 28px !important;
    height: 28px !important;
    max-width: 28px !important;
    max-height: 28px !important;
    object-fit: contain;
  }

  .eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    margin-top: 10px; /* Reduced from 30px to save space */
    margin-bottom: 4px; /* Reduced from 6px */
    font-size: 11px;
    font-weight: 800;
    text-transform: uppercase;
    color: var(--blue);
  }

  .eyebrow::before {
    content: "";
    width: 9px;
    height: 9px;
    border-radius: 2.5px;
    background: linear-gradient(135deg, var(--purple), var(--blue));
  }

  section.dark .eyebrow {
    color: var(--cyan);
    margin-top: 0;
  }

  .gradient-text {
    background: linear-gradient(135deg, var(--purple), var(--blue));
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
  }

  .lead {
    font-size: 14.5px;
    line-height: 1.35;
    color: var(--muted);
    margin-bottom: 6px;
    max-width: 980px;
  }

  /* Cover Slide */
  .intro-brand {
    display: flex;
    align-items: center;
    gap: 40px;
    width: 86%;
    max-width: 960px;
    z-index: 5;
    text-align: left;
  }

  .intro-logo-wrap {
    width: 160px;
    filter: drop-shadow(0 15px 30px rgba(0,0,0,0.3));
  }

  .intro-logo-wrap img {
    width: 100%;
    display: block;
  }

  .intro-copy {
    color: var(--white);
  }

  .intro-copy p {
    font-size: 17px;
    font-weight: 700;
    color: rgba(255, 255, 255, 0.85);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 4px;
  }

  /* Grids and Cards */
  .grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-top: 4px;
  }

  .grid-3 {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-top: 4px;
  }

  .card {
    background: var(--white);
    border: 1px solid var(--line);
    border-radius: 10px;
    padding: 12px 16px;
    box-shadow: 0 4px 12px rgba(16, 24, 40, 0.02);
  }

  .card h3 {
    font-size: 16px;
    color: var(--blue);
    font-weight: 800;
    margin-bottom: 2px;
  }

  .card p {
    font-size: 12.5px;
    line-height: 1.3;
    color: var(--muted);
  }

  .card strong {
    color: var(--ink);
    font-weight: 700;
  }

  /* Side-by-side tables row */
  .tables-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-top: 4px;
  }

  .tables-row table {
    margin-top: 0;
  }

  /* cost-table-card wrapping the tables */
  .cost-table-card {
    background: var(--white);
    border: 1px solid var(--line);
    border-radius: 10px;
    padding: 10px 12px;
    box-shadow: 0 4px 12px rgba(16, 24, 40, 0.02);
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
  }

  .cost-table-card h3 {
    font-size: 13.5px;
    color: var(--blue);
    font-weight: 800;
    margin-bottom: 4px;
  }

  /* Global Table System */
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 4px;
    margin-bottom: 0;
    font-size: 10.5px; /* Compact executive size */
    background: var(--white);
    border: 1px solid var(--line);
    border-radius: 6px;
    overflow: hidden;
    table-layout: fixed;
  }

  th {
    background: linear-gradient(135deg, var(--purple), var(--blue));
    color: var(--white);
    padding: 4px 6px;
    font-weight: 700;
    font-size: 9.5px;
    text-transform: uppercase;
    text-align: left;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-sizing: border-box;
    height: 24px;
  }

  td {
    padding: 4px 6px;
    border: 1px solid var(--line);
    color: var(--ink);
    font-weight: 600;
    line-height: 1.2;
    word-break: break-word;
    overflow-wrap: break-word;
    vertical-align: middle;
    box-sizing: border-box;
    height: 25px; /* Enforces consistent row height */
  }

  tr:nth-child(even) td {
    background: var(--soft);
  }

  td strong {
    font-weight: 800;
    color: var(--blue);
  }

  tr.highlight-row td {
    background: #eef4ff !important;
    font-weight: 700;
  }

  tr.highlight-row td strong {
    color: var(--purple);
  }

  tr.total-row td {
    background: var(--ink) !important;
    color: var(--white) !important;
    font-weight: 700;
  }

  tr.total-row td:last-child {
    color: var(--cyan) !important;
  }

  .green {
    color: var(--success) !important;
    font-weight: 700;
  }

  /* Pricing specific cards */
  .kpi-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    margin-top: 2px;
    margin-bottom: 4px;
  }

  .kpi-card {
    background: var(--white);
    border: 1px solid var(--line);
    border-radius: 8px;
    padding: 6px 10px;
    text-align: center;
    box-shadow: 0 4px 12px rgba(16, 24, 40, 0.01);
  }

  .kpi-card small {
    display: block;
    font-size: 8px;
    font-weight: 800;
    text-transform: uppercase;
    color: var(--muted);
    letter-spacing: 0.5px;
    margin-bottom: 1px;
  }

  .kpi-card b {
    display: block;
    font-size: 14.5px;
    font-weight: 800;
    color: var(--purple);
  }

  /* Cover Slide stats */
  .cover-kpis {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    width: 86%;
    max-width: 960px;
    margin-top: 30px;
    z-index: 5;
  }

  .cover-kpi {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 12px;
    padding: 14px;
    text-align: center;
    backdrop-filter: blur(10px);
  }

  .cover-kpi strong {
    display: block;
    font-size: 24px;
    font-weight: 800;
    color: var(--cyan);
    margin-bottom: 4px;
  }

  .cover-kpi span {
    display: block;
    font-size: 10.5px;
    color: rgba(255, 255, 255, 0.8);
    font-weight: 600;
  }

  /* Cost Analysis details */
  .cost-kpis {
    display: grid;
    grid-template-columns: 1fr;
    gap: 6px;
  }

  .cost-kpi {
    background: var(--white);
    border: 1px solid var(--line);
    border-radius: 10px;
    padding: 8px 14px;
    box-shadow: 0 10px 24px rgba(16, 24, 40, 0.02);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .cost-kpi small {
    font-size: 9.5px;
    font-weight: 800;
    color: var(--muted);
    text-transform: uppercase;
  }

  .cost-kpi b {
    font-size: 18px;
    font-weight: 800;
    color: var(--blue);
  }

  .cost-kpi b.positive {
    color: var(--purple);
  }

  /* Performance Grid */
  .perf-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-top: 24px;
  }

  .perf-card {
    background: var(--white);
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 10px 30px rgba(16, 24, 40, 0.03);
    text-align: center;
  }

  .perf-card small {
    display: block;
    font-size: 10.5px;
    font-weight: 800;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 4px;
  }

  .perf-card b {
    display: block;
    font-size: 30px;
    font-weight: 800;
    color: var(--purple);
    margin-bottom: 4px;
  }

  .perf-card span {
    display: block;
    font-size: 11px;
    color: var(--muted);
    font-weight: 600;
  }

  /* Footer layout */
  .footer {
    position: absolute;
    left: 64px;
    right: 64px;
    bottom: 20px;
    display: flex;
    justify-content: space-between;
    color: var(--muted);
    font-size: 10px;
    font-weight: 700;
    border-top: 1px solid var(--line);
    padding-top: 6px;
  }

  section.dark .footer {
    color: rgba(255, 255, 255, 0.6);
    border-top: 1px solid rgba(255, 255, 255, 0.15);
  }
</style>


<!-- _class: dark -->

<div class="brand">
  <img src="assets/logo.svg" alt="FlairsTech logo" />
  <span>FlairsTech</span>
</div>

<div class="intro-brand">
  <div class="intro-logo-wrap">
    <img src="assets/logo.svg" alt="FlairsTech logo">
  </div>
  <div class="intro-copy">
    <div class="eyebrow">Internal Commercial Model</div>
    <h1>From managed services to<br><span class="gradient-text">AI-enabled operating models.</span></h1>
    <p>This model turns AI from a loose capability into a priced commercial structure across CX and BDR.</p>
  </div>
</div>

<div class="cover-kpis">
  <div class="cover-kpi">
    <strong>35–40%</strong>
    <span>Baseline margin target</span>
  </div>
  <div class="cover-kpi">
    <strong>+25%</strong>
    <span>AI-Enabled CX target uplift</span>
  </div>
  <div class="cover-kpi">
    <strong>+30%</strong>
    <span>AIMY-Powered BDR target uplift</span>
  </div>
  <div class="cover-kpi">
    <strong>40–65%</strong>
    <span>AI-first entry margin target</span>
  </div>
</div>

<div class="footer">
  <span>AI Commercial Model Strategy</span>
  <span>01</span>
</div>

---

<div class="brand">
  <img src="assets/logo.svg" alt="FlairsTech logo" />
  <span>FlairsTech</span>
</div>

<div class="eyebrow">Commercial Strategy</div>
<h2>The Strategic Story</h2>
<p class="lead">AI does not replace the service model. It changes how the service is packaged, priced, and governed.</p>

<div class="grid-3">
  <div class="card">
    <h3>1 Protect the base</h3>
    <p>Legacy Managed CX and Managed BDR remain available for capacity-led clients and lower AI-maturity accounts.</p>
    <p style="margin-top: 8px; font-size: 12.5px;"><strong>FTE/month pricing</strong><br>35–40% baseline margin<br>Useful fallback, not default</p>
  </div>
  
  <div class="card">
    <h3>2 Upgrade the core</h3>
    <p>AI-Enabled CX and AIMY-Powered BDR add a priced operating layer across QA, coaching, visibility, and governance.</p>
    <p style="margin-top: 8px; font-size: 12.5px;"><strong>CX uplift target: +25%</strong><br><strong>BDR uplift target: +30%</strong><br>Measured through ROI & usage</p>
  </div>
  
  <div class="card">
    <h3>3 Open new doors</h3>
    <p>AI-first entry products give Sales a low-friction way to prove value before a full outsourcing pitch.</p>
    <p style="margin-top: 8px; font-size: 12.5px;"><strong>Fixed project / Pilot fees</strong><br>AI QA Pilot & Diagnostics<br>ICP/List Build & BDR QA</p>
  </div>
</div>

<div class="footer">
  <span>AI Commercial Model Strategy</span>
  <span>02</span>
</div>

---

<div class="brand">
  <img src="assets/logo.svg" alt="FlairsTech logo" />
  <span>FlairsTech</span>
</div>

<div class="eyebrow">Commercial Strategy</div>
<h2>Portfolio Architecture</h2>
<p class="lead">Three commercial routes across two service lines. The model is intentionally not one generic “AI strategy.”</p>

<table>
  <colgroup>
    <col style="width: 15%;">
    <col style="width: 25%;">
    <col style="width: 25%;">
    <col style="width: 15%;">
    <col style="width: 20%;">
  </colgroup>
  <thead>
    <tr>
      <th>Route</th>
      <th>CX offer</th>
      <th>BDR offer</th>
      <th>Pricing logic</th>
      <th>Margin role</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Legacy Managed</strong></td>
      <td>Managed CX</td>
      <td>Managed BDR</td>
      <td>FTE/month</td>
      <td>Protect current base business at 35–40%</td>
    </tr>
    <tr>
      <td><strong>Legacy + AI</strong></td>
      <td>AI-Enabled CX</td>
      <td>AIMY-Powered BDR</td>
      <td>FTE + uplift + setup + capped usage</td>
      <td>Premium managed service and modest margin expansion</td>
    </tr>
    <tr>
      <td><strong>AI First Entry</strong></td>
      <td>AI QA Pilot, Workflow Diagnostic, Knowledge Assessment</td>
      <td>ICP/List Build, Campaign Readiness, BDR QA Pilot</td>
      <td>Fixed project / per unit / pilot</td>
      <td>Door opener and higher-margin add-on revenue</td>
    </tr>
    <tr>
      <td><strong>Expansion</strong></td>
      <td>CX Workflow Automation</td>
      <td>AIMY Growth Engine</td>
      <td>Setup + monthly / usage / hybrid outcome pricing</td>
      <td>Higher margin upside through non-FTE meters</td>
    </tr>
  </tbody>
</table>

<div class="footer">
  <span>AI Commercial Model Strategy</span>
  <span>03</span>
</div>

---

<div class="brand">
  <img src="assets/logo.svg" alt="FlairsTech logo" />
  <span>FlairsTech</span>
</div>

<div class="eyebrow">Financial Model</div>
<h2>Pricing Thesis &amp; Recurring Margin</h2>
<p class="lead">The AI uplift funds a real operating layer. True margin expansion comes from scoped modules and outcome models.</p>

<div class="kpi-row">
  <div class="kpi-card">
    <small>CX Baseline Rate</small>
    <b>$1,600</b>
  </div>
  <div class="kpi-card">
    <small>AI-Enabled CX (+25%)</small>
    <b>$2,000</b>
  </div>
  <div class="kpi-card">
    <small>BDR Baseline Rate</small>
    <b>$2,000</b>
  </div>
  <div class="kpi-card">
    <small>AIMY-Powered BDR (+30%)</small>
    <b>$2,600</b>
  </div>
</div>

<div class="tables-row">
  <div class="cost-table-card">
    <h3>CX Recurring Margin (English L1)</h3>
    <table>
      <colgroup>
        <col style="width: 46%;">
        <col style="width: 27%;">
        <col style="width: 27%;">
      </colgroup>
      <thead>
        <tr>
          <th>Item</th>
          <th>Legacy CX</th>
          <th>AI-Enabled CX</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Monthly price</td>
          <td>$1,600</td>
          <td><strong>$2,000</strong></td>
        </tr>
        <tr>
          <td>Base delivery cost</td>
          <td>$1,000</td>
          <td>$1,000</td>
        </tr>
        <tr>
          <td>AI operating cost</td>
          <td>—</td>
          <td>$175</td>
        </tr>
        <tr class="highlight-row">
          <td>Gross profit</td>
          <td>$600</td>
          <td><strong>$825</strong></td>
        </tr>
        <tr class="highlight-row">
          <td>Gross margin</td>
          <td>37.5%</td>
          <td><strong>41.3%</strong></td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="cost-table-card">
    <h3>BDR Recurring Margin (Standard BDR)</h3>
    <table>
      <colgroup>
        <col style="width: 46%;">
        <col style="width: 27%;">
        <col style="width: 27%;">
      </colgroup>
      <thead>
        <tr>
          <th>Item</th>
          <th>Legacy BDR</th>
          <th>AIMY-Powered BDR</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Monthly price</td>
          <td>$2,000</td>
          <td><strong>$2,600</strong></td>
        </tr>
        <tr>
          <td>Base delivery cost</td>
          <td>$1,250</td>
          <td>$1,250</td>
        </tr>
        <tr>
          <td>AIMY/data/tooling cost</td>
          <td>—</td>
          <td>$300</td>
        </tr>
        <tr class="highlight-row">
          <td>Gross profit</td>
          <td>$750</td>
          <td><strong>$1,050</strong></td>
        </tr>
        <tr class="highlight-row">
          <td>Gross margin</td>
          <td>37.5%</td>
          <td><strong>40.4%</strong></td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

<div class="footer">
  <span>AI Commercial Model Strategy</span>
  <span>04</span>
</div>

---

<div class="brand">
  <img src="assets/logo.svg" alt="FlairsTech logo" />
  <span>FlairsTech</span>
</div>

<div class="eyebrow">Service Offering</div>
<h2>AI-Enabled CX Offering</h2>
<p class="lead">AI improves quality, speed, and visibility. Workflow automation and Voice AI are separate expansion layers.</p>

<div class="grid-3">
  <div class="card">
    <h3>CX Managed</h3>
    <p>Standard delivery for capacity-led opportunities and lower AI-maturity clients.</p>
    <p style="margin-top: 8px; font-size: 12.5px;"><strong>From $1.4K–$1.7K</strong><br>per English L0–L1 FTE<br>Includes Agents, TL, QA, standard training & reporting</p>
  </div>
  
  <div class="card">
    <h3>AI-Enabled CX</h3>
    <p>Managed CX with AI QA, Agent Assist, automatic summaries, Client Pulse, and coaching insights.</p>
    <p style="margin-top: 8px; font-size: 12.5px;"><strong>Target +25% uplift</strong><br>on applicable base rate<br>Usage caps & overage rules apply</p>
  </div>
  
  <div class="card">
    <h3>+ CX Expansion</h3>
    <p>Automation, Voice AI, and diagnostics are priced separately where the workflow justifies it.</p>
    <p style="margin-top: 8px; font-size: 12.5px;"><strong>Typical $10K+ setup</strong><br>Workflow Diagnostic<br>Voice AI priced per minute</p>
  </div>
</div>

<div class="footer">
  <span>AI Commercial Model Strategy</span>
  <span>05</span>
</div>

---

<div class="brand">
  <img src="assets/logo.svg" alt="FlairsTech logo" />
  <span>FlairsTech</span>
</div>

<div class="eyebrow">Service Offering</div>
<h2>AIMY-Powered BDR Offering</h2>
<p class="lead">BDR has stronger productization potential. The AIMY package needs caps on lead volume and QA coverage.</p>

<div class="grid-3">
  <div class="card">
    <h3>Managed BDR</h3>
    <p>Standard BDR capacity for clients that already own the sales motion and mainly need outreach execution.</p>
    <p style="margin-top: 8px; font-size: 12.5px;"><strong>From $1.8K–$2.2K</strong><br>per BDR / month<br>Outreach execution, manager oversight, standard reports</p>
  </div>
  
  <div class="card">
    <h3>AIMY-Powered BDR</h3>
    <p>Managed outbound with AI-supported sourcing, hygiene, guidance, BDR QA, Client Pulse, and CRM handoff.</p>
    <p style="margin-top: 8px; font-size: 12.5px;"><strong>Target +30% uplift</strong><br>on applicable base rate<br>Lead sourcing/hygiene within caps</p>
  </div>
  
  <div class="card">
    <h3>AIMY Growth Engine</h3>
    <p>Premium model for mature campaigns where accepted meetings or SQL outcomes can be clearly defined.</p>
    <p style="margin-top: 8px; font-size: 12.5px;"><strong>Hybrid Pricing</strong><br>Base rate + meeting/SQL fee<br>Requires clear ICP & rules</p>
  </div>
</div>

<div class="footer">
  <span>AI Commercial Model Strategy</span>
  <span>06</span>
</div>

---

<div class="brand">
  <img src="assets/logo.svg" alt="FlairsTech logo" />
  <span>FlairsTech</span>
</div>

<div class="eyebrow">Financial Model</div>
<h2>Bundled vs Standalone Module Allocations</h2>
<p class="lead">Bundled modules share the managed service infrastructure. The package only works if total cost stays inside the uplift.</p>

<div class="tables-row">
  <div class="cost-table-card">
    <h3>CX Bundled Module Allocation</h3>
    <table>
      <colgroup>
        <col style="width: 38%;">
        <col style="width: 22%;">
        <col style="width: 20%;">
        <col style="width: 20%;">
      </colgroup>
      <thead>
        <tr>
          <th>Module</th>
          <th>Standalone</th>
          <th>Bundled</th>
          <th>Cost</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>AI QA & Coaching</td>
          <td>$150/FTE</td>
          <td><strong>$85/FTE</strong></td>
          <td>$35–$60</td>
        </tr>
        <tr>
          <td>Agent Assist Copilot</td>
          <td>$125/FTE</td>
          <td><strong>$75/FTE</strong></td>
          <td>$35–$60</td>
        </tr>
        <tr>
          <td>Case Summaries</td>
          <td>$50/FTE</td>
          <td><strong>$25/FTE</strong></td>
          <td>$10–$20</td>
        </tr>
        <tr>
          <td>Client Pulse</td>
          <td>Bundled</td>
          <td><strong>$25/FTE eq.</strong></td>
          <td>$10–$20</td>
        </tr>
        <tr>
          <td>Governance / Insights</td>
          <td>$50–$100</td>
          <td><strong>$35/FTE</strong></td>
          <td>$20–$35</td>
        </tr>
        <tr class="highlight-row">
          <td>Total</td>
          <td>—</td>
          <td><strong>$245/FTE</strong></td>
          <td class="green">$110–$195</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="cost-table-card">
    <h3>BDR Bundled Module Allocation</h3>
    <table>
      <colgroup>
        <col style="width: 38%;">
        <col style="width: 22%;">
        <col style="width: 20%;">
        <col style="width: 20%;">
      </colgroup>
      <thead>
        <tr>
          <th>Module</th>
          <th>Standalone</th>
          <th>Bundled</th>
          <th>Cost</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Lead Sourcing + Hygiene</td>
          <td>$2k–$10k</td>
          <td><strong>$150/BDR</strong></td>
          <td>$80–$150</td>
        </tr>
        <tr>
          <td>Sales Guidance</td>
          <td>$2k–$7k</td>
          <td><strong>$75/BDR</strong></td>
          <td>$25–$50</td>
        </tr>
        <tr>
          <td>BDR QA & Coaching</td>
          <td>$200/BDR</td>
          <td><strong>$110/BDR</strong></td>
          <td>$50–$90</td>
        </tr>
        <tr>
          <td>Client Pulse</td>
          <td>Bundled</td>
          <td><strong>$50/BDR eq.</strong></td>
          <td>$20–$40</td>
        </tr>
        <tr>
          <td>Funnel Gov + Handoff</td>
          <td>$100–$200</td>
          <td><strong>$90/BDR</strong></td>
          <td>$50–$80</td>
        </tr>
        <tr class="highlight-row">
          <td>Total</td>
          <td>—</td>
          <td><strong>$475/BDR</strong></td>
          <td class="green">$225–$410</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

<div class="footer">
  <span>AI Commercial Model Strategy</span>
  <span>07</span>
</div>

---

<div class="brand">
  <img src="assets/logo.svg" alt="FlairsTech logo" />
  <span>FlairsTech</span>
</div>

<div class="eyebrow">Commercial Model</div>
<h2>CX Legacy Level Card by Language</h2>
<p class="lead">Standard CX pricing starts from the English card. L5 remains unscaled as an operations/governance role.</p>

<table>
  <colgroup>
    <col style="width: 16%;">
    <col style="width: 21%;">
    <col style="width: 21%;">
    <col style="width: 21%;">
    <col style="width: 21%;">
  </colgroup>
  <thead>
    <tr>
      <th>Level</th>
      <th>English</th>
      <th>French</th>
      <th>Spanish / Italian</th>
      <th>German / Dutch</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>L0</strong></td>
      <td>$1,400–$1,600</td>
      <td>$1,575–$1,800</td>
      <td>$1,750–$2,000</td>
      <td>$1,925–$2,200</td>
    </tr>
    <tr>
      <td><strong>L1</strong></td>
      <td>$1,600–$1,700</td>
      <td>$1,800–$1,913</td>
      <td>$2,000–$2,125</td>
      <td>$2,200–$2,338</td>
    </tr>
    <tr>
      <td><strong>L2</strong></td>
      <td>$1,800–$2,000</td>
      <td>$2,025–$2,250</td>
      <td>$2,250–$2,500</td>
      <td>$2,475–$2,750</td>
    </tr>
    <tr>
      <td><strong>L3</strong></td>
      <td>$2,300–$2,500</td>
      <td>$2,588–$2,813</td>
      <td>$2,875–$3,125</td>
      <td>$3,163–$3,438</td>
    </tr>
    <tr>
      <td><strong>L4</strong></td>
      <td>$2,500–$2,800</td>
      <td>$2,813–$3,150</td>
      <td>$3,125–$3,500</td>
      <td>$3,438–$3,850</td>
    </tr>
    <tr class="highlight-row">
      <td><strong>L5 (Ops Mgr)</strong></td>
      <td>$3,000–$4,000</td>
      <td>$3,000–$4,000</td>
      <td>$3,000–$4,000</td>
      <td>$3,000–$4,000</td>
    </tr>
  </tbody>
</table>

<div class="footer">
  <span>AI Commercial Model Strategy</span>
  <span>08</span>
</div>

---

<div class="brand">
  <img src="assets/logo.svg" alt="FlairsTech logo" />
  <span>FlairsTech</span>
</div>

<div class="eyebrow">Commercial Model</div>
<h2>CX AI-Enabled Level Card (+25% Uplift)</h2>
<p class="lead">+25% applied to applicable legacy rate. Usage caps and overage rules required.</p>

<table>
  <colgroup>
    <col style="width: 16%;">
    <col style="width: 21%;">
    <col style="width: 21%;">
    <col style="width: 21%;">
    <col style="width: 21%;">
  </colgroup>
  <thead>
    <tr>
      <th>Level</th>
      <th>English</th>
      <th>French</th>
      <th>Spanish / Italian</th>
      <th>German / Dutch</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>L0</strong></td>
      <td>$1,750–$2,000</td>
      <td>$1,969–$2,250</td>
      <td>$2,188–$2,500</td>
      <td>$2,406–$2,750</td>
    </tr>
    <tr>
      <td><strong>L1</strong></td>
      <td>$2,000–$2,125</td>
      <td>$2,250–$2,391</td>
      <td>$2,500–$2,656</td>
      <td>$2,750–$2,922</td>
    </tr>
    <tr>
      <td><strong>L2</strong></td>
      <td>$2,250–$2,500</td>
      <td>$2,531–$2,813</td>
      <td>$2,813–$3,125</td>
      <td>$3,094–$3,438</td>
    </tr>
    <tr>
      <td><strong>L3</strong></td>
      <td>$2,875–$3,125</td>
      <td>$3,234–$3,516</td>
      <td>$3,594–$3,906</td>
      <td>$3,953–$4,297</td>
    </tr>
    <tr>
      <td><strong>L4</strong></td>
      <td>$3,125–$3,500</td>
      <td>$3,516–$3,938</td>
      <td>$3,906–$4,375</td>
      <td>$4,297–$4,813</td>
    </tr>
    <tr class="highlight-row">
      <td><strong>L5 (Ops Mgr)</strong></td>
      <td>$3,750–$5,000</td>
      <td>$3,750–$5,000</td>
      <td>$3,750–$5,000</td>
      <td>$3,750–$5,000</td>
    </tr>
  </tbody>
</table>

<div class="footer">
  <span>AI Commercial Model Strategy</span>
  <span>09</span>
</div>

---

<div class="brand">
  <img src="assets/logo.svg" alt="FlairsTech logo" />
  <span>FlairsTech</span>
</div>

<div class="eyebrow">Commercial Model</div>
<h2>CX Criteria &amp; BDR Level Card (+30% Uplift)</h2>
<p class="lead">How we classify CX work levels, alongside BDR legacy and AIMY-powered level cards.</p>

<div class="tables-row">
  <div class="cost-table-card">
    <h3>CX Criteria</h3>
    <table>
      <colgroup>
        <col style="width: 12%;">
        <col style="width: 88%;">
      </colgroup>
      <thead>
        <tr>
          <th>Lvl</th>
          <th>CX Criteria</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><b>L0</b></td>
          <td>Basic back office, tagging, simple updates, low judgment</td>
        </tr>
        <tr>
          <td><b>L1</b></td>
          <td>Standard customer handling with clear SOPs and escalation</td>
        </tr>
        <tr>
          <td><b>L2</b></td>
          <td>Senior handling, exceptions, refunds, complaints, multi-system</td>
        </tr>
        <tr>
          <td><b>L3</b></td>
          <td>QA, SME, training, calibration, knowledge maintenance</td>
        </tr>
        <tr>
          <td><b>L4</b></td>
          <td>Team lead / supervisor, coaching, queue & escalation control</td>
        </tr>
        <tr>
          <td><b>L5</b></td>
          <td>Ops manager, account governance, AI adoption roadmap</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="cost-table-card">
    <h3>BDR Level Card</h3>
    <table>
      <colgroup>
        <col style="width: 10%;">
        <col style="width: 42%;">
        <col style="width: 24%;">
        <col style="width: 24%;">
      </colgroup>
      <thead>
        <tr>
          <th>Lvl</th>
          <th>Function</th>
          <th>Legacy</th>
          <th>AIMY +30%</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><b>L0</b></td>
          <td>Research / Hygiene</td>
          <td>$1.3K–$1.8K</td>
          <td><strong>$1.7K–$2.3K</strong></td>
        </tr>
        <tr>
          <td><b>L1</b></td>
          <td>Standard BDR</td>
          <td>$1.8K–$2.2K</td>
          <td><strong>$2.3K–$2.9K</strong></td>
        </tr>
        <tr>
          <td><b>L2</b></td>
          <td>Senior / Multilingual</td>
          <td>$2.2K–$2.8K</td>
          <td><strong>$2.9K–$3.6K</strong></td>
        </tr>
        <tr>
          <td><b>L3</b></td>
          <td>BDR TL / QA</td>
          <td>$3.0K–$3.8K</td>
          <td><strong>$3.9K–$4.9K</strong></td>
        </tr>
        <tr>
          <td><b>L4</b></td>
          <td>BDR Manager</td>
          <td>$4.0K–$5.0K</td>
          <td><strong>$5.2K–$6.5K</strong></td>
        </tr>
        <tr>
          <td><b>L5</b></td>
          <td>AIMY Growth Cons.</td>
          <td>$5.0K–$7.0K</td>
          <td><strong>$6.5K–$9.1K</strong></td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

<div class="footer">
  <span>AI Commercial Model Strategy</span>
  <span>10</span>
</div>

---

<div class="brand">
  <img src="assets/logo.svg" alt="FlairsTech logo" />
  <span>FlairsTech</span>
</div>

<div class="eyebrow">Value Proposition</div>
<h2>Client ROI &amp; Value Cases</h2>
<p class="lead">The premium must be justified through measurable operating value. ROI reviewed after 90 days.</p>

<div class="tables-row">
  <div class="cost-table-card">
    <h3>CX Value Case (20-FTE, +$8k/mo premium)</h3>
    <table>
      <colgroup>
        <col style="width: 72%;">
        <col style="width: 28%;">
      </colgroup>
      <thead>
        <tr>
          <th>Metric</th>
          <th>Target range</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Productivity / capacity</td>
          <td class="green">10–15%</td>
        </tr>
        <tr>
          <td>AHT reduction</td>
          <td class="green">8–15%</td>
        </tr>
        <tr>
          <td>Wrap-up reduction</td>
          <td class="green">15–30%</td>
        </tr>
        <tr>
          <td>QA coverage expansion</td>
          <td class="green">5–10x</td>
        </tr>
        <tr>
          <td>Rework / recontact reduction</td>
          <td class="green">5–10%</td>
        </tr>
        <tr>
          <td>Ramp improvement</td>
          <td class="green">10–20%</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="cost-table-card">
    <h3>BDR Value Case (5-BDR, +$3k/mo premium)</h3>
    <table>
      <colgroup>
        <col style="width: 72%;">
        <col style="width: 28%;">
      </colgroup>
      <thead>
        <tr>
          <th>Metric</th>
          <th>Target range</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Bad-fit lead waste reduction</td>
          <td class="green">10–20%</td>
        </tr>
        <tr>
          <td>Lead coverage improvement</td>
          <td class="green">10–15%</td>
        </tr>
        <tr>
          <td>Engagement relative uplift</td>
          <td class="green">5–10%</td>
        </tr>
        <tr>
          <td>Accepted meeting quality uplift</td>
          <td class="green">5–10%</td>
        </tr>
        <tr>
          <td>BDR ramp/coaching improvement</td>
          <td class="green">10–20%</td>
        </tr>
        <tr>
          <td>Handoff leakage reduction</td>
          <td class="green">5–10%</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

<div class="footer">
  <span>AI Commercial Model Strategy</span>
  <span>11</span>
</div>

---

<div class="brand">
  <img src="assets/logo.svg" alt="FlairsTech logo" />
  <span>FlairsTech</span>
</div>

<div class="eyebrow">Governance</div>
<h2>Governance &amp; Implementation Timeline</h2>
<p class="lead">Implementation process turns the commercial model into a controlled operating system.</p>

<div class="grid-2" style="margin-top: 10px;">
  <div class="card" style="padding: 14px 20px;">
    <h3>01 Baseline &amp; Scope</h3>
    <p style="font-size: 12px; color: var(--muted); margin-bottom: 2px;"><strong>Weeks 1–2</strong></p>
    <p>Confirm workflows, data access, KPIs, scope, and commercial assumptions with the client.</p>
  </div>
  
  <div class="card" style="padding: 14px 20px;">
    <h3>02 Configure &amp; Build</h3>
    <p style="font-size: 12px; color: var(--muted); margin-bottom: 2px;"><strong>Weeks 3–5</strong></p>
    <p>Configure AI QA, agent assist/guidance, Client Pulse dashboards, and the governance model.</p>
  </div>
  
  <div class="card" style="padding: 14px 20px;">
    <h3>03 Pilot &amp; Calibrate</h3>
    <p style="font-size: 12px; color: var(--muted); margin-bottom: 2px;"><strong>Weeks 6–8</strong></p>
    <p>Run controlled pilot, compare AI output with human review, and adjust model parameters.</p>
  </div>
  
  <div class="card" style="padding: 14px 20px;">
    <h3>04 Scale &amp; Govern</h3>
    <p style="font-size: 12px; color: var(--muted); margin-bottom: 2px;"><strong>Weeks 9–12</strong></p>
    <p>Expand coverage, move into recurring monthly operating reviews, and audit metrics.</p>
  </div>
</div>

<div class="footer">
  <span>AI Commercial Model Strategy</span>
  <span>12</span>
</div>

---

<div class="brand">
  <img src="assets/logo.svg" alt="FlairsTech logo" />
  <span>FlairsTech</span>
</div>

<div class="eyebrow">Governance</div>
<h2>Guardrails &amp; Eligibility Rules</h2>
<p class="lead">Pricing only works when scope, usage, and delivery ownership are controlled and protected.</p>

<div class="tables-row">
  <div class="cost-table-card">
    <h3>Commercial Guardrails</h3>
    <table>
      <colgroup>
        <col style="width: 33%;">
        <col style="width: 67%;">
      </colgroup>
      <thead>
        <tr>
          <th>Rule</th>
          <th>Recommendation</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><b>Minimum term</b></td>
          <td>6 months, 12 months preferred when setup is amortized</td>
        </tr>
        <tr>
          <td><b>Setup fee</b></td>
          <td>mandatory unless explicitly amortized</td>
        </tr>
        <tr>
          <td><b>Usage caps</b></td>
          <td>required for AI QA, transcription, lead sourcing, dashboards, integrations</td>
        </tr>
        <tr>
          <td><b>Change requests</b></td>
          <td>required for new workflows, channels, languages, ICPs, dashboards</td>
        </tr>
        <tr>
          <td><b>Repricing</b></td>
          <td>volume, channel mix, scope, QA coverage, or data needs change materially</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="cost-table-card">
    <h3>Package Eligibility</h3>
    <table>
      <colgroup>
        <col style="width: 30%;">
        <col style="width: 35%;">
        <col style="width: 35%;">
      </colgroup>
      <thead>
        <tr>
          <th>Package</th>
          <th>Good fit</th>
          <th>Avoid when</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><b>Managed CX/BDR</b></td>
          <td>capacity need, low AI maturity</td>
          <td>client expects transformation or outcome pricing</td>
        </tr>
        <tr>
          <td><b>AI-Enabled CX</b></td>
          <td>stable workflows, KB, data access</td>
          <td>broken SOPs, no baseline, unclear ownership</td>
        </tr>
        <tr>
          <td><b>AIMY-Powered BDR</b></td>
          <td>clear ICP, lead source, handoff rules</td>
          <td>vague ICP, weak offer, no sales owner</td>
        </tr>
        <tr>
          <td><b>Automation/Growth</b></td>
          <td>clear process and outcomes</td>
          <td>subjective criteria, high uncertainty</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

<div class="footer">
  <span>AI Commercial Model Strategy</span>
  <span>13</span>
</div>

---

<div class="brand">
  <img src="assets/logo.svg" alt="FlairsTech logo" />
  <span>FlairsTech</span>
</div>

<div class="eyebrow">Sales Enablement</div>
<h2>Entry Signal to Expansion Path</h2>
<p class="lead">Sales should use AI-first products to diagnose and prove value, then convert into premium operating models.</p>

<table>
  <colgroup>
    <col style="width: 30%;">
    <col style="width: 25%;">
    <col style="width: 45%;">
  </colgroup>
  <thead>
    <tr>
      <th>Client Signal</th>
      <th>Entry Offer</th>
      <th>Expansion Path</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Weak QA visibility</td>
      <td><strong>AI QA Pilot</strong></td>
      <td>AI QA managed service → AI-Enabled CX</td>
    </tr>
    <tr>
      <td>Manual / repetitive workflow</td>
      <td><strong>Workflow Diagnostic</strong></td>
      <td>CX Workflow Automation</td>
    </tr>
    <tr>
      <td>Poor knowledge consistency</td>
      <td><strong>Knowledge Assessment</strong></td>
      <td>Agent Assist → AI-Enabled CX</td>
    </tr>
    <tr>
      <td>Poor lead quality</td>
      <td><strong>ICP/List Build</strong></td>
      <td>AIMY-Powered BDR</td>
    </tr>
    <tr>
      <td>Weak outbound messaging</td>
      <td><strong>Campaign Readiness Pack</strong></td>
      <td>AIMY-Powered BDR</td>
    </tr>
    <tr>
      <td>BDR activity but low quality</td>
      <td><strong>BDR QA Pilot</strong></td>
      <td>AIMY-Powered BDR / Growth Engine</td>
    </tr>
    <tr>
      <td>Clear ICP + outcome focus</td>
      <td><strong>AIMY Growth Engine</strong></td>
      <td>Hybrid pricing / expanded campaigns</td>
    </tr>
  </tbody>
</table>

<div class="footer">
  <span>AI Commercial Model Strategy</span>
  <span>14</span>
</div>

---

<div class="brand">
  <img src="assets/logo.svg" alt="FlairsTech logo" />
  <span>FlairsTech</span>
</div>

<div class="eyebrow">Sales Enablement</div>
<h2>Recommended Leadership Decisions</h2>
<p class="lead">Decisions required by management to make the commercial model executable in production.</p>

<table>
  <colgroup>
    <col style="width: 32%;">
    <col style="width: 68%;">
  </colgroup>
  <thead>
    <tr>
      <th>Decision</th>
      <th>Recommended Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>CX AI uplift</strong></td>
      <td>+25% target applied to base rate card</td>
    </tr>
    <tr>
      <td><strong>BDR AIMY uplift</strong></td>
      <td>+30% target applied to base rate card</td>
    </tr>
    <tr>
      <td><strong>Setup fee policy</strong></td>
      <td>mandatory unless amortized into a longer-term contract</td>
    </tr>
    <tr>
      <td><strong>Client Pulse</strong></td>
      <td>bundled visibility only, not standalone software access</td>
    </tr>
    <tr>
      <td><strong>AI First</strong></td>
      <td>shortlist 3 CX products and 3 BDR products as defined above</td>
    </tr>
    <tr>
      <td><strong>Output pricing</strong></td>
      <td>only with written ICP, acceptance, handoff, and rejection criteria</td>
    </tr>
  </tbody>
</table>

<div class="footer">
  <span>AI Commercial Model Strategy</span>
  <span>15</span>
</div>
