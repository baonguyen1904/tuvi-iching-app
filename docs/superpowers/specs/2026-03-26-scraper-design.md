# Scraper Module Design — Direct Port to Playwright

**Date:** 2026-03-26
**Status:** Approved
**Scope:** Task 01 — Data Pipeline (scraper only, no scoring)

---

## Overview

Port the existing Selenium-based scrapers from `/mnt/d/Working/TBTesu/tuvi/scraper` to Playwright async, living inside TuViApp at `backend/app/services/`. Two scrapers: cohoc.net (lifetime + 10yr) and tuvi.vn (monthly). Schema matches existing scraper output exactly — no new extraction logic.

---

## Module Structure

```
backend/
├── app/
│   ├── services/
│   │   ├── scraper_browser.py    # Browser lifecycle manager
│   │   ├── scraper_cohoc.py      # cohoc.net scraper (lifetime + 10yr)
│   │   ├── scraper_tuvivn.py     # tuvi.vn scraper (monthly)
│   │   └── soup_utils.py         # HTML parsing helpers (ported from existing)
│   ├── models/
│   │   └── schemas.py            # Pydantic v2 models (ported from existing)
│   └── constants.py              # GIO_SINH, LUNA_YEARS, URLs, cung order arrays
├── requirements.txt
└── tests/
    ├── test_scraper_cohoc.py
    ├── test_scraper_tuvivn.py
    └── fixtures/                  # Saved HTML snapshots for offline tests
```

### Dependencies

