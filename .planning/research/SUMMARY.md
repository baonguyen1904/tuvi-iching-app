# Project Research Summary

**Project:** Vietnamese Tu Vi AI Interpretation Web App (TuViApp)
**Domain:** AI-powered Vietnamese astrology (Tu Vi) interpretation system
**Researched:** 2026-03-23
**Confidence:** HIGH

## Executive Summary

This is a specialized AI-powered astrology interpretation product targeting Vietnamese-speaking users who want expert-quality narrative readings of their Tu Vi birth chart (la so). The standard expert approach is a two-stage pipeline: (1) generate the la so (12-palace birth chart with star placements) from birth data, then (2) apply a domain-specific scoring engine to derive life-dimension scores and alerts that ground an AI narrative generation step. The critical dependency chain — birth data input → lunar calendar conversion → la so chart generation (via cohoc.net scraper) → scoring engine → AI luan giai per dimension — must be built strictly in that order. No step can be bypassed.

The recommended architecture is a Next.js 16 frontend (App Router, Tailwind v4) consuming a FastAPI backend (Python 3.12), with the backend hosting the Playwright-based scraper, vnlunar calendar converter, Python scoring engine, and Claude API integration for streaming AI narrative. The knowledge base for AI grounding consists of 7 curated markdown files (one per life dimension) that are injected inline into prompts — no RAG pipeline is needed given the KB fits well within Claude's context window. La so results are cached by a hash of birth inputs, enabling both performance and shareable URLs via opaque UUIDs.

The two highest-risk areas are: (1) the cohoc.net scraper dependency — the site is JavaScript-rendered and has no SLA, making it the primary single point of failure; and (2) AI tone and grounding — without explicit multi-level tone enforcement and post-generation star-name validation, the AI will produce fear-inducing language and hallucinate star combinations not present in the user's chart. Both risks must be addressed with preventive architecture from day one, not as post-MVP patches. The scoring engine port from Google Sheets must be validated against expert data before any AI generation is attempted.

---

## Key Findings

### Recommended Stack

The stack is purpose-built around two constraints: (1) the la so calculation ecosystem is Python-native (vnlunar, Playwright, BeautifulSoup, the Google Sheets scoring port), and (2) the frontend needs SSR for shareable result pages with good performance. This makes a Next.js + FastAPI split the correct architecture — not a pure Next.js app. See [STACK.md](.planning/research/STACK.md) for full detail.

**Core technologies:**
- **Next.js 16.2.1 + React 19**: Frontend framework — App Router for SSR on shareable result pages; SSE streaming compatible via Route Handlers
- **FastAPI 0.135.2 + Python 3.12**: Backend API — async-first, natural home for the Python scraping/scoring/AI pipeline
- **Pydantic 2.12.5**: Data validation — defines la so response schemas and Claude structured output parsing
- **anthropic SDK 0.86.0**: Claude API client — async streaming, structured output via `client.beta.messages.parse()`; claude-sonnet-4-5 validated for Vietnamese
- **Playwright 1.58.0 + BeautifulSoup 4.14.3**: La so scraping — cohoc.net is JavaScript-rendered; Playwright is the only viable scraping approach
- **vnlunar 1.1.1**: Vietnamese lunar calendar conversion — do not substitute Chinese calendar libraries; Vietnamese calendar diverges from Chinese for specific years
- **Tailwind CSS 4.x**: Styling — CSS-first config, default with create-next-app for Next.js 16
- **Recharts 3.8.0**: Score visualization — SVG-based line charts for Duong/Am/TB timelines per dimension

**Critical version constraints:**
- Next.js 16 requires Node.js 20.9+ (Node 18 is dropped)
- FastAPI 0.135.2 requires Pydantic v2; Pydantic v1 is incompatible
- Use Railway for backend (always-on); Vercel for frontend (native Next.js host)

### Expected Features

The MVP is well-defined and scoped. The 7-dimension interpretation (su nghiep, tien bac, hon nhan, suc khoe, dat dai, hoc tap, con cai) with on-demand streaming AI narrative is the core value proposition. See [FEATURES.md](.planning/research/FEATURES.md) for full detail.

