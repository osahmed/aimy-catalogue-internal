# AiMY Standing Decisions

All decisions on this page are locked. Do not contradict them in any output.
When a new decision is made in a session, add it here before the session ends.

Last Updated: April 2026

---

## Agent Boundaries

### AiMY Sales ↔ AiMY Connect (Locked March 2026)
Documented in Confluence AC2 page 639467522.

**Rule:** Boundaries follow user roles, not functional overlap. Ask "which user role owns this
workflow?" — not "which system touches the data?"

| Responsibility | Owner |
|---|---|
| Cadence design — what touchpoints, in what order, over what timeframe | AiMY Sales |
| Task generation — "Rep X needs to call Lead Y today" | AiMY Sales |
| Task prioritization within a rep's queue | AiMY Sales |
| Real-time availability routing — "Rep X is free, push next task" | AiMY Connect |
| Redistribution / reassignment — rep is offline, overloaded, or sick | AiMY Connect |
| Supervisor visibility into BDR execution | AiMY Connect (Operations Hub) |
| Retry on failed outreach attempt | Split — Sales logs attempt and updates cadence; Connect handles re-queue for real-time routing only |

### AiMY Talent ↔ AiMY Connect (Locked April 2026)

- **AiMY Talent = Planner** — hiring requests, pipeline management, interview scheduling, evaluation, outcome routing
- **AiMY Connect = Dispatcher** — routes WhatsApp and voice channels for recruiter-candidate communication; manages channel-level operations in real time
- Talent decides what should happen and to whom. Connect handles the channel in real time.

### AiMY QA Scope (Locked)

- Evaluates all conversation quality across all agents: calls, WhatsApp transcripts, tickets
- QA's responsibility ends at the failure signal. Knowledge enrichment (article generation, publishing) is owned by AiMY Knowledge — not QA.
- QA absorbs platform-wide KPI governance and metric definitions (the proposed KPI Dictionary concept is absorbed into QA, not a separate module).

---

## AiMY Talent — Locked Decisions

### Interaction Model (Locked April 2026)

- **Chat interface is the primary interaction surface** for all roles. No forms anywhere.
- **Right panel is the canvas**: candidate cards, pipeline visuals, analytics, item details. Not a control surface.
- Right panel **auto-loads** with role-appropriate content when a user opens AiMY Talent — no navigation required.
- **WhatsApp is an output channel** — AiMY composes, recruiter instructs via chat. Recruiters never write WhatsApp messages directly.
- Hiring manager interview feedback is collected **conversationally via chat** — not a form.
- This is the **Generative UI pattern** (AIMY-4094) — same as AiMY Sales Manager mode.
- QA v2 uses a floating chat pattern — this is **distinct** from the Generative UI chat + canvas. Do not conflate them.

### Role Model (Locked April 2026)

| Role | Visibility Boundary |
|---|---|
| HR Manager | All reqs, all recruiters. Full pipeline across everything. |
| Recruiter | Only their assigned reqs and candidate queues. |
| Hiring Manager | Only their own reqs. |
| Candidate | Only their own application. Via Portable Agent, no login required. |
| Employee | Only their own profile, onboarding tasks, and HR self-service requests. |

No cross-pollination between Hiring Managers. HR Manager sees all.

### Offer Approval Chain (Locked April 2026 — full mapping pending)

Recruiter prepares → Hiring Manager approves (candidate fit, salary, margin) → Business Unit Director approves (offer send) → Offer dispatched via e-signature.

Full three-tier workflow must be mapped before RD-1324 moves to Implementation.

### Legacy System Integration (Locked April 2026)

- **Engage** — candidate and employee record store (CVs, skills, interview notes). Read-only source. Becomes legacy.
- **SSA** — workflow and approval system (recruitment initiation, approvals, HR decisions). Bidirectional: AiMY reads from and writes back. Becomes legacy.
- Both are integration points, not constraints. Outside-in replacement — wrap first, replace over time.
- The hiring funnel is owned and stored natively in AiMY Talent (Engage cannot cleanly support it).

---

