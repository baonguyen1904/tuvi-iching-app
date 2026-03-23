# Phase 1: Foundation and Data Pipeline - Context

**Gathered:** 2026-03-23
**Status:** Ready for planning

<domain>
## Phase Boundary

Users can submit birth data (date, time, gender, optional name) and the system produces a validated la so (Tu Vi chart) with all 14 chinh tinh and phu tinh placed across 12 cung. Includes solar-to-lunar calendar conversion, cohoc.net scraping, caching, and error handling. Scoring, AI generation, and result display are separate phases.

</domain>

<decisions>
## Implementation Decisions

### Scraper strategy
- **D-01:** Use Playwright (Python) for browser automation — cohoc.net is JS-rendered, httpx/requests will return empty chart containers
- **D-02:** First step in implementation: inspect cohoc.net network tab for hidden XHR/fetch API endpoints. If a clean JSON API exists behind the form submission, use direct HTTP calls (httpx) instead of full browser automation — faster and more stable
- **D-03:** If Playwright is needed: submit the form programmatically, wait for chart DOM to populate, then parse HTML for sao placements
- **D-04:** Centralize all HTML selectors in a single module so breakage is detected and fixed in one place
- **D-05:** Implement retry logic (3 attempts) with circuit breaker pattern for scraper resilience

### Input form behavior
- **D-06:** Solar calendar (duong lich) date picker only — system handles conversion to am lich internally
- **D-07:** Birth time: dropdown of 12 canh gio plus "Khong ro" (unknown) option
- **D-08:** When user selects "Khong ro": use default canh gio Ty (23:00-01:00) and display a disclaimer that time-dependent calculations may vary
- **D-09:** Gender: two options — Nam/Nu (no other/prefer not to say for traditional Tu Vi system)
- **D-10:** Name field is optional, used only for display on result page
- **D-11:** Validation: date is required, time defaults to "Khong ro" if not selected, gender is required

### Cache design
- **D-12:** SQLite database for la so caching — persistent, works on Railway, queryable
- **D-13:** Cache key: SHA-256 hash of normalized birth data (ISO date string + canh gio code + gender)
- **D-14:** Cache stores: raw scraped HTML, parsed la so structure (12 cung x sao placements), and Cung Menh
- **D-15:** Same cache key also serves as the shareable result URL identifier (used in Phase 3)
- **D-16:** No cache expiry for la so data — Tu Vi charts are deterministic (same input = same chart forever)

### Project structure
- **D-17:** Single monorepo with `/frontend` (Next.js) and `/backend` (FastAPI) directories at root
- **D-18:** Backend is the primary deliverable for Phase 1 — API endpoints for la so generation
- **D-19:** Frontend in Phase 1 is minimal: input form that POSTs to backend API, receives la so confirmation
- **D-20:** Shared types/schemas: backend defines the la so data schema (Pydantic models), frontend consumes JSON

### Claude's Discretion
- Exact Playwright page interaction timing and wait strategies
- SQLite schema design details (table structure, indexes)
- Error message wording (must be in Vietnamese, friendly tone)
- vnlunar library integration approach for am lich conversion
- Backend project scaffolding (FastAPI directory structure, dependency management)
- Frontend scaffolding choices (App Router vs Pages Router — though App Router is standard for Next.js 16)

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project context
- `gsd_project_prompt.md` — Full project brief with business logic domains, technical decisions, and constraints
- `docs/mvp_scope_ai_agent_plan.md` — MVP scope definition, user flow, AI agent architecture, development plan
- `docs/research_plan_kinh_dich_tu_vi_app.md` — Market research, competitive landscape, technical architecture concepts

### Research findings
- `.planning/research/STACK.md` — Technology stack recommendations with verified versions (Playwright, vnlunar, FastAPI, Next.js 16)
- `.planning/research/ARCHITECTURE.md` — System architecture, component boundaries, data flow, build order
- `.planning/research/PITFALLS.md` — Critical pitfalls including scraper fragility, am lich intercalary months, and Vercel SSE buffering

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- None — greenfield project, no existing code

### Established Patterns
- None — patterns will be established in this phase

### Integration Points
- Backend API will be consumed by frontend (Phase 1 minimal) and later by AI engine (Phase 3)
- La so data schema defined here becomes the contract for scoring engine (Phase 2) and AI generation (Phase 3)
- Cache key/ID becomes the shareable URL identifier (Phase 3)

</code_context>

<specifics>
## Specific Ideas

- cohoc.net scraping target: tuvi.cohoc.net/lap-la-so-tu-vi.html — POST birth data to this form
- vnlunar 1.1.1 is the correct Vietnamese lunar calendar library (NOT Chinese calendar libraries — documented divergences exist)
- The la so data structure must capture: 12 cung names, sao list per cung (chinh tinh + phu tinh), Cung Menh identification
- Research flagged a `g_token_key` mechanism on cohoc.net that may need browser DevTools inspection to understand

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 01-foundation-and-data-pipeline*
*Context gathered: 2026-03-23*