**Must have (table stakes):**
- Birth data input form with solar/lunar calendar toggle and intercalary month support
- Duong lich to Am lich conversion — wrong conversion produces a completely wrong chart
- La so generation (cohoc.net scraper) — this IS the product
- 12-cung grid chart visualization — standard Tu Vi display format expected by all users
- AI luan giai per dimension (on-demand, streaming) — core value proposition
- Tong quan van menh overview — cross-dimension synthesis that completes the reading
- Scoring visualization: Duong/Am/TB line charts per dimension
- Alert detection and markers on timeline charts
- Vietnamese-only UI with empowering (non-fear-inducing) tone
- Mobile-responsive layout — test group accesses on mobile
- Shareable result URLs with opaque IDs (no login required)
- La so caching — prevents repeat scrapes, enables shareable URLs
- Graceful error handling for cohoc.net failures

**Should have (competitive differentiators):**
- On-demand per-dimension generation (reduces initial load, cuts API cost)
- Streaming AI responses (makes generation feel live, not a dump)
- Alert markers overlaid on timeline charts (unique in market)
- Multi-step loading progress indicator ("Đang lập lá số..." → "Đang phân tích...")

**Defer (v2+):**
- User accounts / saved readings — shareable URLs solve the "save" need for MVP
- Two-level explanation depth (basic vs. in-depth) — deferred until KB is deep enough
- Chatbot / conversational follow-up — changes product category, high cost
- Compatibility / partner chart comparison — separate domain
- PDF export, native app, bilingual support — all low value for MVP test group

### Architecture Approach

The system splits cleanly into two parallel tracks: the data pipeline (scraper → converter → scoring engine → cache → chart endpoint) and the AI generation pipeline (knowledge base → AI engine → SSE streaming endpoint). The result page loads chart data from the first track immediately; AI narrative for each dimension is generated on-demand via the second track when the user clicks a dimension tab. See [ARCHITECTURE.md](.planning/research/ARCHITECTURE.md) for full detail.

**Major components:**
1. **Scraper Module** (`services/scraper.py`) — Playwright-based cohoc.net scraper, isolated behind a circuit breaker interface; replaceable without touching other services
2. **Lunar Converter** (`services/lunar.py`) — pure function, vnlunar-based, handles intercalary months and Vietnamese GMT+7 timezone
3. **Scoring Engine** (`services/scoring.py`) — deterministic port of Google Sheets logic; pure Python function, fully unit-testable
4. **Alert Detection** (`services/alerts.py`) — sao combination rules producing tagged alert flags; required input to AI engine
5. **AI Engine** (`services/ai_engine.py`) — builds dimension prompt (KB inline injection + scores + alerts + la so), calls Claude API, yields SSE chunks
6. **Cache Layer** (`db/cache.py`) — SQLite keyed on `sha256(birth_params)[:16]`; maps to UUID for shareable URLs; stores la so + scores + alerts (not AI narratives)
7. **Knowledge Base** (`knowledge_base/*.md`) — 7 dimension markdown files + core_stars.md; loaded inline per request, no vector DB
8. **Next.js Frontend** — Input form, result page (`/result/[id]`), dimension detail pages with SSE consumer component

**Key architectural decisions:**
- Inline KB injection over RAG — entire KB (~20-40K tokens) fits in Claude's 200K context window; RAG adds complexity with no benefit
- Birth data hash as both cache key and shareable ID — no auth required; opaque UUID in URL prevents birth data exposure
- On-demand per-dimension AI generation — avoids 7 concurrent Claude API calls on page load
- Frontend connects directly to FastAPI for SSE — never proxy streaming through Next.js API routes (Vercel buffers SSE)

### Critical Pitfalls

See [PITFALLS.md](.planning/research/PITFALLS.md) for full detail including recovery strategies and a verification checklist.