- `playwright` (async API)
- `beautifulsoup4` + `lxml` (HTML parsing)
- `python-slugify` (star matching — CLAUDE.md rule #7)
- `pydantic` v2 (schemas)
- `unicodedata` (NFC normalization — stdlib)

---

## Browser Lifecycle (`scraper_browser.py`)

Single Chromium process, fresh browser context per request.

```python
class BrowserManager:
    _browser: Browser | None

    async def start():
        # Called at FastAPI startup (lifespan event)
        # Launch single Chromium process
        playwright = await async_playwright().start()
        _browser = await playwright.chromium.launch(headless=True)

    async def new_context() -> BrowserContext:
        # Per-request: isolated cookies/storage
        return await _browser.new_context(
            locale="vi-VN",
            user_agent="...",  # Mimic real browser UA
        )

    async def shutdown():
        # Called at FastAPI shutdown
        await _browser.close()
```

- Integrated via FastAPI `@asynccontextmanager` lifespan
- Each scrape call: get context → open page → work → close context
- No `playwright-stealth` initially — add only if sites block

---

## Schemas (`models/schemas.py`)

Direct port of existing `schemas/__init__.py`, Pydantic v1 → v2:

```python
class CungDetail(BaseModel):
    ten: str                        # Cung name ("Than" suffix stripped)
    sao: list[str]                  # Star names as-is from scraper
    thang: str | None = None        # Month label (e.g., "Th.1"), monthly only

class CungInfo(BaseModel):
    cung_chung: list[CungDetail]    # 12 lifetime cungs
    cung_10yrs: list[CungDetail]    # 10-year Dai Van (can be empty list)
    cung_12months: list[CungDetail] # Monthly, sorted by month

class LaSoTuVi(BaseModel):
    ngay_sinh: str                  # "YYYY-MM-DD"
    gio_sinh: str                   # "HHhMM" or "HH:MM"
    gender: str                     # "Nam" / "Nu"
    nam_am_lich: str | None = None
    menh: str | None = None
    cuc: str | None = None
    than_cu: str | None = None
    menh_chu: str | None = None
    than_chu: str | None = None
    am_duong: str | None = None     # "Duong Nam", "Am Nu", etc.
    cung: CungInfo | None = None

class LaSoTuViInput(BaseModel):
    ngay_sinh: str                  # "DD/MM/YYYY"
    gio_sinh: str                   # "HHhMM"
    gender: str
    full_name: str | None = None
    nam_xem: int | None = None
    noi_sinh: str | None = None
```

**Key decision:** `sao` is `list[str]` — slug generation and variant extraction happen in the scoring engine, not the scraper. Matches existing code boundary.

---

## Scraper A: cohoc.net (`scraper_cohoc.py`)

Direct port of `tuvi_cohoc_scraper.py`.

### Flow

1. **Navigate** to form URL
2. **Fill form** — XPath selectors for dropdowns:
   - `//select[@name='ddlNgay']/option[text()='{day}']`
   - `//select[@name='ddlThang']/option[text()='{month}']`
   - `//select[@name='ddlNam']/option[text()='{year}']`
   - Time via `GIO_SINH` dict mapping
   - Gender radio button
3. **Submit** — `page.evaluate("document.getElementById('btGiaiDoan').click()")`
4. **Wait for result** — detect URL changes:
   - `ip-deny` in URL → raise `RuntimeError("IP denied by tuvi.cohoc.net")`
   - `cache-not-found` in URL → wait up to 90s for `div.thien-ban`
   - Otherwise → wait 10s for result page load
5. **Parse HTML** — `page.content()` → BeautifulSoup:
   - Metadata: `find_metadata_field(soup, "Nam:")`, `"Menh:"`, `"Cuc:"`, `"Am Duong:"`
   - 12 cungs: `td.cung` elements
   - Stars per cung: `div.chinh-tinh span`, `ul.sao-tot li`, `ul.sao-xau li`, `div.cung-bottom span`
   - Find Menh cung, reorder based on `am_duong` using existing index arrays
   - 10-year: same logic with `span.cung-tieuvan` year labels
6. **Return** `LaSoTuVi` with `cung_chung` + `cung_10yrs`

### Cung Reorder Logic (preserved from existing)

```python
# Duong Nam / Am Nu
main_order = [0, 1, 2, 3, 5, 7, 11, 10, 9, 8, 6, 4]
# Am Nam / Duong Nu
reversed_order = [0, 4, 6, 8, 9, 10, 11, 7, 5, 3, 2, 1]
```

---

## Scraper B: tuvi.vn (`scraper_tuvivn.py`)

Direct port of `tuvi_vn_scraper.py`.

### Flow

1. **Navigate** to form URL, wait 3s (existing behavior)
2. **Fill form** — scroll into view, text inputs (`.fill()`), dropdowns (XPath text match), gender radio (index-based), optional `nam_xem`
3. **Submit** and wait for `td.cung` elements
4. **Parse HTML**:
   - Cungs: `p.text-sao-chinh-tinh`
   - Main stars: `div.chinh-tinh p.text-chinh-chinh`
   - Good stars: `div.sao-tot > div[data-sao-id]` — **filter out `.d-none`**
   - Bad stars: `div.sao-xau > div[data-sao-id]` — **filter out `.d-none`**
   - Bottom: `div.cung-bottom > span.txt-tiny-mid`
   - Month: `div.view-cung-dai-van > p` (second `<p>`)
5. **Find Menh cung, reorder, sort by month**
6. **Return** `LaSoTuVi` with `cung_12months`

### Unicode handling (preserved)

`to_string()` normalizes to NFC, strips/collapses whitespace, removes dashes and plus signs.

---

## Shared Utilities

### `soup_utils.py` (copy from existing)

- `find_metadata_field(soup, label)` — dual strategy: cohoc style (span in p) + tuvi.vn style (sibling td)
- `to_string(element)` — NFC normalization, whitespace cleanup

### `constants.py` (port from existing)

- `GIO_SINH`: hour → time range mapping for cohoc.net form
- `LUNA_YEARS`: lunar year name cycle (12 years)
- `COHOC_FORM_URL`, `TUVIVN_FORM_URL`: target URLs
- `MAIN_ORDER`, `REVERSED_ORDER`: cung reorder index arrays

---

## Error Handling

Same behavior as existing code — scraper raises, API router decides response.

| Condition | Detection | Action |
|-----------|-----------|--------|
| IP rate-limit | `ip-deny` in URL | `RuntimeError("IP denied by tuvi.cohoc.net")` |
| Cache generating | `cache-not-found` in URL | Wait 90s for `div.thien-ban`, `RuntimeError` on timeout |
| Form load fail | Element not found in 15s | `RuntimeError("Form page did not load")` |
| Form submit fail | URL unchanged after 15s | `RuntimeError("Form did not navigate")` |
| Menh not found | tuvi.vn parsing | `ValueError` listing available cungs |
| Network timeout | Playwright timeout | Propagate `TimeoutError` |

No auto-retry in scraper layer.

---

## Testing Strategy

### 1. HTML Snapshot Tests (offline, fast)

- Save real HTML responses as fixtures in `tests/fixtures/`
- Test parsing logic without hitting live sites
- Verify: cung count = 12, star extraction correct, metadata populated, reordering works

### 2. Live Integration Tests (manual, slow)

- Marked with `@pytest.mark.live` — skipped in CI
- Hit real sites with known birth data
- Verify determinism: same input → same output twice

### 3. Fixtures to capture

- `fixtures/cohoc_result.html` — cohoc.net result page
- `fixtures/tuvivn_result.html` — tuvi.vn result page
- `fixtures/cohoc_expected.json` — expected parsed LaSoTuVi
- `fixtures/tuvivn_expected.json` — expected parsed LaSoTuVi

---

## What Changes vs. Existing Code

| Aspect | Existing | New |
|--------|----------|-----|
| Browser driver | Selenium + undetected-chromedriver | Playwright async |
| Element access | `driver.find_element()` | `page.locator()` / `page.evaluate()` |
| Waits | `WebDriverWait` + `EC.*` | `page.wait_for_selector()` / `page.wait_for_url()` |
| Form interaction | `element.click()`, `element.send_keys()` | `locator.click()`, `locator.fill()` |
| Browser lifecycle | Global driver at startup | BrowserManager: single process, context-per-request |
| Pydantic | v1 | v2 |
| Async | Sync (threaded) | Native async |

## What Stays Unchanged

- All CSS/XPath selectors
- BeautifulSoup parsing logic
- `soup_utils.py` functions
- Cung reorder index arrays
- `GIO_SINH` and `LUNA_YEARS` constants
- Schema shape (nullable metadata, `list[str]` for stars)
- Error types and messages
