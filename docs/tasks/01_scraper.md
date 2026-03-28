# Task 01: Scraper Pipeline
## TWO Scrapers → Structured Lá Số Data

**Priority:** Must — blocks everything else
**Estimated effort:** 3-4 days
**Dependencies:** None
**Output:** `services/scraper_cohoc.py` + `services/scraper_tuvivn.py`
**Spec file** `docs/superpowers/specs/2026-03-26-scraper-design.md`
**Plan file** `docs/superpowers/plans/2026-03-26-scraper-implementation.md`
**Claude code session** = `0a133f23-e1c2-40fe-942c-04a7795a5441`

---

## CRITICAL FINDING: Two Data Sources

The existing codebase uses **TWO different websites** for different time scales:

| Source | URL | Provides | Used for |
|--------|-----|----------|----------|
| tuvi.cohoc.net | `/lay-la-so-tu-vi-ngay-duong-lich.html` | `cung` (lifetime) + `cung_10yrs` (Đại Vận) | Lifetime chart + 10-year chart |
| tuvi.vn | (form submit with `nam_xem`) | `cung_12months` (sorted by month) | Monthly chart |

**Both must be scraped** for a complete profile. They share the same birth data input but return different chart perspectives.

---

## Scraper A: tuvi.cohoc.net (Lifetime + 10-Year)

### What it does
1. POST birth data to cohoc.net form
2. Parse result HTML → extract 12 cung (lifetime) + 12 cung_10yrs (Đại Vận)
3. Return structured data

### Input
```python
@dataclass
class BirthInput:
    birth_date: date         # dương lịch
    birth_hour: str          # ty, suu, dan, mao, thin, ty_, ngo, mui, than, dau, tuat, hoi
    gender: str              # "male" or "female"
    name: str | None = None
```

### Output
```python
@dataclass
class Star:
    name: str                # e.g., "Phá Quân" (base name, cleaned)
    raw_name: str            # e.g., "Phá Quân\n(Đ)" (original from HTML)
    variant: str | None      # "Đ", "H", "M", or None
    slug: str                # slugify(raw_name.lower()) for matching

@dataclass
class Cung:
    name: str                # e.g., "Mệnh" (cleaned, "Thân" suffix stripped)
    stars: list[Star]

@dataclass
class CohocData:
    # Metadata
    nam: str                 # Năm âm lịch, e.g., "Giáp Tuất"
    menh: str                # Mệnh ngũ hành, e.g., "Mộc"
    cuc: str                 # Cục, e.g., "Thủy Nhị Cục"
    than_cu: str             # Cung Thân cư, e.g., "Thiên Di"
    menh_chu: str            # Mệnh chủ sao
    than_chu: str            # Thân chủ sao
    am_duong: str            # "Dương Nam", "Âm Nữ", etc.
    
    # Chart data
    cung: list[Cung]         # 12 cung — lifetime chart
    cung_10yrs: list[Cung]   # 12 cung — Đại Vận (10-year periods), ordered by time
```

### Star Name Parsing (CRITICAL)

Stars from cohoc.net come with embedded newlines for variant suffixes:

```
Raw HTML text        → raw_name          → name        → variant → slug
"Phá Quân\n(Đ)"     → "Phá Quân\n(Đ)"  → "Phá Quân"  → "Đ"     → "pha-quan-d"
"Tử Vi"             → "Tử Vi"           → "Tử Vi"     → None    → "tu-vi"
"L.Hồng Loan"       → "L.Hồng Loan"    → "L.Hồng Loan" → None  → "l-hong-loan"
"ĐV. T Khôi"        → "ĐV. T Khôi"     → "ĐV. T Khôi" → None   → "dv-t-khoi"
```

**Parsing logic:**
```python
import re
from slugify import slugify

def parse_star(raw_text: str) -> Star:
    raw_name = raw_text.strip()
    
    # Extract variant suffix: (Đ), (H), (M)
    variant_match = re.search(r'\(([ĐHM])\)', raw_name)
    variant = variant_match.group(1) if variant_match else None
    
    # Clean name (remove newlines, keep variant in slug)
    name = re.sub(r'\n.*', '', raw_name).strip()  # base name without variant
    
    # Slug for matching against laso_points
    slug = slugify(raw_name.lower())  # includes variant: "pha-quan-d"
    
    return Star(name=name, raw_name=raw_name, variant=variant, slug=slug)
```

### Đại Vận Ordering Logic

The 10-year chart cungs are ordered based on `am_duong` and current year:

```python
LUNA_YEARS = {
    2022: "Dần", 2023: "Mão", 2024: "Thìn", 2025: "Tị", 2026: "Ngọ",
    2027: "Mùi", 2028: "Thân", 2029: "Dậu", 2030: "Tuất", 2031: "Hợi",
    2032: "Tí",  2033: "Sửu",  # ... extends in 12-year cycle
}

# Ordering arrays (from existing code):
MAIN_ORDER = [0, 1, 2, 3, 5, 7, 11, 10, 9, 8, 6, 4]      # Dương Nam / Âm Nữ
REVERSED_ORDER = [0, 4, 6, 8, 9, 10, 11, 7, 5, 3, 2, 1]   # Âm Nam / Dương Nữ
```

