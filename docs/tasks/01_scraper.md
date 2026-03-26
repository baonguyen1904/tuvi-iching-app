# Task 01: Scraper Pipeline
## cohoc.net → Structured Lá Số Data

**Priority:** Must — blocks everything else
**Estimated effort:** 2-3 days
**Dependencies:** None
**Output:** Python module `services/scraper.py`

---

## What to Build

A Playwright-based async scraper that:
1. Takes birth data (date, hour, gender) as input
2. Submits to tuvi.cohoc.net/lap-la-so-tu-vi.html
3. Parses the returned HTML
4. Extracts structured lá số data (12 cung × sao)
5. Returns a typed Python dataclass

---

## Input

```python
@dataclass
class BirthInput:
    birth_date: date        # dương lịch, e.g., 1968-04-20
    birth_hour: str         # enum: ty, suu, dan, mao, thin, ty_, ngo, mui, than, dau, tuat, hoi
    gender: str             # "male" or "female"
    name: str | None = None # optional, not used for scraping
```

## Output

```python
@dataclass
class Star:
    name: str               # e.g., "Thiên Đồng"
    type: str               # "chinh_tinh" or "phu_tinh"

@dataclass
class Cung:
    name: str               # e.g., "Mệnh", "Phụ Mẫu", "Phúc Đức", ...
    position: int           # 1-12 (vị trí trên lá số)
    stars: list[Star]

@dataclass
class LasoData:
    cung_menh: str          # tên cung mệnh
    ngu_hanh: str           # ngũ hành (Kim/Mộc/Thủy/Hỏa/Thổ)
    lunar_year: str         # năm âm lịch (e.g., "Mậu Thân")
    lunar_info: str         # full âm lịch string
    cungs: list[Cung]       # 12 cung with stars
    raw_html: str | None    # optional: store raw HTML for debugging
```

---

## Implementation Notes

### Playwright Setup
```python
from playwright.async_api import async_playwright

async def scrape_laso(input: BirthInput) -> LasoData:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        # ... navigate, fill, submit, parse
```

### Form Fields on cohoc.net
- Inspect the form at `tuvi.cohoc.net/lap-la-so-tu-vi.html`
- Map `birth_hour` enum to the website's dropdown values
- Map `gender` to the website's radio/select values
- Handle dương lịch → the site may do its own conversion

### HTML Parsing
- After form submission, wait for result page to render
- 12 cung are displayed in a grid/table structure
- Each cung contains sao names (likely in a specific CSS class or HTML structure)
- **IMPORTANT:** Parse carefully — the HTML structure may vary. Use robust selectors.

### Error Handling
- Timeout: set 30 second timeout for page load
- Network error: raise `ScraperError` with descriptive message
- Unexpected HTML: log raw HTML, raise `ParseError`
- Rate limiting: add 1-2 second delay between requests

---

## Acceptance Criteria

- [ ] `scrape_laso()` returns `LasoData` for valid input
- [ ] All 12 cung are parsed with correct star names
- [ ] Works for at least 5 different birth dates (see test fixtures)
- [ ] Handles timeout gracefully (raises `ScraperError` after 30s)
- [ ] Async-compatible (can be called from FastAPI endpoint)
- [ ] Raw HTML is stored for debugging when `debug=True`
- [ ] Logging: info-level log for each scrape attempt (no PII in logs, just "scraping for profile {hash}")

---

## Test Cases

Use these birth data as fixtures (compare output with manual cohoc.net check):

| # | Birth Date | Hour | Gender | Expected Cung Mệnh | Notes |
|---|-----------|------|--------|--------------------|----|
| 1 | 1968-04-20 | dau | female | TBD (verify manually) | Primary test case |
| 2 | 1990-01-15 | ngo | male | TBD | Different generation |
| 3 | 2000-12-31 | ty | female | TBD | Edge: year-end |
| 4 | 1985-06-10 | mao | male | TBD | Mid-range |
| 5 | 1975-09-22 | hoi | female | TBD | Different hour |

**Before implementation:** Manually go to cohoc.net with these inputs, screenshot results, and fill in "Expected Cung Mệnh" + save the full lá số as reference.

---

## Edge Cases

- What if cohoc.net is down? → Raise `ScraperError("Service unavailable")`
- What if HTML structure changes? → ParseError with raw HTML for debugging
- What if the site returns a captcha? → Log + raise error (handle manually for now)
- Birth dates at year boundaries (Dec 31 → lunar calendar may be different year)