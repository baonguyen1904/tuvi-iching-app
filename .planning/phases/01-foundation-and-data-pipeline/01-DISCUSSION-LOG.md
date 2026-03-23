# Phase 1: Foundation and Data Pipeline - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-03-23
**Phase:** 01-foundation-and-data-pipeline
**Areas discussed:** Scraper strategy, Input form behavior, Cache design, Project structure
**Mode:** Auto (all decisions auto-selected based on recommended defaults)

---

## Scraper Strategy

| Option | Description | Selected |
|--------|-------------|----------|
| Playwright browser automation | Full browser automation to handle JS-rendered cohoc.net | ✓ |
| httpx direct HTTP calls | Lighter but only works if site has a hidden API | (check first) |
| Build own la so calculator | Eliminate scraper dependency entirely | |

**User's choice:** [auto] Playwright as primary, but inspect network tab first for hidden XHR API
**Notes:** Research confirmed cohoc.net is JS-rendered. Direct httpx would fail on the chart container. Network inspection is the first implementation task.

---

## Input Form Behavior

| Option | Description | Selected |
|--------|-------------|----------|
| Solar calendar only | Users enter duong lich, system converts | ✓ |
| Dual calendar toggle | Users can switch between solar and lunar input | |
| Default canh gio Ty for unknown | Produces valid chart with disclaimer | ✓ |
| Skip time-dependent calculations | More accurate but incomplete chart | |

**User's choice:** [auto] Solar-only input with system conversion; default to Ty for unknown time with disclaimer
**Notes:** Most users know their solar birthday. Lunar input adds complexity without clear MVP value.

---

## Cache Design

| Option | Description | Selected |
|--------|-------------|----------|
| SQLite database | Persistent, queryable, works on Railway | ✓ |
| In-memory (Redis/dict) | Fast but lost on restart | |
| Filesystem (JSON files) | Simple but not queryable | |

**User's choice:** [auto] SQLite with SHA-256 hash of normalized birth data as cache key
**Notes:** No cache expiry needed — Tu Vi charts are deterministic. Cache key doubles as shareable URL identifier.

---

## Project Structure

| Option | Description | Selected |
|--------|-------------|----------|
| Monorepo (/frontend + /backend) | Single repo, simple for 1 developer | ✓ |
| Separate repos | Independent deploy cycles | |
| Full-stack Next.js | API routes in Next.js, no separate backend | |

**User's choice:** [auto] Monorepo with /frontend (Next.js) and /backend (FastAPI) at root
**Notes:** Full-stack Next.js considered but Python is needed for scraping/scoring logic. Separate repos adds overhead for 1 developer.

---

## Claude's Discretion

- Playwright timing/wait strategies
- SQLite schema design
- Vietnamese error message wording
- vnlunar integration approach
- Backend/frontend scaffolding details

## Deferred Ideas

None — discussion stayed within phase scope