1. **cohoc.net is JavaScript-rendered — `requests` returns empty charts** — Use Playwright from day one; never attempt a static HTTP scraper. Validate by checking that all 14 chinh tinh appear across 12 cung for at least 5 known birth inputs before proceeding to scoring.

2. **AI generates content not grounded in the user's chart** — Pass sao placements in XML-tagged structured data blocks; add explicit "only reference stars listed in `<chart_data>`" constraint; run post-generation cross-check that all named stars exist in chart data.

3. **AI uses fear-inducing language despite tone instructions** — Implement tone enforcement at three levels: (1) explicit prohibition list in system prompt, (2) 2-3 few-shot examples per negative alert category, (3) prohibited vocabulary scan post-generation. Expert partner must sign off before user testing.

4. **Google Sheets scoring logic ports incorrectly** — Treat the Sheets as a test oracle: run 10+ known la so through both and assert exact score equality. Use `decimal.Decimal` for arithmetic; normalize sao name Unicode (NFC); raise explicit errors on missing lookup keys.

5. **Vietnamese intercalary month mis-classification** — Use vnlunar (not Chinese calendar libraries); expose a "tháng nhuận" checkbox in the input form; test with known leap-month birth dates (e.g., 1985 leap month 2, 1995 leap month 8).

6. **Streaming truncated by Vercel/proxy** — Connect React EventSource directly to the Railway FastAPI endpoint; never proxy SSE through Next.js API routes. Set `X-Accel-Buffering: no`; send keep-alive pings every 15 seconds. Verify in deployed staging before user testing.

7. **Shareable URLs expose birth data** — Use opaque UUIDs as URL keys from the start; map to birth data server-side in cache. Retrofitting opaque IDs after URLs have been shared is high-cost.

---

## Implications for Roadmap

The research reveals a clear dependency chain that dictates phase order. The critical path is: scraper → calendar converter → scoring engine → chart API endpoint → frontend result page. AI generation (KB + AI engine + streaming endpoint) can be developed in parallel once the la so data structure is defined after the scraper phase. Knowledge base authoring is expert-dependent and should begin as a parallel track immediately.

### Phase 1: Project Setup and Infrastructure

**Rationale:** All subsequent phases require a functioning dev environment with both frontend and backend running and communicating. Establishing the monorepo structure, deployment targets (Vercel + Railway), and environment configuration early eliminates infrastructure surprises during feature development.

**Delivers:** Working Next.js + FastAPI skeleton deployed to staging; `POST /api/chart` stub returning mock data; basic input form rendering.

**Addresses:** Core infrastructure dependency for all features

**Avoids:** Discovering Vercel/Railway configuration issues mid-feature development; SSE streaming proxy pitfall (establish direct FastAPI-to-frontend SSE connection before building streaming feature)

### Phase 2: Data Pipeline (Scraper + Calendar Converter)

**Rationale:** This is the most uncertain phase — cohoc.net is an external dependency with no SLA, and the Vietnamese calendar converter must handle intercalary months correctly. Everything downstream (scoring, AI) depends on valid la so data. Validating this pipeline before building anything else prevents propagating bad data through the system.

**Delivers:** Playwright-based cohoc.net scraper returning validated la so struct; vnlunar-based Am lich converter with intercalary month support; schema validation asserting 14 chinh tinh across 12 cung; circuit breaker pattern wrapping scraper.

**Addresses:** La so generation, lunar/solar calendar conversion, graceful error handling

**Avoids:** Pitfalls 1 (JS-rendered scraper), 3 (intercalary month), 5 (HTML structure change validation); all "Looks Done But Isn't" scraper and converter checklist items

**Research flag:** NEEDS PHASE RESEARCH — cohoc.net's exact form submission mechanism (`g_token_key` handling) and DOM structure require inspection via browser DevTools before implementation; scraper logic cannot be fully designed from documentation alone.

### Phase 3: Scoring Engine

**Rationale:** The scoring engine is the domain logic core — a pure Python port of the expert's Google Sheets logic. It must be built and validated against known expert data before any AI generation can be attempted. Getting this wrong invalidates all AI interpretations silently.

