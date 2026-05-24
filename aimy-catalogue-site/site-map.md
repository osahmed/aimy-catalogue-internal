# AiMY Catalogue Website — Site Map & User Navigation Plan

This document outlines the proposed page structure, navigation links, and interactive flow for the AiMY Catalogue Static Website.

---

## 1. Directory Structure

```
aimy-catalogue-site/
├── index.html               # Main single-page application prototype
├── catalogue-data.json      # Structured data of all modules & tickets
├── catalogue-content.md     # Customer-facing copywriting source
├── internal-review-notes.md # Data gaps & review notes
└── site-map.md              # Navigation outline (this file)
```

---

## 2. Section Map (index.html)

The website is designed as a premium, single-page application (SPA) with a sleek modern layout:

1.  **Header Navigation**
    *   Logo: `AiMY`
    *   Links: `Journey Overview` | `Module Explorer` | `New Releases` | `Continuous Loop`
    *   Call to Action: `Book a Demo` (Triggers a popup calendar placeholder)

2.  **Hero Section**
    *   Large HSL gradients, sleek dark mode aesthetics.
    *   Sales pitch headline & subheadline.
    *   Actionable CTAs: `Explore Live Catalogue` and `Watch Onboarding Walkthrough`.

3.  **Day 0 vs Day 30 Experience Comparison**
    *   Interactive side-by-side cards highlighting the structural operational improvements of AiMY (Before vs. After).

4.  **Interactive Onboarding Timeline**
    *   Interactive 4-week timeline component displaying the modular activation steps.

5.  **Interactive Module Catalogue**
    *   A grid of interactive cards representing the 6 modules: `Knowledge`, `Voice`, `QA`, `Connect`, `Sales`, and `Talent`.
    *   Clicking a card opens a modal overlay showing:
        *   Module summary & problem solved
        *   Integrations connected
        *   **Live Jira Proof:** Interactive, searchable lists of active released and upcoming tickets.

6.  **New Releases Section**
    *   Highlights the newly released features (e.g. FAQ system, conversational search, automated loop).

7.  **Continuous Improvement Loop Flow**
    *   Visual representation of the closed operational circle.

8.  **Footer**
    *   Copyright, review status, and contact links.
