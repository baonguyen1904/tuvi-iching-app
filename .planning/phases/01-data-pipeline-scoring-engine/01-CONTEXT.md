# Phase 1: Data Pipeline & Scoring Engine - Context

**Gathered:** 2026-03-24
**Status:** Ready for planning

<domain>
## Phase Boundary

Given any birth data input (ngày sinh, giờ sinh, giới tính), the system can:
1. Scrape lá số data from two sources (tuvi.cohoc.net for cả đời + 10 năm, tuvi.vn for 12 tháng)
2. Calculate per-dimension scores (Dương/Âm/TB) across all time periods
3. Detect alert triggers (🔺🔻) from sao combinations
4. Cache results to avoid re-scraping

</domain>

<decisions>
## Implementation Decisions

### Scraper Approach
- **D-01:** Keep Selenium + undetected-chromedriver approach from legacy codebase — proven to work with both cohoc.net and tuvi.vn
- **D-02:** Deploy via Docker container with headless Chrome — standard approach for Railway hosting
- **D-03:** Run scrapers sequentially (cohoc first, then tuvi.vn) — simpler, one Chrome instance

### Data Structure
- **D-04:** Keep legacy separate data structure — CungInfo with cung_chung, cung_10yrs (from cohoc.net), cung_12months (from tuvi.vn). Do NOT merge into unified schema.
- **D-05:** Port existing Pydantic schemas (CungDetail, CungInfo, LaSoTuVi, LaSoTuViInput) from legacy codebase

### Scoring Logic
- **D-06:** Export laso_points.xlsx → JSON lookup tables once, load JSON at Python startup. No xlsx dependency at runtime.
- **D-07:** Validate scoring port with automated pytest suite — 20+ test cases comparing Python output vs Sheet output

### Caching
- **D-08:** Use Supabase/Postgres for caching lá số results
- **D-09:** Split cache keys by source:
  - cohoc.net: key = ngày sinh + giờ sinh + giới tính (data never changes)
  - tuvi.vn: key = ngày sinh + giờ sinh + giới tính + năm xem (monthly data changes yearly)

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Legacy Scraper Code
- `/mnt/d/Working/TBTesu/tuvi/scraper/src/scrapers/tuvi_cohoc_scraper.py` — cohoc.net scraper (Selenium + BeautifulSoup, parse_body extracts 12 cung for cả đời + 10 năm)
- `/mnt/d/Working/TBTesu/tuvi/scraper/src/scrapers/tuvi_vn_scraper.py` — tuvi.vn scraper (Selenium + BeautifulSoup, extracts 12 cung for 12 tháng, sorted by month)
- `/mnt/d/Working/TBTesu/tuvi/scraper/src/schemas/__init__.py` — Pydantic schemas: CungDetail, CungInfo, LaSoTuVi, LaSoTuViInput
- `/mnt/d/Working/TBTesu/tuvi/scraper/src/soup_utils.py` — Shared HTML parsing utilities (find_metadata_field with Unicode normalization)
- `/mnt/d/Working/TBTesu/tuvi/scraper/src/constants.py` — LUNA_YEARS mapping, Chrome paths
- `/mnt/d/Working/TBTesu/tuvi/scraper/src/main.py` — FastAPI endpoints for scraper service (reference for API patterns)

### Scoring Data
- `/mnt/d/Working/TBTesu/tuvi/laso_points.xlsx` — Google Sheet scoring logic to port to JSON

### Project Docs
- `docs/mvp_scope_ai_agent_plan.md` — MVP scope, AI architecture, KB structure, development plan
- `docs/gsd_project_prompt.md` — Full project brief with 6 business logic domains

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **tuvi_cohoc_scraper.py**: Complete scraper with form filling, navigation waiting, IP rate-limit detection, processing page handling, HTML parsing for 12 cung × sao. Uses main_order/reversed_order arrays for Dương Nam/Âm Nữ cung ordering.
- **tuvi_vn_scraper.py**: Complete scraper with form filling, HTML parsing. Also has `get_la_so_url()` for direct POST without Selenium. Handles d-none hidden elements filtering.
- **soup_utils.py**: Robust metadata extraction with NFC Unicode normalization, supports both tuvi.cohoc (p > span) and tuvi.vn (td sibling) HTML layouts.
- **schemas/__init__.py**: Pydantic models ready to port — CungDetail(ten, sao, thang), CungInfo(cung_chung, cung_10yrs, cung_12months), LaSoTuVi, LaSoTuViInput.
- **constants.py**: LUNA_YEARS mapping (2022-2043), GIO_SINH time ranges for 12 canh giờ.

### Established Patterns
- Selenium WebDriverWait for page load detection
- undetected-chromedriver for Cloudflare bypass
- Unicode NFC normalization throughout (critical for Vietnamese text matching)
- JSON file dump for caching (to be replaced with Supabase)

### Integration Points
- FastAPI as the API framework (existing pattern in legacy)
- Pydantic for request/response validation
- Two separate endpoints: `/la-so-tu-vi` (cohoc) and `/la-so-tu-vi-thang` (tuvi.vn) — may consolidate into single endpoint

</code_context>

<specifics>
## Specific Ideas

- The scoring logic lives in `laso_points.xlsx` as lookup tables — each sao has predefined point values per dimension
- Points categorized as Dương (positive), Âm (negative), TB (neutral)
- Scores calculated for: cả đời (lifetime, 10-year blocks), 10 năm (decade, yearly), 12 tháng (monthly)
- Alert triggers fire when certain sao combinations align at specific time periods
- Legacy main.py shows the integration pattern: scrape → save JSON → return data

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 01-data-pipeline-scoring-engine*
*Context gathered: 2026-03-24*
