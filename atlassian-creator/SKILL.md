---
name: atlassian-creator
description: >
  Creates, scopes, and commits Jira epics, Jira stories, and Confluence pages for the AiMY
  platform at FlairsTech, following the product methodology and house rules established by Ahmed
  Mahfouz (Director of Technology). Use this skill whenever Ahmed asks to create, update, write,
  commit, or draft any Jira ticket (epic or story) or Confluence page — or when he says "add this
  to Jira", "create the epics", "commit the stories", "write the Confluence page", "document this",
  or describes a feature or product decision where the natural next step is Jira or Confluence
  output. Also trigger when reviewing or updating existing tickets or pages, scoping a new agent or
  module, or producing a story list for a sprint. This skill governs all naming conventions,
  description formats, field population, flow labelling, story sequencing, diagram preferences,
  Confluence page structure, and the review-before-commit rule that applies to every artifact.
---

# AiMY Atlassian Creator Skill

Governs how all Jira epics, Jira stories, and Confluence pages are created for the AiMY platform.
Read this entire file before producing any Jira or Confluence output.

---

## 0. Working Methodology — Read First

These rules govern every session, regardless of what's being created.

**Decisions before output.** Ahmed works through decisions sequentially before artifacts are
produced. Never jump straight to ticket creation. Confirm scope, phasing, role model, and story
list in the conversation first. Only produce output once decisions are locked.

**Review before commit.** Always present epics and stories in the conversation for Ahmed to review
and correct before calling any Jira or Confluence API. The phrase "commit to Jira" or explicit
approval is the trigger for actual API calls. Never batch-commit without sign-off.

**Sequential task focus.** Finish one task completely before moving to the next. If something
surfaces that needs attention but isn't the current task, flag it with a 📌 to-do marker and
continue. Do not context-switch mid-task.

**Be inquisitive.** Ask the question that should be asked, not just the one that was asked.
Proactively surface gaps, inconsistencies, open decisions, and risks before they become problems.

**Simplicity in Jira language.** Story descriptions must be conversational. A developer picking
up a story cold should understand what to build without asking anyone. No jargon, no corporate
filler, no checklist walls.

**Flag everything deferred.** Any decision, open question, or dependency that surfaces during a
session but isn't resolved gets a 📌 to-do marker inline, and appears in the To-Do Delta at the
end of the session.

---

## 1. Atlassian Configuration

**Cloud ID:** `d3513000-a49d-4f6b-8258-dc0e35fc47fe`
**Instance:** flairstechdev.atlassian.net
**Jira boards:** AIMY (Implementation team), RD (PoC / Research)
**Confluence space key:** AC2 (AIMY Central)
**Confluence space numeric ID:** `426901869` — required for `spaceId` parameter on all API calls

### Critical API Rules

- Always use `contentFormat: "markdown"` on Jira story descriptions
- Epic issue types do NOT require custom fields — only Stories do
- Story-to-epic linking: use `parent: {"key": "AIMY-XXXX"}` parameter, not a custom field
- JQL searches: use broad `summary ~` with OR conditions; split into two queries to avoid result limits
- Before creating any Confluence page: search for an existing page first using `searchConfluenceUsingCql`
- `spaceId` on Confluence API calls must be the numeric ID (`426901869`), not the space key

### Required Custom Fields — AIMY Story Issue Types Only

| Field | Key | Required Value |
|---|---|---|
| Product | `customfield_10122` | `{"id": "10355"}` — use for all AiMY Talent stories |
| Acceptance Criteria | `customfield_10117` | ADF format — plain text is rejected by the API |

Epic issue types: no custom fields needed.

### Known Confluence Page IDs — Agent Product Overviews

| Agent | Page ID | URL |
|---|---|---|
| AiMY Talent — Product Overview | `539754497` | /spaces/AC2/pages/539754497 |
| AiMY Talent — Business Flows | `642285570` | /spaces/AC2/pages/642285570 |
| AiMY Connect — Product Overview | `639696898` | /spaces/AC2/pages/639696898 |
| AiMY QA — Product Overview | `539394056` | /spaces/AC2/pages/539394056 |
| AiMY Sales — Product Overview | `539361283` | /spaces/AC2/pages/539361283 |
| AiMY Knowledge — Product Overview | `539394049` | /spaces/AC2/pages/539394049 |
| AiMY Phone — Product Overview | `621117442` | /spaces/AC2/pages/621117442 |
| AiMY Phone — Epic & Story Index | `620855302` | /spaces/AC2/pages/620855302 |
| Sales ↔ Connect Boundary Decision | `639467522` | /spaces/AC2/pages/639467522 |

Agent Product Overview pages share the same parent folder: `539361281`
Business Flows pages are created as children of their agent's Product Overview page.
Architecture Decision pages are created as children of the relevant agent's Product Overview page.

---

## 2. Jira Epic Rules

