# Confluence Page Templates

Templates for the three standard page types used in AC2. Follow these structures exactly.
Adapt section content to the agent — never remove sections, never add sections not listed here.

Last Updated: April 2026

---

## Template 1: Agent Product Overview Page

**Placement:** Child of agent folder under AC2 root (parent ID `539361281`)
**Title format:** `[AiMY Agent Name] — Product Overview`
**Version message on create:** "Initial product overview — [Month Year]"
**Version message on update:** Describe specifically what changed, e.g.,
"Updated Jira index with epics from April 2026 session. Added business flow section."

---

```markdown
# [AiMY Agent Name] — Product Overview

**Status:** [e.g., Internal Only — In Development / Live — External Revenue]
**Owner:** Ahmed Mahfouz
**Last Updated:** [Month Year]
**Confidential — Internal Use**

---

## 1. What [Agent] Is

[Two to three sentences. What it does, what it replaces, who it serves. Written from the
product perspective — not marketing. Include the "not just a X" framing where relevant.]

### What [Agent] Is NOT

- Not [common misconception 1]
- Not [common misconception 2]
- Not [common misconception 3]

---

## 2. North Star

[One paragraph. The end-state vision — what does done look like? What problem is fully solved?
Should be specific enough to make scope decisions against.]

---

## 3. Legacy Systems & Integration Principle

[Include this section only if the agent wraps legacy FlairsTech systems. Otherwise remove.]

[Name each legacy system, what it does, how AiMY integrates with it (read-only vs. bidirectional),
and the direction of travel (becomes legacy over time). Always invoke the outside-in replacement
principle.]

---

## 4. Interaction Model

[Include this section only if the agent uses the chat + right panel Generative UI pattern.
Otherwise remove. Document: what goes in chat, what goes in the right panel, what auto-loads
on login per role. Reference AIMY-4094. State the no-forms rule if applicable.]

---

## 5. Deployment Model

[Two to three sentences. FlairsTech first. Which BUs are primary stakeholders. External
productization timeline / status.]

---

## 6. Role Model

| Role | Who They Are | What They Own | What They See |
| --- | --- | --- | --- |
| [Role 1] | [Who] | [What they control] | [Their visibility scope] |
| [Role 2] | ... | ... | ... |

### [Any sub-decisions about the role model — approval chains, visibility boundaries, etc.]

---

## 7. Business Flows

[Agent] work is organised into business flows. Each flow is a sequence of epics and stories
that together deliver a complete user outcome. Flows are labelled on all Jira epics and stories.

See the dedicated page for full flow documentation and story sequences:
**[[AiMY Agent] — Business Flows & Interaction Model](link)**

| Flow Label | What It Covers | Epics |
| --- | --- | --- |
| `flow-label-1` | [Description] | [Epic keys] |
| `flow-label-2` | ... | ... |

---

## 8. Module Architecture

### Phase 1 — [Phase Name]

| Module | What It Does | Primary Role(s) |
| --- | --- | --- |
| **[Module Name]** | [Plain language description] | [Role(s)] |

### Phase 2 — [Phase Name]

[Same table structure]

### Phase 3 — [Phase Name]

[Same table structure]

---

## 9. Cross-Agent Dependencies

| [Agent] Module | Depends On | Nature |
| --- | --- | --- |
| All modules | AiMY Knowledge | Shared memory backbone |
| [Module] | [Agent + Epic] | [What flows between them] |

---

## 10. Jira Epic Index

### AIMY Board (Implementation)

| Key | Title | Flow | Phase | Status |
| --- | --- | --- | --- | --- |
| [AIMY-XXXX] | [Epic Title] | `flow-label` | [1/2/3] | [To Do / In Progress / Released] |

### Story Index by Epic

#### [Epic Title] ([Epic Key])

| Key | Title |
| --- | --- |
| [AIMY-XXXX] | [Story Title] |

### RD Board (PoC / Research Reference)

| Key | Title | Status | Notes |
| --- | --- | --- | --- |
| [RD-XXXX] | [Title] | [Status] | [e.g., superseded by AIMY-XXXX / promote when Phase 1 stable] |

---

## 11. Known Gaps & Open Items

| Item | Status | Notes |
| --- | --- | --- |
| [Gap or open decision] | [e.g., Not started / BLOCKED / Pending decision] | [What's needed to resolve] |

---

## 12. Standing Principles

- [Agent] is **FlairsTech-first** — [internal dogfood principle]
- [Key boundary or design principle]
- [Pricing principle if applicable]
- Write **"AiMY"** (capital M). Never "AIMY".

---

## 13. References

### Confluence Pages

| Page | Link |
| --- | --- |
| [Page Title] | [URL] |

### Jira — Key Epics

| Key | Summary | Link |
| --- | --- | --- |
| [AIMY-XXXX] | [Epic Title] | [https://flairstechdev.atlassian.net/browse/AIMY-XXXX] |

---

*This page is the single source of truth for [AiMY Agent] product scope.*
```