The website handles this ordering. Scraper just extracts `cung_10yrs` in the order presented.

### HTML Parsing Details

```python
# Cung extraction selectors (from existing code):
chinh_tinh = cung_td.select_one("div.cung-top > div.chinh-tinh > p:nth-child(1) > span").text
sao_tot = cung_td.select("div.cung-middle > ul.sao-tot > li")
sao_xau = cung_td.select("div.cung-middle > ul.sao-xau > li")
sao_bottom = cung_td.select_one("div.cung-bottom > p > span").text

# Cung name: strip "Thân" suffix
ten_cung = re.sub(r"\s+Thân$", "", raw_text, flags=re.IGNORECASE).strip()

# Metadata extraction uses Unicode NFC normalization
```

### Edge Cases from Existing Code

1. **IP rate-limit:** URL contains `ip-deny` → raise error, retry later
2. **Cache not found:** URL contains `cache-not-found` → wait up to 90s for server to generate
3. **Unicode:** Apply NFC normalization for metadata fields
4. **"Thân" suffix:** Some cung names have " Thân" appended → strip it

---

## Scraper B: tuvi.vn (Monthly)

### What it does
1. Submit birth data + `nam_xem` (year to analyze) to tuvi.vn
2. Parse result → extract 12 cung with month labels
3. Return sorted by month

### Output
```python
@dataclass
class MonthlyCung:
    name: str                # Cung name
    month: int               # 1-12
    month_label: str         # "Th.1", "Th.2", etc.
    stars: list[Star]

@dataclass
class TuViVnData:
    cung_12months: list[MonthlyCung]  # 12 entries, sorted by month
```

### Star Filtering
tuvi.vn uses CSS class `d-none` to hide irrelevant stars:
```python
# MUST filter out hidden stars:
if "d-none" not in div.get("class", []):
    sao.append(text)
```

---

## Combined Output

```python
@dataclass
class LasoData:
    """Complete chart data from both sources."""
    # Metadata (from cohoc)
    nam: str
    menh: str
    cuc: str
    than_cu: str
    menh_chu: str
    than_chu: str
    am_duong: str
    
    # Chart data
    cung: list[Cung]              # Lifetime (12 cungs) — from cohoc
    cung_10yrs: list[Cung]        # Đại Vận (12 cungs, ordered) — from cohoc
    cung_12months: list[MonthlyCung]  # Monthly (12, sorted) — from tuvi.vn
```

---

## Implementation: Playwright Migration

Existing code uses `undetected-chromedriver` (Selenium). Port to **Playwright** (async):

```python
from playwright.async_api import async_playwright

class CohocScraper:
    async def scrape(self, input: BirthInput) -> CohocData:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            await page.goto(COHOC_URL)
            # Fill form fields...
            await page.click('input[type="submit"]')
            
            # Wait for result (handle cache-not-found retry)
            await page.wait_for_selector('div.cung-top', timeout=90000)
            
            html = await page.content()
            return self._parse(html, input)
    
    def _parse(self, html: str, input: BirthInput) -> CohocData:
        # BeautifulSoup parsing (same selectors as existing code)
        ...

class TuViVnScraper:
    async def scrape(self, input: BirthInput, nam_xem: int) -> TuViVnData:
        # Similar pattern, different URL and form
        ...
```

---

## Acceptance Criteria

- [ ] **Cohoc scraper:** Returns `CohocData` with 12 cung + 12 cung_10yrs for valid input
- [ ] **TuViVn scraper:** Returns `TuViVnData` with 12 monthly cungs sorted by month
- [ ] **Star names:** Correctly parse variant suffixes (Đ/H/M) from newline-embedded format
- [ ] **Star slugs:** `slugify(raw_name.lower())` produces correct slugs matching laso_points
- [ ] **L. prefix stars** and **ĐV. prefix stars** are captured
- [ ] **d-none filter:** Hidden stars on tuvi.vn are excluded
- [ ] **Cung name cleaning:** "Thân" suffix stripped
- [ ] **Unicode:** NFC normalization applied
- [ ] **Error handling:** Timeout (90s), IP rate-limit, cache-not-found retry
- [ ] **Async:** Both scrapers work with asyncio (FastAPI compatible)
- [ ] **Test:** 5 birth data inputs produce consistent, verifiable output
- [ ] **Logging:** Info-level per scrape (no PII), warning for parse issues

---

## Test Cases

| # | Birth Date | Hour | Gender | Verify |
|---|-----------|------|--------|--------|
| 1 | 1994-07-19 | dan (06h) | male | Matches existing report output (payload from code) |
| 2 | 1968-04-20 | dau | female | Different generation |
| 3 | 1990-01-15 | ngo | male | Edge: early January |
| 4 | 2000-12-31 | ty | female | Edge: year-end |
| 5 | 1985-06-10 | mao | male | Mid-range |

For test case 1, we have the existing payload format to compare against:
```python
# Expected payload from existing code:
{"full_name": "Test", "ngay_sinh": "19/07/1994", "gio_sinh": "06h00", "gender": "Nam"}
```