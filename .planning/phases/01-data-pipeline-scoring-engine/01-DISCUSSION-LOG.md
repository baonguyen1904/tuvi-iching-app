# Phase 1: Data Pipeline & Scoring Engine - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-03-24
**Phase:** 01-data-pipeline-scoring-engine
**Areas discussed:** Scraper approach, Data merging, Scoring logic, Caching strategy

---

## Scraper Approach

| Option | Description | Selected |
|--------|-------------|----------|
| Keep Selenium | Port existing code as-is — proven to work, faster to ship | ✓ |
| HTTP + BeautifulSoup | Try direct HTTP POST first — lighter, no browser needed | |
| You decide | Claude picks best approach | |

**User's choice:** Keep Selenium
**Notes:** None

### Follow-up: Deployment

| Option | Description | Selected |
|--------|-------------|----------|
| Docker + headless | Docker container with Chrome headless — standard for Railway | ✓ |
| Separate service | Scraper as separate microservice on VM | |
| You decide | Claude picks | |

**User's choice:** Docker + headless

---

## Data Merging

| Option | Description | Selected |
|--------|-------------|----------|
| Keep separate | Two scraper calls, two data sets, combined into CungInfo — matches legacy | ✓ |
| Unified structure | Merge into single normalized schema | |
| You decide | Claude picks | |

**User's choice:** Keep separate

### Follow-up: Scrape Order

| Option | Description | Selected |
|--------|-------------|----------|
| Sequential | cohoc first, then tuvi.vn — simpler, one Chrome instance | ✓ |
| Parallel | Two Chrome instances simultaneously | |
| You decide | Claude picks | |

**User's choice:** Sequential

---

## Scoring Logic

| Option | Description | Selected |
|--------|-------------|----------|
| JSON lookup | Export xlsx → JSON once, load at startup | ✓ |
| Read xlsx runtime | Use openpyxl/pandas to read xlsx at startup | |
| Hardcode in Python | Convert to Python dicts/constants | |
| You decide | Claude picks | |

**User's choice:** JSON lookup

### Follow-up: Validation

| Option | Description | Selected |
|--------|-------------|----------|
| Manual test cases | Pick 5-10 birth dates, compare manually | |
| Automated tests | Export Sheet results for 20+ cases, write pytest | ✓ |
| You decide | Claude picks | |

**User's choice:** Automated tests

---

## Caching Strategy

| Option | Description | Selected |
|--------|-------------|----------|
| SQLite | Simple file-based DB | |
| JSON files | Keep legacy approach | |
| Supabase/Postgres | Cloud DB — more setup but scales better | ✓ |
| You decide | Claude picks | |

**User's choice:** Supabase/Postgres

### Follow-up: Cache Key

| Option | Description | Selected |
|--------|-------------|----------|
| birth+gender | Static key for all data | |
| birth+gender+year | Include năm xem for monthly data | |
| You decide | Claude determines | |

**User's choice:** Split by source — cohoc: birth+gender (static), tuvi.vn: birth+gender+year (yearly monthly data)

---

## Claude's Discretion

None — user made all decisions explicitly.

## Deferred Ideas

None — discussion stayed within phase scope.