### Naming Convention

Format: `[Agent Name] — [What It Does]`

Good: `AiMY Talent — WhatsApp Channel for Recruiters`
Good: `AiMY Sales — Outreach Orchestration & Sequencing`
Bad: `AIMY Talent WhatsApp` / `Talent - WhatsApp improvements` / `AiMY-NEW-01`

Never use "NEW" in any placeholder ID. Never use "AIMY" in prose titles — only in Jira board keys.

### Epic Description Structure

```markdown
[One paragraph: what this epic delivers and why it matters. Written from the user's perspective.
No bullet walls — full sentences.]

## Business Flow
[flow-label]

## Out of Scope
[What explicitly is NOT in this epic. Always include even if brief.]

## Dependencies
[Other epics or stories that must exist first. External system or ops prerequisites.]

## References
[RD tickets this supersedes. Confluence pages. Prior research. Always include if applicable.]
```

### Epic Labels
Always apply two labels:
1. The relevant flow label (e.g., `flow-candidate-comms`)
2. The agent label (e.g., `aimy-talent`, `aimy-sales`, `aimy-connect`)

---

## 3. Jira Story Rules

### Story Format — Non-Negotiable

Every story uses exactly this structure. No variations, no additional sections:

```markdown
## User Story

As a [role], I want to [action], so that [outcome].

## How It Works

- [Bullet: what the system does, in plain conversational language]
- [Bullet: what happens next, edge cases, fallback behaviour]
- [Future state note if relevant: "Future: once X is live, Y replaces Z"]

## Depends On

- [AIMY-XXXX (what it provides to this story)]
- [External dependency — e.g., "WhatsApp Business account provisioned at FlairsTech (ops prerequisite)"]
- [Parent epic key — always include]
```

**No acceptance criteria checklists.** No "Definition of Done" sections. No "Technical Notes"
sections. No "Business Value" headers. The "How It Works" section carries all of that in plain
language. If a developer needs a checklist, the How It Works bullets are the checklist.

### Story Titles

Format: `[Epic Context] — [What This Story Does]`

Good: `WhatsApp — Twilio Business API Integration`
Good: `Interview Scheduling — Stall Alert: No Booking Received`
Bad: `Implement WhatsApp` / `Scheduling story 2` / `AIMY-4149 subtask`

Titles must be specific enough to identify the story without reading the description.

### Blocked Stories

If a story cannot start due to a pending external decision:
- Add `[BLOCKED]` to the end of the title
- In "How It Works": state what the blocker is and who owns the decision
- In "Depends On": reference the blocking item explicitly

### Story Sequence & Dependency Discipline

When presenting a story list for review, always include a sequence column showing:
- The build order (1, 2, 3... or 1, 2a, 2b for parallel paths)
- What each story depends on
- What each story unlocks

Make dependency chains explicit in the "Depends On" section — never leave a story that looks
self-contained when it actually needs another story to ship first.

### Batch Commit Process

1. Present all stories grouped by epic in a review table (Key TBD, Title, Sequence, Summary)
2. Ahmed reviews — wait for explicit approval or corrections
3. Create epics first; record their keys before creating any stories
4. Create stories in dependency order, parent each to correct epic key
5. After all commits: present a final key index (epic keys + story keys, grouped by epic)
6. Update the agent's Product Overview page Jira index section

---

## 4. Confluence Content Rules

### When to Create vs. Update

**Create new:** New agent product overview, new business flows page, new architecture decision page
**Update existing:** Jira index after new tickets, corrections from a session, new sections added

Always search before creating:
```
searchConfluenceUsingCql: title = "[Page Title]" AND space.key = "AC2"
```

### Diagram Preferences

Two diagram types are used depending on context:

**Text/ASCII diagrams** — used inside Confluence pages for flow sequences:
```
Recruiter instructs AiMY in chat
    ↓
AiMY composes WhatsApp message (AIMY-4156)
    ↓
Recruiter confirms → AiMY sends via Twilio (AIMY-4151)
```
Always wrap in a code block. Include Jira ticket references at each step.

**Mermaid diagrams** — used for standalone FigJam boards and complex system diagrams.
Use `Figma:generate_diagram` tool. Prefer `flowchart LR` direction. Quote all node and edge text.

### Product Overview Page — Required Structure

Read `references/page-templates.md` for the full template. Required sections in order:

1. Status header (Status, Owner, Last Updated, Confidential tag)
2. What [Agent] Is + What [Agent] Is NOT
3. North Star
4. Legacy Systems & Integration Principle (if agent wraps legacy systems)
5. Interaction Model (if agent uses chat + right panel pattern)
6. Deployment Model
7. Role Model (table: Role, Who They Are, What They Own, What They See)
8. Business Flows (summary table + link to Business Flows child page)
9. Module Architecture (phased tables: Module, What It Does, Primary Role(s))
10. Cross-Agent Dependencies (table: Module, Depends On, Nature)
11. Jira Epic Index (epics table + story sub-tables grouped by epic)
12. Known Gaps & Open Items (table: Item, Status, Notes)
13. Standing Principles (prose bullets)
14. References (Confluence pages table + Jira key table)