## Platform Architecture — Locked Decisions

### Generative UI (AIMY-4094)

- Shared platform infrastructure. Split-pane: persistent chat left, generated visualizations right.
- First consumer: AiMY Sales Manager mode.
- Second consumer: AiMY Talent HR Manager Operations Hub.
- Reusable by AiMY Connect Operations Hub and AiMY QA v2 in future.
- QA v2 floating chat is a **distinct** pattern — do not conflate.

### MCP Multi-Server Platform (AIMY-3681)

- Shared **Phase 1** dependency for both AiMY Sales and AiMY Talent.
- When updating AIMY-3681: add a comment explaining it is a shared Phase 1 dependency for both agents, not sequential.

### Sales & Talent Share Infrastructure (Locked)

- AiMY Phone (AIMY-3683–3687) — shared across both agents
- MCP framework (AIMY-3681) — Phase 1 shared dependency
- Features built for one are designed for reuse on the other from day one

### Operations Hub

The Operations Hub is a **permission-gated visibility layer inside an agent** — not a separate product.

- **Support / Sales Operations Hub** → lives inside AiMY Connect
- **HR Manager Operations Hub** → lives inside AiMY Talent
- Support Supervisor and Sales Supervisor share AiMY Connect but with **different data contexts** — two separate views, never blended.

---

## AiMY Sales — Phase 1 Sprint Plan (Locked March 2026)

| Epic | Key | Sprint |
|---|---|---|
| Data Hygiene & Validation | AIMY-4076 | S1–S2 |
| Outreach Orchestration & Sequencing | AIMY-4082 | S2–S3 |
| Rep Task View | AIMY-4088 | S1–S2 |
| Generative UI — Chat + Canvas (platform) | AIMY-4094 | S3 |

Stories: AIMY-4077 through AIMY-4140 (13 stories).
Sprint 1: Lead Sourcing, Data Hygiene scaffold, Rep View UI shell.
Sprint 2: Data Hygiene build, Sequencing cadence engine, AiMY Phone infra, Rep View live data.
Sprint 3: Dialer trigger, next-best action, QA linkage, Manager Generative UI.

---

## Open Items — Not Yet Decided

These items are known but undecided. Do not make assumptions about them in output.

| Item | Status |
|---|---|
| AiMY Sales external offering | Pending — Ahmed decision |
| AiMY Knowledge pricing (infrastructure vs. product) | Pending — Ahmed decision |
| Portable Agent website deployment | Wired into Talent, not live — blockers TBD |
| AIMY-NEW-01 through 07 (Managed AI Support gap closure epics) | Specified, not yet created in Jira |
| Peter's playbook reframing pass | Confirmed next step, not started |
| AiMY Finance scoping | ~1 month out, zero Jira epics |
| QA v2 forward roadmap | Blocked on Ahmed sharing QA UI |
| ACF (AiMY Contribution Framework) | Flagged for dedicated session |
| AIMY-3122 / AIMY-3124 overlap | Two escalation epics — merge or clarify |
| RD-1325 (AiMY Operations Agent), RD-1422 (Sales V2), RD-1425 (Connect Copilot) | Surfaced, not discussed |
| WhatsApp Egyptian number provisioning | AIMY-4181 BLOCKED — ops decision pending |
| Microsoft Bookings API access | Bookings live at FlairsTech — confirm Graph API access before AIMY-4186 starts |
| Hiring Manager auth model for external tenants | Active Directory per tenant — document when external offering scoped |

---

## Retired / Never Reference

| Term | Reason |
|---|---|
| AiMY Analytics | RETIRED March 2026. Capabilities → Connect Ops Hub + Sales Manager mode. |
| MyConnect / Calls | Legacy. Being replaced by AiMY Connect. |
| PEX | Old branding of AiMY Knowledge. No longer in use. |
| AIMY K Aroma | Cancelled initiative. |
| AiMY Dev | Not a current agent. |
| AiMY UI | Not a current agent. |
| 6–8 week deployment timeline | Corrected to 1–4 weeks. |
| Per-seat pricing | Never. Always outcome-based. |