---

## Template 2: Business Flows & Interaction Model Page

**Placement:** Child of the agent's Product Overview page
**Title format:** `[AiMY Agent Name] — Business Flows & Interaction Model`
**Version message:** "Initial flows documentation — [Month Year]"

---

```markdown
# [AiMY Agent] — Business Flows & Interaction Model

**Owner:** Ahmed Mahfouz
**Last Updated:** [Month Year]
**Parent:** [[AiMY Agent] — Product Overview](link)
**Confidential — Internal Use**

---

## Purpose of This Page

[Two paragraphs. Explain the problem this page solves: developers see Jira tickets as
independent items with no sequencing context. This page provides the sequence, rationale,
and dependency chain. Explain that developers should read this page before picking up any story.]

---

## Interaction Model — Read This First

[Document how the agent's UI works at the surface level — before any flow-specific content.
This shapes how every story is built. For agents using Generative UI: document the chat / right
panel split, no-forms rule, WhatsApp as output channel, role-based auto-load. For other agents:
document whatever interaction model applies.]

### [Sub-section: e.g., "The Chat + Right Panel Split"]

[Prose explanation of what each surface is for.]

### [Sub-section: e.g., "Role-Based Right Panel"]

| Role | Right Panel Auto-Loads With |
| --- | --- |
| [Role] | [Content] |

---

## Flow: `flow-label-1`

**What this flow covers:** [One sentence.]

**[Any important note — e.g., current channel priority, phase dependency]**

### Sequence

[ASCII code block diagram showing the full flow with Jira ticket references at each step]

```
[Step description]
    ↓
[Step description (AIMY-XXXX)]
    ↓
[Branch A → AIMY-XXXX]
[Branch B → AIMY-XXXX]
```

### Epics in This Flow

| Key | Title | Status |
| --- | --- | --- |
| [AIMY-XXXX] | [Epic Title] | [Status] |

### Stories in This Flow

| Key | Title | Sequence |
| --- | --- | --- |
| [AIMY-XXXX] | [Story Title] | [1 — Foundation / 2 — depends on AIMY-XXXX / etc.] |

### [Key Dependency note if applicable]

---

## Flow: `flow-label-2`

[Same structure as above]

---

## Flow Dependency Map

[ASCII code block showing how the flows connect to each other. Which flows feed into which.
Which flows run in parallel.]

```
flow-one
    ↓
flow-two    flow-parallel (runs in parallel)
    ↓
flow-three
```

---

## Jira Label Reference

Use these labels on all [Agent] epics and stories. A story belongs to exactly one flow.

| Label | Covers | Apply To |
| --- | --- | --- |
| `flow-label` | [Description] | [Epic keys] |
| `aimy-[agent]` | Agent label — apply to ALL [Agent] tickets | Everything |

---

*This page is maintained as part of the [AiMY Agent] product documentation.
Update after each planning session where flows are added, modified, or sequenced.*
```

---

## Template 3: Architecture Decision Page

**Placement:** Child of the relevant agent's Product Overview page
**Title format:** `Architecture Decision — [What Was Decided]`
**Version message:** "Architecture decision documented — [Month Year]"

---

```markdown
# Architecture Decision — [What Was Decided]

**Decision Date:** [Month Year]
**Owner:** Ahmed Mahfouz
**Status:** Locked
**Documented In:** [Confluence page this lives under]

---

## Context

[Two to three sentences. What question needed answering? What was ambiguous or in dispute?
What triggered the need for this decision?]

---

## Decision

[One or two sentences. The decision in plain language. No ambiguity.]

**[Left side] = [Role/function it owns]**
**[Right side] = [Role/function it owns]**

---

## Rationale

[Why this boundary? What principle was applied? Reference the "boundaries follow user roles"
principle where applicable.]

---

## Boundary Table

| Responsibility | Owner |
| --- | --- |
| [Specific responsibility] | [Owner] |
| [Specific responsibility] | [Owner] |

---

## What Is Explicitly Out of Scope for Each Side

**[Left side] does NOT own:**
- [Item]
- [Item]

**[Right side] does NOT own:**
- [Item]
- [Item]

---

## Split Cases

[Document any responsibilities that are genuinely shared or split, with exact ownership of each part.]

---

*This decision is locked. Any proposal to revise it must go through Ahmed Mahfouz.*
```

---

## Version Message Standards

Always be specific in version messages — vague messages like "updates" are not acceptable.

| Action | Example Version Message |
|---|---|
| New page created | "Initial product overview — April 2026" |
| Jira index updated | "Updated Jira index: added AIMY-4148–4256 from April 2026 Talent session" |
| Section added | "Added Business Flows section (Section 7) and link to flows child page" |
| Full rewrite | "Full rewrite — vision, role model, module architecture, Jira index. April 2026." |
| Correction | "Corrected: AiMY Analytics marked as RETIRED, capabilities redistributed" |
| Minor update | "Updated Known Gaps: added Microsoft Bookings API access confirmation item" |