**Delivers:** Python scoring engine producing Duong/Am/TB scores per dimension + alert flags for sao combinations; parity-tested against 10+ known la so from expert's Sheets; `pytest` test suite with exact equality assertions.

**Addresses:** Scoring engine (7 dimensions), alert detection

**Avoids:** Pitfall 6 (scoring logic port errors) — parity tests are the gate before this phase is considered done; silent None/0 returns on missing lookup keys

**Research flag:** STANDARD PATTERNS — Python dict lookup tables, decimal arithmetic, Unicode normalization are all well-documented; no external research needed beyond the expert's Sheets as oracle.

### Phase 4: Knowledge Base Authoring (Expert-Led, Parallel Track)

**Rationale:** KB authoring is expert-dependent, not engineering-dependent. It should begin as soon as the la so data structure is defined (after Phase 2 produces the scraper output schema). Running this in parallel with Phase 3 prevents a KB bottleneck from blocking the AI engine phase.

**Delivers:** 7 dimension markdown files (su_nghiep, tien_bac, hon_nhan, suc_khoe, dat_dai, hoc_tap, con_cai) + core_stars.md reference file; expert-validated content; tone exemplars for each dimension's negative alert categories (required for Phase 5 tone enforcement).

**Addresses:** Knowledge base (AI grounding), empowering tone (non-fear-inducing content examples)

**Avoids:** Pitfall 4 (AI hallucination) — KB files define the boundary of permissible AI content; Pitfall 5 (fear-inducing tone) — tone exemplars authored here become the few-shot examples in Phase 5 prompts

**Research flag:** EXPERT-GATED — this phase cannot proceed without scheduled expert sessions; plan expert availability before starting Phase 3.

### Phase 5: AI Luan Giai Engine

**Rationale:** Only buildable after Phase 2 (la so data structure), Phase 3 (scoring output structure), and Phase 4 (KB files exist). This phase implements the product's core value: streaming AI narrative per dimension with expert-quality grounding.

**Delivers:** `services/ai_engine.py` with inline KB injection, structured prompt per dimension, Claude API streaming; `POST /api/luangiai/{id}/{dimension}` SSE endpoint; post-generation validation (star-name cross-check + prohibited vocabulary scan); expert partner sign-off on 3 sample outputs per dimension category.

**Addresses:** AI luan giai per dimension (on-demand, streaming), tong quan van menh overview

**Avoids:** Pitfall 4 (hallucination) — structured data blocks + grounding constraint + post-generation validation; Pitfall 5 (tone) — three-level enforcement with few-shot examples and vocabulary scan; Pitfall 8 (prompt injection) — user input passed inside XML delimiters

**Research flag:** STANDARD PATTERNS — Claude API streaming, inline KB injection, and SSE FastAPI are well-documented; tone enforcement and grounding constraint patterns are documented in Anthropic's official docs.

### Phase 6: Cache, URLs, and Result Page

**Rationale:** Caching and shareable URLs are tightly coupled — the URL scheme must be designed before the result page is built, as the URL key structure affects both cache lookup logic and privacy. Designing the URL as an opaque UUID from the start (not birth data hash in URL) prevents a costly retrofit.

**Delivers:** SQLite cache keyed on birth data hash; UUID-based shareable URLs (`/result/{uuid}`); `GET /api/result/{uuid}` returning cached la so + scores + alerts; result page rendering 12-cung grid chart and dimension navigation; la so caching preventing repeat scrapes.

**Addresses:** Caching, shareable result URLs, chart visualization (12-cung grid), results page

**Avoids:** Pitfall 7 (shareable URL privacy) — opaque UUID in URL by design; anti-pattern of storing AI narratives in cache (store only la so + scores)

**Research flag:** STANDARD PATTERNS — SQLite, UUID generation, Next.js dynamic routes are all standard.

### Phase 7: Scoring Visualization and Alerts UI

**Rationale:** Score timeline charts and alert markers are the most visually impactful differentiators. They can be built as a self-contained layer on top of the already-complete scoring and result page from Phase 6.

