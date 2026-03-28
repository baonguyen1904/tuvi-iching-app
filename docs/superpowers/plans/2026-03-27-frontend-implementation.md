# Frontend Implementation Plan — TuVi AI

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a complete Next.js frontend for TuVi AI with 5 pages (landing, form, processing, result, dimension detail), design system, charts, and API integration.

**Architecture:** Next.js 15+ App Router with TypeScript. Server Components for static/SEO content, Client Components for interactivity. shadcn/ui for complex primitives, custom components for design system alignment. Recharts for all chart types.

**Tech Stack:** Next.js 15+, TypeScript, Tailwind CSS, shadcn/ui, Recharts, react-markdown, rehype-raw, Sonner, Lucide React, date-fns

**Design Spec:** [`docs/superpowers/specs/2026-03-27-frontend-design-spec.md`](../specs/2026-03-27-frontend-design-spec.md) (v1.2, split into 5 parts)

---

## Plan Parts

| Part | File | Tasks | Contents |
|------|------|-------|----------|
| 1 | [tasks-01-05-setup-landing-form.md](frontend/tasks-01-05-setup-landing-form.md) | 1-5 | Project setup, design system, API client, landing page, input form |
| 2 | [tasks-06-09-pages-charts.md](frontend/tasks-06-09-pages-charts.md) | 6-9 | Processing screen, chart components, result overview, dimension detail |
| 3 | [tasks-10-12-polish.md](frontend/tasks-10-12-polish.md) | 10-12 | Error boundaries, loading skeletons, accessibility, mobile testing |

---

## Task Overview (12 tasks, 12 commits)

| Task | Name | Key Files | Commit |
|------|------|-----------|--------|
| 1 | Project Setup | Next.js init, shadcn, deps, config | `feat: init Next.js 15 project` |
| 2 | Design System | tokens, types, constants, utils, tailwind | `feat: add design system foundation` |
| 3 | API Client + Mock Data | api.ts, mock-data.ts, utils.test.ts | `feat: add API client and mock data` |
| 4 | Landing Page | layout.tsx, page.tsx, 10 landing components | `feat: add landing page with all 9 sections` |
| 5 | Input Form | BirthInputForm, DatePickerField, validation | `feat: add input form with validation` |
| 6 | Processing Screen | ProcessingScreen, StepIndicator, FunFactRotator | `feat: add processing screen with polling` |
| 7 | Chart Components | 5 Recharts components + chartConfig | `feat: add chart components` |
| 8 | Result Overview | 10 result components (cards, badges, feedback) | `feat: add result overview page` |
| 9 | Dimension Detail | 6 detail components (charts, AI text, nav) | `feat: add dimension detail page` |
| 10 | Error Boundaries | 5 error.tsx + 3 loading.tsx | `feat: add error boundaries and loading skeletons` |
| 11 | Accessibility | ARIA labels, skip link, semantic HTML | `feat: add accessibility` |
| 12 | Mobile Polish | Responsive verification, Lighthouse audit | `feat: mobile polish and final fixes` |

---

## Execution Order

Tasks 1-5 must be sequential (each builds on the previous).

Tasks 6-9 can be parallelized after Task 5:
- Task 6 (Processing) + Task 7 (Charts) can run in parallel
- Task 8 (Result) depends on Task 7 (uses chart components)
- Task 9 (Detail) depends on Tasks 7 + 8

Tasks 10-12 are sequential and run after Tasks 6-9.

```
1 → 2 → 3 → 4 → 5 → 6 ─┐
                          ├→ 8 → 9 → 10 → 11 → 12
                     5 → 7 ┘
```

---

## Spec Reference Map

| Task | Reads Spec Part |
|------|----------------|
| 1-3 | [01-design-system.md](../specs/frontend/01-design-system.md) |
| 4-5 | [02-landing-form.md](../specs/frontend/02-landing-form.md) |
| 6, 8 | [03-processing-result.md](../specs/frontend/03-processing-result.md) |
| 7, 9 | [04-detail-charts.md](../specs/frontend/04-detail-charts.md) |
| 10-12 | [05-api-a11y-perf.md](../specs/frontend/05-api-a11y-perf.md) |

---

## Critical Rules (from CLAUDE.md)

1. **8 dimensions:** van_menh + 7 (su_nghiep, tien_bac, hon_nhan, suc_khoe, dat_dai, hoc_tap, con_cai)
2. **van_menh:** has charts, NO alerts, interpretation=null (placeholder)
3. **Alerts use amber (NOT red)** for negative
4. **Date range:** 1920 to currentYear (dynamic)
5. **Mobile-first** design, test at 375px
6. **All dimensions pre-generated** — no lazy loading
