# AiMY — Dual-Track Pitch Website Sitemap

This document maps the page layout, navigation anchors, and interactive components for the refactored **AiMY Product Catalogue and Sales Pitch Website**.

---

## 1. Website Directory Map

```
aimy-catalogue-site/
├── index.html                       # Refactored dual-track website prototype
├── catalogue-public.json            # Sanitized customer-friendly features
├── catalogue-internal-evidence.json # Internal Jira lookup evidence (backstage)
├── catalogue-content.md             # Customer copywriting master source
├── internal-review-notes.md         # Exclusions and traceability gap reports
└── site-map.md                      # Structure outline (this file)
```

---

## 2. index.html Section Layout

The website is engineered as a premium, single-page application (SPA) structured around a dual-track interactive experience:

1.  **Omnichannel Header Navigation**
    *   Corporate branding logo: `AiMY`
    *   **Unified Track Switcher Toggle**: A dynamic, premium tabbed switch allowing prospects to toggle the entire site experience between:
        *   `Support Operations Track`
        *   `Sales Operations Track`
    *   Primary CTA: `Request Assessment`

2.  **Interactive Hero Segment**
    *   Headline & subheadline with glowing animated blobs and smooth radial gradients.
    *   Track-specific copy loaded dynamically based on the active toggle state.

3.  **Before vs. After Comparison Matrix**
    *   Shows Day 0 manual support/sales limitations side-by-side with Day 30 automated outcomes.
    *   Content slides dynamically based on the selected operational track.

4.  **1–4 Week Timeline Visualizer**
    *   A horizontal timeline displaying modular onboarding phases:
        *   `Support Track Timeline`: Knowledge (W1) -> Voice (W2) -> QA (W3) -> Connect (W4).
        *   `Sales Track Timeline`: playbooks (W1) -> BDR sequences (W2) -> Manager canvas (W3) -> Close Loop (W4).

5.  **Modular Product Catalogue Grid**
    *   Interactive cards representing:
        *   *Support view:* Knowledge, Voice, QA, Connect, Continuous Loop.
        *   *Sales view:* Knowledge (Sales), Sales — BDR Mode, Sales — Manager Mode, Continuous Loop (Sales).
    *   Each card features custom scaling transitions. Clicking a card opens a modal overlay showing detailed customer value, integrations, and a **sanitized, searchable catalogue table of recently released features** (zero Jira details).

6.  **"What's New in AiMY" Slider**
    *   Vibrant, glassmorphic highlight boxes illustrating recently shipped customer-facing enhancements.

7.  **Animated Continuous Loop Engine**
    *   Visual flowchart mapping self-improving operational signals. Clicking diagram steps triggers plain-English pipeline explainers.

8.  **Footer**
    *   Product guidelines, review tag, and developer check signatures.