Footer: *This page is the single source of truth for [Agent] product scope.*

### Business Flows Page — Purpose & Structure

Purpose: give developers the sequencing context that Jira alone cannot provide.
Lives as a child of the agent's Product Overview page.

Required sections:
1. **Purpose of This Page** — explain why flows exist, what developers should do with them
2. **Interaction Model — Read This First** — the chat/right panel split, no-forms rule, etc.
3. **One section per flow** — flow label, what it covers, full ASCII sequence diagram with Jira refs, epics table, story sequence table with build order numbers
4. **Flow Dependency Map** — ASCII diagram showing how flows connect to each other
5. **Jira Label Reference** — table of all flow labels and what they cover

Story sequence tables must include a "Sequence" column with explicit numbers and a note on what each story depends on and unlocks.

### Confluence Writing Standards

- **Prose with headers** for explanatory sections — not bullet walls
- **Tables** for role models, epic indexes, module architecture, story sequences, gap lists
- **Code blocks** for flow diagrams (ASCII) and sequence diagrams
- Always include a **version message** on updates that describes exactly what changed
- **Update the Jira epic index** in the Product Overview after every session where tickets are created
- Link to Jira tickets with full URLs: `https://flairstechdev.atlassian.net/browse/AIMY-XXXX`
- Link to Confluence pages with full URLs: `https://flairstechdev.atlassian.net/wiki/spaces/AC2/pages/[ID]`

---

## 5. AiMY Platform Rules — Always Apply

### Terminology
- Write **"AiMY"** (capital M) in all prose, titles, and page content
- "AIMY" is correct only in Jira board keys (AIMY-XXXX) and Confluence space keys
- **Never reference in any output:** PEX, AIMY K Aroma, AiMY Analytics (retired March 2026),
  AiMY Dev, AiMY UI, MyConnect/Calls (legacy)

### Pricing
- Always outcome-based: per chat, per conversation, per transaction
- Never per-seat under any framing

### Platform Capabilities
- Voice AI and n8n are **native platform capabilities** — never named as third-party tools
- AI-generated articles always require **human review** before publishing — never say "auto-published"
- Deployment timeline is **1–4 weeks** — not 6–8 weeks
- FlairsTech is always **the first customer** — internal deployment is the proof of concept

### Retired — Never Reference
AiMY Analytics is RETIRED (March 2026). Capabilities redistributed:
- Operational dashboards → AiMY Connect (Operations Hub)
- Funnel analytics → AiMY Sales Manager mode (via Generative UI)

---

## 6. Reference Files

Read these when the task requires deeper guidance:

| File | When to Read |
|---|---|
| `references/decisions.md` | Any time you are about to define agent boundaries, module ownership, role model, interaction model, or architectural scope. Also read to avoid contradicting locked decisions. |
| `references/flows.md` | When applying flow labels, writing a Business Flows page, building story sequence tables, or documenting how flows connect. |
| `references/page-templates.md` | When creating or substantially updating a Product Overview, Business Flows, or Architecture Decision page. |

---

## 7. Pre-Commit Quality Checklist

Run through this before calling any Jira or Confluence API:

**Methodology**
- [ ] Ahmed has reviewed and approved the output in the conversation
- [ ] All decisions were confirmed before output was produced

**Jira Epics**
- [ ] Title format: `[Agent Name] — [What It Does]`
- [ ] Description includes: Business Flow label, Out of Scope, Dependencies, References sections
- [ ] Flow label + agent label applied
- [ ] No custom fields on epic issue types

**Jira Stories**
- [ ] Description format: User Story → How It Works → Depends On (nothing else)
- [ ] `customfield_10122: {"id": "10355"}` set on all AIMY Story issue types
- [ ] `contentFormat: "markdown"` used on all story descriptions
- [ ] Parent epic key in `parent` parameter
- [ ] Sequence numbers confirmed and dependency chain explicit
- [ ] Blocked stories have `[BLOCKED]` in title and blocker documented

**Confluence**
- [ ] Searched for existing page before creating new
- [ ] `spaceId` is numeric `426901869` (not space key "AC2")
- [ ] Version message describes what changed
- [ ] Jira epic index updated in Product Overview after ticket commits
- [ ] Diagram type matches context: ASCII in pages, Mermaid for FigJam

**Language**
- [ ] "AiMY" capitalisation correct throughout
- [ ] No hard ROI figures, no per-seat pricing, no "auto-published"
- [ ] No references to retired agents or deprecated terminology
- [ ] No "NEW" in any story or epic identifier
