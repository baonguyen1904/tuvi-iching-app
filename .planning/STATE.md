# Project State: Kinh Dich x Tu Vi — AI Luan Giai MVP

---

## Project Reference

**Core Value**: User enters birth data and receives an accurate, personalized, expert-level Tu Vi interpretation that is empowering — powered by AI but grounded in validated scoring logic and expert-curated knowledge.

**Current Focus**: Phase 1 — Foundation and Data Pipeline

**Milestone**: M1 — MVP (test with ~20-50 expert clients)

---

## Current Position

**Phase**: 1 — Foundation and Data Pipeline
**Plan**: None started
**Status**: Not started
**Progress**: [ ][ ][ ] 0/3 phases complete

```
Phase 1 [         ] Not started
Phase 2 [         ] Not started
Phase 3 [         ] Not started
```

---

## Performance Metrics

**Plans completed**: 0
**Requirements satisfied**: 0/36
**Phases complete**: 0/3

---

## Accumulated Context

### Key Decisions Made

| Decision | Rationale | Status |
|----------|-----------|--------|
| Next.js 16 frontend + FastAPI backend | SSR for shareable result pages; Python owns scraper/scoring/AI pipeline | Pending confirmation |
| Playwright-based cohoc.net scraper | Site is JS-rendered; static HTTP requests return empty charts | Pending confirmation |
| vnlunar for calendar conversion | Vietnamese calendar diverges from Chinese for specific years | Pending confirmation |
| Claude Sonnet API (claude-sonnet-4-5) | Vietnamese quality, 200K context for inline KB injection | Pending confirmation |
| Inline KB injection (no RAG) | Full KB fits within context window; RAG adds complexity with no benefit | Pending confirmation |
| SQLite cache keyed on birth data hash | MVP only needs la so caching; maps to opaque UUID for shareable URLs | Pending confirmation |
| Recharts for score visualization | SVG-based, well-documented; verify version 3.8.0 with npm | Pending confirmation |
| Vercel (frontend) + Railway (backend) | Fast, cheap deployment; Railway is always-on (required for scraper) | Pending confirmation |
| No auth for MVP | Reduce friction; shareable links solve "save" need for test group | Pending confirmation |
| On-demand per-dimension AI generation | Avoids 7 concurrent Claude calls on page load; cuts API cost | Pending confirmation |
| Direct EventSource to FastAPI (not proxied through Next.js) | Vercel buffers SSE; must connect React directly to Railway endpoint | Pending confirmation |
| Opaque UUID in shareable URL (not birth data hash) | Prevents birth data exposure in URL; retrofitting is high-cost | Pending confirmation |

### Critical Risks to Track

- **cohoc.net scraper**: Primary single point of failure. JS-rendered, no SLA. `g_token_key` mechanism unknown — requires browser DevTools inspection before committing to scraping approach.
- **AI hallucination**: Must be constrained to stars present in user's chart via structured data blocks + post-generation cross-check.
- **AI tone**: Three-level enforcement required (system prompt prohibition list + few-shot examples + post-generation vocabulary scan). Expert sign-off required before user testing.
- **Scoring port accuracy**: Must be validated against expert's Google Sheets for 20+ test cases before AI generation phase begins.
- **Expert availability**: Knowledge base authoring is gated on expert partner (~5h total, 3 sessions). Confirm scheduling before starting Phase 2.

### Todos

- [ ] Confirm expert partner availability windows before starting Phase 2
- [ ] Inspect cohoc.net `g_token_key` mechanism via browser DevTools before committing to scraper implementation
- [ ] Get access to expert's Google Sheets scoring logic before starting Phase 2
- [ ] Verify recharts version: `npm view recharts version`
- [ ] Confirm Node.js version >= 20.9 in dev environment (Next.js 16 requirement)

### Blockers

None currently.

---

## Session Continuity

**Last session**: 2026-03-23 — Project initialized, roadmap created
**Next action**: Begin Phase 1 planning via `/gsd:plan-phase 1`

---

*Last updated: 2026-03-23 after roadmap creation*