**Delivers:** Recharts line charts per dimension showing Duong/Am/TB score trajectories over lifetime and decade horizons; alert markers on timeline at relevant time periods; alert badge rendering (neutral/amber color, placed after narrative to avoid fixation on negative markers).

**Addresses:** Scoring visualization (Duong/Am/TB charts), alert markers on timeline

**Avoids:** UX pitfall of displaying alert badges prominently before empowering narrative; performance trap of streaming all 7 dimensions simultaneously

**Research flag:** STANDARD PATTERNS — Recharts is well-documented; the scoring data shape is defined in Phase 3.

### Phase 8: Streaming UI and On-Demand Generation

**Rationale:** This phase delivers the final UX layer: streaming text rendering, on-demand per-dimension generation, and the multi-step loading progress indicator. It depends on the SSE endpoint from Phase 5 and the result page structure from Phase 6.

**Delivers:** React SSE consumer component (`components/stream/`); on-demand dimension generation triggered by tab click; skeleton-to-streaming-text transition; multi-step progress indicator ("Đang lập lá số..." → "Đang phân tích sao..." → "Đang viết luan giai..."); end-to-end streaming verification in Vercel + Railway staging.

**Addresses:** Streaming AI responses, on-demand dimension generation, processing/loading screen

**Avoids:** Pitfall 2 (Vercel SSE truncation) — direct frontend-to-FastAPI SSE connection, verified in staging; performance trap of pre-fetching all 7 dimensions; UX pitfall of blank screen with no progress feedback

**Research flag:** STANDARD PATTERNS — EventSource API and streaming text rendering are documented; however, Vercel SSE proxy behavior should be tested early in this phase before building full UI.

### Phase 9: Mobile Polish, Error Handling, and Launch Readiness

**Rationale:** Final hardening pass before expert partner testing with the 20-50 user test group. Ensures mobile layout, graceful error handling, and all "Looks Done But Isn't" checklist items are verified.

**Delivers:** Mobile-responsive layout (12-cung grid on small screens); graceful error handling for cohoc.net unavailability (Vietnamese message + retry button); input form summary/confirmation step showing "Ngày sinh: 15/03/1985 (dương lịch)" before generation; security review (no birth data in logs, no system prompt in API responses, rate limiting on scraper endpoint); all PITFALLS.md verification checklist items passing.

**Addresses:** Mobile-responsive layout, graceful error handling, Vietnamese-only UI, security

**Avoids:** UX pitfall of generic error messages; security mistake of logging raw birth data; prompt injection via birth data fields

**Research flag:** STANDARD PATTERNS — Tailwind responsive design, rate limiting on FastAPI are standard.

### Phase Ordering Rationale

- **Phases 2-3 must precede Phase 5** because the AI engine requires both the la so data structure (from scraper) and the scoring output schema (from scoring engine) to build prompts correctly.
- **Phase 4 (KB authoring) is the only expert-dependent phase** and must run in parallel with Phases 2-3; expert availability is on the critical path for Phase 5.
- **Phase 6 (cache + URLs) must precede Phase 7-8** because result page structure, dimension navigation, and the URL scheme are shared dependencies.
- **The shareable URL scheme (Phase 6) must be decided before any URLs are shared** — retrofitting opaque IDs is high-cost (Pitfall 7).
- **Streaming verification (Phase 8) requires deployed staging** — local development masks Vercel SSE buffering; this test cannot be deferred to launch day.

### Research Flags

Phases needing deeper research during planning:
- **Phase 2 (Scraper):** cohoc.net's exact form submission mechanism requires browser DevTools inspection to determine if `g_token_key` is server-validated; DOM structure and selector strategy cannot be finalized from documentation alone.

