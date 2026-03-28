# Frontend Design Spec — TuVi AI (Index)

**Date:** 2026-03-27 | **Version:** 1.2 | **Status:** Approved

**Stack:** Next.js 15+ (App Router, TypeScript), Tailwind CSS, shadcn/ui, Recharts

---

## Design Decisions — Overrides from Task 04

| Decision | This Spec | Task 04 | Rationale |
|----------|-----------|---------|-----------|
| Dimension detail routing | Separate routes `/result/[id]/[dimension]` | Accordion | Direct linking, cleaner URL |
| Dimensions in overview | 8 including `van_menh` | 7 axes | CLAUDE.md Rule 4 |
| Charts per dimension | 3 (Lifetime + Decade + Monthly) | 2 | Monthly data is core feature |
| Date range | 1920 to `currentYear` (dynamic) | 1920-2010 | Future-proof |

---

## Spec Parts

| Part | File | Contents |
|------|------|----------|
| 1 | [01-design-system.md](frontend/01-design-system.md) | Color tokens, typography, spacing, shadows, icons, shadcn mapping, TypeScript types |
| 2 | [02-landing-form.md](frontend/02-landing-form.md) | Landing page (9 sections), Input form (4 fields, validation, submit) |
| 3 | [03-processing-result.md](frontend/03-processing-result.md) | Processing screen (polling, steps), Result overview (profile, charts, cards, feedback) |
| 4 | [04-detail-charts.md](frontend/04-detail-charts.md) | Dimension detail page, Recharts config (Lifetime, Decade, Monthly, Radar, Bar) |
| 5 | [05-api-a11y-perf.md](frontend/05-api-a11y-perf.md) | API client, responsive rules, interactions, accessibility, performance, file structure, config |

---

## Quick Reference

- **8 dimensions:** su_nghiep, tien_bac, hon_nhan, suc_khoe, dat_dai, hoc_tap, con_cai, van_menh
- **van_menh:** has charts, NO alerts, interpretation=null (placeholder)
- **Alerts:** amber (NOT red) for negative, emerald for positive
- **Mobile breakpoint:** 640px (Tailwind `sm`)
- **Max content width:** 768px
