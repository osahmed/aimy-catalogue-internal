# AiMY Business Flows Reference

Flows solve a specific problem: developers see Jira tickets as independent items with no visible
connection to each other or to the bigger picture. Flows provide that context — the sequence,
the rationale, and the dependency chain that ties stories together.

Last Updated: April 2026

---

## How Flows Work

Every Jira epic and story carries a flow label. Stories belong to exactly one flow.

When creating a Business Flows Confluence page, document each flow with:
1. What it covers (one sentence)
2. The full sequence as an ASCII code-block diagram with Jira ticket references at each step
3. A story sequence table with explicit build order numbers and dependency notes
4. Key dependencies called out separately

When presenting stories for review, always include a sequence column. Make the build order
unambiguous so the implementation team knows exactly what to build first.

---

## AiMY Talent Flows (Active — April 2026)

### `flow-candidate-comms`
All communication channels recruiters use with candidates. AiMY mediates every outbound message —
recruiters never compose directly. Channel priority: Calls (live) → WhatsApp (being built) →
Email (scheduling only, until WhatsApp is live).

**Epics:** AIMY-3683–3687 (AiMY Phone), AIMY-4148 (WhatsApp)

**WhatsApp story build sequence:**
1. AIMY-4151 — Twilio Business API Integration ← foundation, everything depends on this
2. AIMY-4156 — Recruiter-Instructed Outreach via Chat
3. AIMY-4161 — Inbound Notification & Recruiter Response Flow
4. AIMY-4166 — Conversation History in Candidate Activity Timeline
5. AIMY-4171 — Conversation Handoff to AiMY QA for Scoring
6. AIMY-4176 — Send Microsoft Bookings Link to Candidate (depends on AIMY-4186)
7. AIMY-4181 — Egyptian Local Number Provisioning Spike [BLOCKED]

---

### `flow-talent-acquisition`
The full recruiter-facing hiring loop: screening decision → interview scheduling → interview →
feedback collection → outcome routing. Core operational loop delivering immediate internal value.

**Epics:** AIMY-4149 (Interview Scheduling), AIMY-4150 (Interview Feedback), AIMY-3381 (CV Parsing)

**Interview Scheduling build sequence:**
1. AIMY-4186 — Microsoft Bookings Integration ← foundation, everything in scheduling depends on this
2. AIMY-4191 — Trigger & Bookings Link Dispatch via Email
3. AIMY-4196 — Booking Confirmed: Pipeline Update & Notifications
4. AIMY-4201 — Stall Alert: No Booking Received

**Interview Feedback build sequence:**
1. AIMY-4206 — Post-Interview Request via Conversational Chat ← triggers after AIMY-4196 confirms time
2. AIMY-4211 — AI Evaluation Summary Generation ← core synthesis step; all routing depends on this
3a. AIMY-4216 — Outcome Routing: Proceed to Offer
3b. AIMY-4221 — Outcome Routing: Pass & Candidate Rejection
3c. AIMY-4226 — Outcome Routing: Further Review & Conflict Escalation
4. AIMY-4231 — Sync Outcomes to Candidate Profile & Operations Hub

**Key cross-flow dependency:** AIMY-4186 (Microsoft Bookings) must confirm Microsoft Graph API
access is available before starting. FlairsTech Bookings account already provisioned.

---

### `flow-hr-visibility`
The HR Manager's operational view of the recruitment pipeline. Not a reporting product — an
operational layer that auto-loads on login and responds to conversational queries in chat.

**Epic:** AIMY-4004 (HR Manager Operations Hub)

**Build sequence:**
1. AIMY-4236 — Role-Based Auto-Load: HR Manager Right Panel ← foundation; all other hub stories depend on this
2. AIMY-4241 — Pipeline Summary View
3. AIMY-4246 — Recruiter Activity Feed
4. AIMY-4251 — Stall Alerts (feeds into AIMY-4236 auto-load)
5. AIMY-4256 — Interview Outcome Summary ← depends on AIMY-4231 being complete

---

### `flow-offer-onboarding`
Offer generation, three-tier approval chain, onboarding orchestration, ramp-to-productivity.

**Status:** Phase 2 — not in active development. Epics to be created.
**Reference:** RD-1324 (Closing Loops) — promote to Implementation when Phase 1 is stable.

**Approval chain (must be fully mapped before implementation):**
Recruiter prepares → Hiring Manager approves (fit + salary + margin) → BU Director approves
(send) → E-signature dispatched → Acceptance triggers onboarding task generation.

---

### `flow-candidate-experience`
Candidate-facing Portable Agent — embeddable on any website, voice-capable, no login required.

**Status:** Phase 1 — wired into AiMY Talent, not yet deployed on FlairsTech website.
Deployment blockers to be discussed separately.

---

### `flow-employee-lifecycle`
Post-hire employee access — onboarding tasks, documents, HR self-service requests.

**Status:** Phase 2+ for AiMY Talent. Parallel track in progress: vacation request flow being
built via AiMY Knowledge as entry point, with SSA write-back for approved requests.
Full scope to be aligned across AiMY Talent, AiMY Knowledge, and AiMY Finance.

---

## AiMY Sales Flows (Active — March 2026)

Sales uses the same flow labelling system. When creating new Sales stories, apply:
- `flow-lead-sourcing` — Apollo integration, persona filtration, data hygiene
- `flow-outreach-execution` — Sequencing, cadence engine, attempt logging, AiMY Phone auto-trigger
- `flow-rep-task-view` — Rep daily task queue, live data connection
- `flow-manager-visibility` — Funnel governance, Manager Generative UI, QA linkage
- `aimy-sales` — agent label on all Sales tickets

---

## Flow Dependency Map (AiMY Talent)

How the six Talent flows connect in sequence:

```
flow-candidate-experience          flow-candidate-comms
  (Portable Agent inbound)           (calls + WhatsApp outbound)
              \                          /
               ↓                        ↓
              flow-talent-acquisition
         (screening → interview → outcome)
                        ↓
              flow-offer-onboarding
         (offer → approval → onboarding)
                        ↓
             flow-employee-lifecycle
               (post-hire self-service)

flow-hr-visibility runs in parallel across ALL flows — the Operations Hub reflects
the live state of every other flow in real time.
```

---

## Jira Label Reference — AiMY Talent

| Label | Covers | Apply To |
|---|---|---|
| `flow-candidate-comms` | Calls, WhatsApp, email with candidates | AIMY-4148, AiMY Phone epics |
| `flow-talent-acquisition` | Interview scheduling, feedback, outcome routing | AIMY-4149, AIMY-4150, AIMY-3381 |
| `flow-hr-visibility` | HR Manager Operations Hub | AIMY-4004 |
| `flow-offer-onboarding` | Offer generation, approval, onboarding | Phase 2 epics (TBD) |
| `flow-candidate-experience` | Portable Agent, candidate-facing surfaces | Phase 1 epic (TBD) |
| `flow-employee-lifecycle` | Post-hire self-service | Phase 2+ epics (TBD) |
| `aimy-talent` | Agent label — apply to ALL AiMY Talent epics and stories | Everything |

---

## Defining Flows for New Agents

When starting a planning session for a new agent or a new phase of an existing agent:
1. Define the end-to-end user journey as a sequence of outcomes
2. Group the outcomes into flows (each flow = one complete user journey thread)
3. Name each flow with the `flow-[agent]-[what-it-covers]` pattern or `flow-[what-it-covers]`
4. Document in the agent's Business Flows Confluence page before creating any Jira tickets
5. Apply flow labels to all epics and stories as they are created