Phases with standard patterns (skip research-phase):
- **Phase 1 (Setup):** Next.js + FastAPI scaffold, Vercel + Railway deployment — extensively documented by Vercel.
- **Phase 3 (Scoring Engine):** Pure Python dict/decimal logic — no external research needed.
- **Phase 5 (AI Engine):** Claude streaming + inline KB injection — official Anthropic docs sufficient.
- **Phase 6 (Cache + URLs):** SQLite + UUID + Next.js dynamic routes — standard patterns.
- **Phase 7 (Visualization):** Recharts line charts — library docs sufficient.
- **Phase 8 (Streaming UI):** EventSource + SSE — documented; early staging test is the key action, not research.
- **Phase 9 (Polish):** Tailwind responsive + FastAPI rate limiting — standard.

---

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | All versions verified from official sources on 2026-03-23; only exception is recharts 3.8.0 (MEDIUM — inferred from search results, not direct npm page) |
| Features | MEDIUM | MVP feature set is HIGH confidence (validated by expert partner via PROJECT.md); differentiator features and competitor analysis are MEDIUM (fewer authoritative Vietnamese Tu Vi app sources) |
| Architecture | HIGH | Patterns verified against official FastAPI, Next.js, and Anthropic docs; multiple implementation examples found for Next.js + FastAPI + SSE streaming |
| Pitfalls | HIGH | Scraper, calendar, streaming pitfalls verified from direct source inspection and official docs; scoring port and tone enforcement are MEDIUM (fewer direct analogues) |

**Overall confidence:** HIGH

### Gaps to Address

- **cohoc.net token mechanism** (`g_token_key`): The scraper research identified this as potentially server-validated but could not determine the full validation mechanism from static inspection. Must be resolved during Phase 2 via browser DevTools network inspection before committing to a scraping approach. Fallback: if token is required, direct XHR API call with httpx may be simpler than DOM scraping.

- **Scoring engine complexity**: The Google Sheets structure (laso_points lookup tables, Duong/Am/TB calculation formulas) has not been inspected directly. Complexity is estimated from domain description. Actual porting effort may vary significantly. Mitigate by: getting Sheets access before starting Phase 3 and reviewing formula depth in a pre-Phase-3 spike.

- **Expert partner availability**: Knowledge base authoring (Phase 4) and tone exemplar review (Phase 5) are gated on expert partner scheduling. This is the only non-engineering dependency on the critical path. Confirm expert availability windows before finalizing the roadmap timeline.

- **recharts 3.8.0 version**: MEDIUM confidence only — could not fetch npm page directly; inferred from search results. Verify with `npm view recharts version` before installation.

---

## Sources

### Primary (HIGH confidence)

- Official Next.js 16 blog posts (nextjs.org/blog) — Next.js 16.2.1 features and requirements
- PyPI verified packages (2026-03-23) — FastAPI, anthropic, playwright, pydantic, vnlunar, httpx, beautifulsoup4
- Anthropic Claude API docs — structured outputs, streaming, hallucination reduction, prompt injection prevention
- cohoc.net direct inspection (`tuvi.cohoc.net/lap-la-so-tu-vi.html`) — JS-rendered confirmation, form field names
- Tailwind CSS v4 + Next.js compatibility docs (tailwindcss.com/docs/guides/nextjs)
- Ho Ngoc Duc Vietnamese lunar calendar documentation (xemamlich.uhm.vn/calrules_en.html)
- Vercel Next.js SSE known issue (github.com/vercel/next.js/discussions/48427)
- OWASP LLM Prompt Injection Prevention Cheat Sheet

### Secondary (MEDIUM confidence)

- PROJECT.md expert partner requirements — validated feature requirements and domain constraints
- Thai Am - Tu Vi 2026 app listing — competitor feature analysis
- Sahansera.dev — Streaming APIs with FastAPI and Next.js implementation pattern
- Jaqpot.org — Building streaming LLM with Next.js, FastAPI
- Medium — Circuit Breaker Pattern in Python

### Tertiary (LOW confidence)

- Dev agency marketing content (apptunix, appquipo, webelight) — general astrology app feature lists; used only to triangulate table-stakes features, not as authoritative sources
- Competitor app listings (spark.mwm.ai) — product feature comparison only

---

*Research completed: 2026-03-23*
*Ready for roadmap: yes*
