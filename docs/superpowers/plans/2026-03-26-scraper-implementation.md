# Scraper Module Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Port the existing Selenium-based tuvi scrapers to Playwright async, integrated into the TuViApp FastAPI backend.

**Architecture:** Two scrapers (cohoc.net for lifetime+10yr, tuvi.vn for monthly) share a single Chromium process via BrowserManager. Each request gets an isolated browser context. HTML parsing uses BeautifulSoup (same selectors as existing code). All code lives at `backend/app/services/`.

**Tech Stack:** Python 3.11+, Playwright (async), BeautifulSoup4, lxml, python-slugify, Pydantic v2, pytest

---

## File Structure

| File | Responsibility |
|------|---------------|
| `backend/app/__init__.py` | Package marker |
| `backend/app/models/__init__.py` | Package marker |
| `backend/app/models/schemas.py` | Pydantic v2 data models (LaSoTuVi, CungDetail, etc.) |
| `backend/app/services/__init__.py` | Package marker |
| `backend/app/services/constants.py` | GIO_SINH map, LUNA_YEARS, URLs, cung reorder arrays |
| `backend/app/services/soup_utils.py` | HTML parsing helpers (find_metadata_field, to_string) |
| `backend/app/services/scraper_browser.py` | BrowserManager: startup, context-per-request, shutdown |
| `backend/app/services/scraper_cohoc.py` | cohoc.net scraper (lifetime + 10yr charts) |
| `backend/app/services/scraper_tuvivn.py` | tuvi.vn scraper (monthly charts) |
| `backend/requirements.txt` | Python dependencies |
| `backend/tests/__init__.py` | Package marker |
| `backend/tests/conftest.py` | Shared pytest fixtures |
| `backend/tests/test_schemas.py` | Schema validation tests |
| `backend/tests/test_soup_utils.py` | Parsing helper tests |
| `backend/tests/test_scraper_cohoc.py` | cohoc.net parsing + live tests |
| `backend/tests/test_scraper_tuvivn.py` | tuvi.vn parsing + live tests |
| `backend/tests/fixtures/` | HTML snapshots + expected JSON |

---

### Task 1: Project Scaffolding + Dependencies

**Files:**
- Create: `backend/requirements.txt`
- Create: `backend/app/__init__.py`
- Create: `backend/app/models/__init__.py`
- Create: `backend/app/services/__init__.py`
- Create: `backend/tests/__init__.py`
- Create: `backend/tests/conftest.py`

- [ ] **Step 1: Create directory structure and package markers**

```bash
mkdir -p backend/app/models backend/app/services backend/tests/fixtures
```

Create `backend/app/__init__.py`:
```python
```

Create `backend/app/models/__init__.py`:
```python
```

Create `backend/app/services/__init__.py`:
```python
```

Create `backend/tests/__init__.py`:
```python
```

- [ ] **Step 2: Create requirements.txt**

Create `backend/requirements.txt`:
```
playwright>=1.40.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
python-slugify>=8.0.0
pydantic>=2.0.0
pytest>=7.0.0
pytest-asyncio>=0.23.0
```

- [ ] **Step 3: Install dependencies and Playwright browser**

```bash
cd backend && pip install -r requirements.txt && playwright install chromium
```

Expected: All packages install successfully, Chromium binary downloaded.

- [ ] **Step 4: Create conftest.py with shared fixtures**

Create `backend/tests/conftest.py`:
```python
import json
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def fixtures_dir():
    return FIXTURES_DIR


@pytest.fixture
def cohoc_html(fixtures_dir):
    path = fixtures_dir / "cohoc_result.html"
    if not path.exists():
        pytest.skip("cohoc_result.html fixture not found")
    return path.read_text(encoding="utf-8")


@pytest.fixture
def tuvivn_html(fixtures_dir):
    path = fixtures_dir / "tuvivn_result.html"
    if not path.exists():
        pytest.skip("tuvivn_result.html fixture not found")
    return path.read_text(encoding="utf-8")


@pytest.fixture
def cohoc_expected(fixtures_dir):
    path = fixtures_dir / "cohoc_expected.json"
    if not path.exists():
        pytest.skip("cohoc_expected.json fixture not found")
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture
def tuvivn_expected(fixtures_dir):
    path = fixtures_dir / "tuvivn_expected.json"
    if not path.exists():
        pytest.skip("tuvivn_expected.json fixture not found")
    return json.loads(path.read_text(encoding="utf-8"))
```

- [ ] **Step 5: Verify pytest discovers empty test suite**

```bash
cd backend && python -m pytest tests/ -v --co
```

Expected: "no tests ran" (0 items collected), no import errors.

- [ ] **Step 6: Commit**

```bash
git add backend/
git commit -m "chore: scaffold backend project structure and dependencies"
```

---

### Task 2: Pydantic v2 Schemas

**Files:**
- Create: `backend/app/models/schemas.py`
- Create: `backend/tests/test_schemas.py`

- [ ] **Step 1: Write failing test for schemas**

Create `backend/tests/test_schemas.py`:
```python
from app.models.schemas import CungDetail, CungInfo, LaSoTuVi, LaSoTuViInput


def test_cung_detail_basic():
    cung = CungDetail(ten="Mệnh", sao=["Tử Vi (B)", "Lộc Tồn"])
    assert cung.ten == "Mệnh"
    assert len(cung.sao) == 2
    assert cung.thang is None


def test_cung_detail_with_month():
    cung = CungDetail(ten="Tài Bạch", sao=["Liêm Trinh (Đ)"], thang="Th.2")
    assert cung.thang == "Th.2"


def test_cung_info():
    cung = CungDetail(ten="Mệnh", sao=["Tử Vi (B)"])
    info = CungInfo(
        cung_chung=[cung],
        cung_10yrs=[],
        cung_12months=[],
    )
    assert len(info.cung_chung) == 1
    assert info.cung_10yrs == []


def test_la_so_tu_vi_minimal():
    la_so = LaSoTuVi(
        ngay_sinh="1997-10-11",
        gio_sinh="12h00",
        gender="Nam",
    )
    assert la_so.menh is None
    assert la_so.cung is None
    assert la_so.am_duong is None


def test_la_so_tu_vi_full():
    cung = CungDetail(ten="Mệnh", sao=["Vũ Khúc (H)"])
    info = CungInfo(cung_chung=[cung], cung_10yrs=[], cung_12months=[])
    la_so = LaSoTuVi(
        ngay_sinh="1997-10-11",
        gio_sinh="12h00",
        gender="Nam",
        am_duong="Âm Nam",
        menh="Giáng Hạ Thủy",
        cuc="Kim Tứ Cục",
        than_cu="Phu thê",
        menh_chu="Cự môn",
        than_chu="Thiên tướng",
        cung=info,
    )
    assert la_so.am_duong == "Âm Nam"
    assert la_so.cung.cung_chung[0].ten == "Mệnh"


def test_la_so_tu_vi_input():
    inp = LaSoTuViInput(
        ngay_sinh="11/10/1997",
        gio_sinh="12h00",
        gender="Nam",
        nam_xem=2026,
    )
    assert inp.nam_xem == 2026
    assert inp.full_name is None


def test_la_so_tu_vi_json_roundtrip():
    cung = CungDetail(ten="Mệnh", sao=["Tử Vi (B)", "Lộc Tồn"])
    info = CungInfo(cung_chung=[cung], cung_10yrs=[], cung_12months=[])
    la_so = LaSoTuVi(
        ngay_sinh="1997-10-11",
        gio_sinh="12h00",
        gender="Nam",
        am_duong="Âm Nam",
        cung=info,
    )
    data = la_so.model_dump()
    restored = LaSoTuVi(**data)
    assert restored.cung.cung_chung[0].sao == ["Tử Vi (B)", "Lộc Tồn"]
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd backend && python -m pytest tests/test_schemas.py -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'app.models.schemas'`

- [ ] **Step 3: Write schemas implementation**

Create `backend/app/models/schemas.py`:
```python
from typing import Optional

from pydantic import BaseModel


class CungDetail(BaseModel):
    ten: str
    sao: list[str]
    thang: Optional[str] = None


class CungInfo(BaseModel):
    cung_chung: list[CungDetail]
    cung_10yrs: list[CungDetail]
    cung_12months: list[CungDetail]


class LaSoTuVi(BaseModel):
    ngay_sinh: str
    gio_sinh: str
    gender: str
    nam_am_lich: Optional[str] = None
    menh: Optional[str] = None
    cuc: Optional[str] = None
    than_cu: Optional[str] = None
    menh_chu: Optional[str] = None
    than_chu: Optional[str] = None
    am_duong: Optional[str] = None
    cung: Optional[CungInfo] = None


class LaSoTuViInput(BaseModel):
    ngay_sinh: str
    gio_sinh: str
    gender: str
    full_name: Optional[str] = None
    nam_xem: Optional[int] = None
    noi_sinh: Optional[str] = None
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd backend && python -m pytest tests/test_schemas.py -v
```

Expected: All 7 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add backend/app/models/schemas.py backend/tests/test_schemas.py
git commit -m "feat: add Pydantic v2 schemas for scraper data models"
```

---

### Task 3: Constants

**Files:**
- Create: `backend/app/services/constants.py`

- [ ] **Step 1: Write constants module**

Create `backend/app/services/constants.py`:
```python
COHOC_FORM_URL = "http://tuvi.cohoc.net/lay-la-so-tu-vi-ngay-duong-lich.html"
TUVIVN_FORM_URL = "https://tuvi.vn/lap-la-so-tu-vi"

# Hour → [start_hour, end_hour] mapping for cohoc.net form
GIO_SINH = {
    1: [23, 1],
    2: [1, 3],
    3: [3, 5],
    4: [5, 7],
    5: [7, 9],
    6: [9, 11],
    7: [11, 13],
    8: [13, 15],
    9: [15, 17],
    10: [17, 19],
    11: [19, 21],
    12: [21, 23],
}

# Lunar year names by Gregorian year
LUNA_YEARS = {
    2022: "Dần",
    2023: "Mão",
    2024: "Thìn",
    2025: "Tị",
    2026: "Ngọ",
    2027: "Mùi",
    2028: "Thân",
    2029: "Dậu",
    2030: "Tuất",
    2031: "Hợi",
    2032: "Tí",
    2033: "Sửu",
    2034: "Dần",
    2035: "Mão",
    2036: "Thìn",
    2037: "Tị",
    2038: "Ngọ",
    2039: "Mùi",
    2040: "Thân",
    2041: "Dậu",
    2042: "Tuất",
    2043: "Hợi",
}

# Cung reorder arrays (position indices in the HTML grid)
# Dương Nam / Âm Nữ
MAIN_ORDER = [0, 1, 2, 3, 5, 7, 11, 10, 9, 8, 6, 4]
# Âm Nam / Dương Nữ
REVERSED_ORDER = [0, 4, 6, 8, 9, 10, 11, 7, 5, 3, 2, 1]
```

- [ ] **Step 2: Verify import works**

```bash
cd backend && python -c "from app.services.constants import GIO_SINH, LUNA_YEARS, MAIN_ORDER; print('OK', len(GIO_SINH), len(LUNA_YEARS))"
```

Expected: `OK 12 22`

- [ ] **Step 3: Commit**

```bash
git add backend/app/services/constants.py
git commit -m "feat: add constants for scraper configuration"
```

---

### Task 4: Soup Utilities

**Files:**
- Create: `backend/app/services/soup_utils.py`
- Create: `backend/tests/test_soup_utils.py`

- [ ] **Step 1: Write failing tests for soup_utils**

Create `backend/tests/test_soup_utils.py`:
```python
from bs4 import BeautifulSoup

from app.services.soup_utils import find_metadata_field, to_string, try_get_text


class TestTryGetText:
    def test_found(self):
        html = '<div><span class="val">Hello</span></div>'
        soup = BeautifulSoup(html, "html.parser")
        assert try_get_text(soup, "span.val") == "Hello"

    def test_not_found(self):
        html = "<div></div>"
        soup = BeautifulSoup(html, "html.parser")
        assert try_get_text(soup, "span.val") == ""

    def test_custom_default(self):
        html = "<div></div>"
        soup = BeautifulSoup(html, "html.parser")
        assert try_get_text(soup, "span.val", "N/A") == "N/A"


class TestFindMetadataField:
    def test_cohoc_style_span_in_p(self):
        html = """
        <div class="thien-ban">
            <p>Năm: <span>Đinh Sửu</span></p>
            <p>Mệnh: <span>Giáng Hạ Thủy</span></p>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        assert find_metadata_field(soup, "Năm:") == "Đinh Sửu"
        assert find_metadata_field(soup, "Mệnh:") == "Giáng Hạ Thủy"

    def test_tuvivn_style_sibling_td(self):
        html = """
        <div class="thien-ban">
            <table><tr>
                <td>Âm dương</td>
                <td><span>Dương Nam</span></td>
            </tr></table>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        assert find_metadata_field(soup, "Âm dương:") == "Dương Nam"

    def test_not_found_returns_default(self):
        html = '<div class="thien-ban"><p>Other: <span>val</span></p></div>'
        soup = BeautifulSoup(html, "html.parser")
        assert find_metadata_field(soup, "Missing:") is None
        assert find_metadata_field(soup, "Missing:", default="X") == "X"

    def test_container_not_found(self):
        html = "<div><p>Năm: <span>Val</span></p></div>"
        soup = BeautifulSoup(html, "html.parser")
        assert find_metadata_field(soup, "Năm:") is None

    def test_custom_container(self):
        html = """
        <div class="view-thien-ban">
            <p>Năm: <span>Mậu Thân</span></p>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        result = find_metadata_field(soup, "Năm:", container_selector="div.view-thien-ban")
        assert result == "Mậu Thân"

    def test_unicode_nfc_normalization(self):
        # NFD: Mệnh as M + e + combining breve + combining dot below + n + h
        import unicodedata
        label_nfd = unicodedata.normalize("NFD", "Mệnh:")
        html = f'<div class="thien-ban"><p>{label_nfd} <span>Kim</span></p></div>'
        soup = BeautifulSoup(html, "html.parser")
        assert find_metadata_field(soup, "Mệnh:") == "Kim"


class TestToString:
    def test_basic(self):
        assert to_string("  Tử   Vi  ") == "Tử Vi"

    def test_removes_dashes_and_plus(self):
        assert to_string("Thiên - Đồng +") == "Thiên Đồng"

    def test_collapses_whitespace(self):
        assert to_string("Phá\n  Quân") == "Phá Quân"

    def test_nfc_normalization(self):
        import unicodedata
        nfd = unicodedata.normalize("NFD", "Mệnh")
        result = to_string(nfd)
        assert result == unicodedata.normalize("NFC", "Mệnh")

    def test_empty_string(self):
        assert to_string("") == ""
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd backend && python -m pytest tests/test_soup_utils.py -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'app.services.soup_utils'`

- [ ] **Step 3: Write soup_utils implementation**

Create `backend/app/services/soup_utils.py`:
```python
import logging
import unicodedata

logger = logging.getLogger(__name__)


def _normalize(text):
    """Normalize Unicode text to NFC form for consistent comparison.

    HTML pages may use NFD (decomposed) while Python strings use NFC (composed).
    """
    return unicodedata.normalize("NFC", text)


def try_get_text(soup, selector, default=""):
    el = soup.select_one(selector)
    if el is None:
        return default

    return el.text


def find_metadata_field(soup, label, container_selector="div.thien-ban", default=None):
    container = soup.select_one(container_selector)
    if not container:
        logger.warning("Container '%s' not found", container_selector)
        return default

    label_nfc = _normalize(label)
    label_search = _normalize(label.rstrip(":").strip())

    # Strategy 1: label + value in same <p> tag (tuvi.cohoc style)
    for p in container.find_all("p"):
        text = _normalize(p.get_text())
        if label_nfc in text:
            span = p.find("span")
            if span:
                return _normalize(span.get_text(strip=True))
            value = text.replace(label_nfc, "").strip()
            if value:
                return value

    # Strategy 2: label in <td>, value in sibling <td> (tuvi.vn style)
    for td in container.find_all("td"):
        td_text = _normalize(td.get_text(strip=True))
        if label_search in td_text:
            next_td = td.find_next_sibling("td")
            if next_td:
                span = next_td.find("span")
                if span:
                    return _normalize(span.get_text(strip=True))
                return _normalize(next_td.get_text(strip=True))

    logger.warning("Metadata field '%s' not found", label)
    return default


def to_string(text: str):
    text = unicodedata.normalize("NFC", text)
    chars = text.strip().split(" ")
    chars = [c.strip() for c in chars if c not in [" ", "\n", ""]]
    new_str = " ".join(chars)
    new_str = new_str.replace("-", "")
    new_str = new_str.replace("+", "")
    return new_str
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd backend && python -m pytest tests/test_soup_utils.py -v
```

Expected: All 11 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add backend/app/services/soup_utils.py backend/tests/test_soup_utils.py
git commit -m "feat: add HTML parsing utilities (soup_utils)"
```

---

### Task 5: BrowserManager

**Files:**
- Create: `backend/app/services/scraper_browser.py`

- [ ] **Step 1: Write BrowserManager implementation**

Create `backend/app/services/scraper_browser.py`:
```python
import logging

from playwright.async_api import Browser, BrowserContext, async_playwright

logger = logging.getLogger(__name__)

_playwright = None
_browser: Browser | None = None


async def start():
    """Launch Chromium. Call once at FastAPI startup."""
    global _playwright, _browser
    _playwright = await async_playwright().start()
    _browser = await _playwright.chromium.launch(headless=True)
    logger.info("BrowserManager: Chromium launched")


async def new_context() -> BrowserContext:
    """Create isolated browser context for a single scrape request."""
    if _browser is None:
        raise RuntimeError("BrowserManager not started. Call start() first.")
    return await _browser.new_context(
        locale="vi-VN",
        viewport={"width": 694, "height": 1080},
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
    )


async def shutdown():
    """Close browser and Playwright. Call at FastAPI shutdown."""
    global _browser, _playwright
    if _browser:
        await _browser.close()
        _browser = None
        logger.info("BrowserManager: browser closed")
    if _playwright:
        await _playwright.stop()
        _playwright = None
```

- [ ] **Step 2: Write a quick smoke test**

```bash
cd backend && python -c "
import asyncio
from app.services import scraper_browser

async def test():
    await scraper_browser.start()
    ctx = await scraper_browser.new_context()
    page = await ctx.new_page()
    await page.goto('https://example.com')
    title = await page.title()
    await ctx.close()
    await scraper_browser.shutdown()
    print(f'OK: {title}')

asyncio.run(test())
"
```

Expected: `OK: Example Domain`

- [ ] **Step 3: Commit**

```bash
git add backend/app/services/scraper_browser.py
git commit -m "feat: add BrowserManager for Playwright lifecycle"
```

---

### Task 6: cohoc.net Scraper

**Files:**
- Create: `backend/app/services/scraper_cohoc.py`
- Create: `backend/tests/test_scraper_cohoc.py`

- [ ] **Step 1: Copy a cohoc.net HTML fixture for offline testing**

Copy the existing HTML fixture from the old scraper project:

```bash
cp "/mnt/d/Working/TBTesu/tuvi/scraper/src/data/html/bao.html" backend/tests/fixtures/cohoc_result.html
```

Also create expected output from a known result:

```bash
cp "/mnt/d/Working/TBTesu/tuvi/scraper/src/data/result_1997-10-11_12_Nam.json" backend/tests/fixtures/cohoc_expected.json
```

- [ ] **Step 2: Write failing tests for cohoc.net parser**

Create `backend/tests/test_scraper_cohoc.py`:
```python
import json

import pytest

from app.services.scraper_cohoc import get_gio_sinh_option, parse_body


class TestGetGioSinhOption:
    def test_midnight(self):
        from datetime import datetime
        assert get_gio_sinh_option(datetime(2000, 1, 1, 0, 0)) == 1

    def test_hour_23(self):
        from datetime import datetime
        assert get_gio_sinh_option(datetime(2000, 1, 1, 23, 0)) == 1

    def test_hour_1(self):
        from datetime import datetime
        assert get_gio_sinh_option(datetime(2000, 1, 1, 1, 0)) == 1

    def test_hour_7(self):
        from datetime import datetime
        assert get_gio_sinh_option(datetime(2000, 1, 1, 7, 0)) == 5

    def test_hour_12(self):
        from datetime import datetime
        assert get_gio_sinh_option(datetime(2000, 1, 1, 12, 0)) == 7

    def test_hour_21(self):
        from datetime import datetime
        assert get_gio_sinh_option(datetime(2000, 1, 1, 21, 0)) == 12


class TestParseBody:
    def test_parse_produces_12_cungs(self, cohoc_html):
        data = parse_body(cohoc_html)
        assert len(data["cung"]) == 12

    def test_parse_first_cung_is_menh(self, cohoc_html):
        data = parse_body(cohoc_html)
        assert "MỆNH" in data["cung"][0]["ten"].upper() or "Mệnh" in data["cung"][0]["ten"]

    def test_parse_each_cung_has_stars(self, cohoc_html):
        data = parse_body(cohoc_html)
        for cung in data["cung"]:
            assert len(cung["sao"]) >= 1, f"Cung '{cung['ten']}' has no stars"

    def test_parse_metadata_present(self, cohoc_html):
        data = parse_body(cohoc_html)
        assert data.get("am_duong") is not None

    def test_parse_10yr_cungs(self, cohoc_html):
        data = parse_body(cohoc_html)
        assert len(data["cung_10yrs"]) == 12


@pytest.mark.live
class TestLiveCohoc:
    """Live integration tests — run with: pytest -m live"""

    @pytest.fixture
    def _browser(self):
        import asyncio
        from app.services import scraper_browser

        async def setup():
            await scraper_browser.start()

        asyncio.get_event_loop().run_until_complete(setup())
        yield
        asyncio.get_event_loop().run_until_complete(scraper_browser.shutdown())

    def test_determinism(self, _browser):
        """Same input twice produces identical output."""
        import asyncio
        from datetime import datetime
        from app.services.scraper_cohoc import get_page_detail

        async def run():
            dob = datetime(1997, 10, 11)
            result1 = await get_page_detail(dob, 12, "Nam")
            result2 = await get_page_detail(dob, 12, "Nam")
            return result1, result2

        r1, r2 = asyncio.get_event_loop().run_until_complete(run())
        assert r1["cung"] == r2["cung"]
```

- [ ] **Step 3: Run tests to verify they fail**

```bash
cd backend && python -m pytest tests/test_scraper_cohoc.py -v -m "not live"
```

Expected: FAIL with `ModuleNotFoundError: No module named 'app.services.scraper_cohoc'`

- [ ] **Step 4: Write cohoc.net scraper implementation**

Create `backend/app/services/scraper_cohoc.py`:
```python
import logging
import re
from datetime import datetime

from bs4 import BeautifulSoup

from app.services import constants, soup_utils
from app.services.scraper_browser import new_context

logger = logging.getLogger(__name__)

GIO_SINH = constants.GIO_SINH


def get_gio_sinh_option(time: datetime):
    for k, v in GIO_SINH.items():
        if time.hour in [23, 24, 0, 1]:
            return 1

        start, end = v
        if start <= time.hour < end:
            return k


def get_list_cungs(cung_tds):
    cungs = []
    for cung_td in cung_tds:
        txt = cung_td.select_one("p.cung-tencung").text.strip()
        txt = re.sub(r"\s+Thân$", "", txt, flags=re.IGNORECASE).strip()
        cungs.append(txt)
    return cungs


def parse_body(body):
    soup = BeautifulSoup(body, features="html.parser")

    data = {
        "nam": soup_utils.find_metadata_field(soup, "Năm:"),
        "menh": soup_utils.find_metadata_field(soup, "Mệnh:"),
        "cuc": soup_utils.find_metadata_field(soup, "Cục:"),
        "cung": [],
        "cung_10yrs": [],
    }

    data["than_cu"] = soup_utils.find_metadata_field(soup, "Thân cư:")
    data["menh_chu"] = soup_utils.find_metadata_field(soup, "Mệnh chủ:")
    data["than_chu"] = soup_utils.find_metadata_field(soup, "Thân chủ:")

    am_duong = soup_utils.find_metadata_field(soup, "Âm Dương:")
    data["am_duong"] = am_duong

    # 12 Cung
    main_order = constants.MAIN_ORDER
    reversed_order = constants.REVERSED_ORDER
    cung_tds = soup.select("td.cung")
    cungs = get_list_cungs(cung_tds)
    start = "MỆNH"
    start_idx = cungs.index(start)

    if am_duong in ["Dương Nam", "Âm Nữ"]:
        idx_in_main = main_order.index(start_idx)
        order = main_order[idx_in_main:] + main_order[:idx_in_main]
    else:
        idx_in_main = reversed_order.index(start_idx)
        order = reversed_order[idx_in_main:] + reversed_order[:idx_in_main]

    for i in order:
        cung_td = cung_tds[i]
        ten_cung = cung_td.select_one("p.cung-tencung").text
        sao = []
        chinh_tinh = cung_td.select_one(
            "div.cung-top > div.chinh-tinh > p:nth-child(1) > span"
        ).text
        sao.append(chinh_tinh)

        sao_tot_lis = cung_td.select("div.cung-middle > ul.sao-tot > li")
        for sao_tot_el in sao_tot_lis:
            sao.append(sao_tot_el.text)

        sao_xau_lis = cung_td.select("div.cung-middle > ul.sao-xau > li")
        for sao_xau_el in sao_xau_lis:
            sao.append(sao_xau_el.text)

        sao_bottom = cung_td.select_one("div.cung-bottom > p > span").text
        sao.append(sao_bottom)

        data["cung"].append({"ten": ten_cung, "sao": sao})

    # Vận 10 năm
    today = datetime.now()
    current_year = constants.LUNA_YEARS[today.year]
    luna_years = [cung_td.select_one("span.cung-tieuvan").text for cung_td in cung_tds]
    start_idx = luna_years.index(current_year)

    if "Nam" in am_duong:
        idx_in_main = main_order.index(start_idx)
        order = main_order[idx_in_main:] + main_order[:idx_in_main]
    else:
        idx_in_main = reversed_order.index(start_idx)
        order = reversed_order[idx_in_main:] + reversed_order[:idx_in_main]

    for i in order:
        cung_td = cung_tds[i]
        ten_cung = cung_td.select_one("p.cung-tencung").text
        sao = []
        chinh_tinh = cung_td.select_one(
            "div.cung-top > div.chinh-tinh > p:nth-child(1) > span"
        ).text
        sao.append(chinh_tinh)

        sao_tot_lis = cung_td.select("div.cung-middle > ul.sao-tot > li")
        for sao_tot_el in sao_tot_lis:
            sao.append(sao_tot_el.text)

        sao_xau_lis = cung_td.select("div.cung-middle > ul.sao-xau > li")
        for sao_xau_el in sao_xau_lis:
            sao.append(sao_xau_el.text)

        sao_bottom = cung_td.select_one("div.cung-bottom > p > span").text
        sao.append(sao_bottom)

        data["cung_10yrs"].append({"ten": ten_cung, "sao": sao})

    return data


async def get_page_detail(dob: datetime, time, gender: str):
    context = await new_context()
    try:
        page = await context.new_page()
        await page.goto(constants.COHOC_FORM_URL)

        # Wait for form to be ready
        try:
            await page.wait_for_selector("#btGiaiDoan", timeout=15000)
        except Exception:
            raise RuntimeError("Form page did not load in time")

        # Fill form
        await page.locator(f"//select[@name='ddlNgay']/option[text()='{dob.day}']").click()
        await page.locator(f"//select[@name='ddlThang']/option[text()='{dob.month}']").click()
        await page.locator(f"//select[@name='ddlNam']/option[text()='{dob.year}']").click()
        await page.locator(f"//select[@name='ddlGio']/option[@value='{time}']").click()
        await page.locator(f"//input[@name='GioiTinh'][@value='rd{gender}']").click()

        # Submit
        await page.evaluate('document.getElementById("btGiaiDoan").click()')

        # Wait for navigation
        form_url = page.url
        try:
            await page.wait_for_url(lambda url: url != form_url, timeout=15000)
        except Exception:
            raise RuntimeError("Form did not navigate after submit")

        current_url = page.url

        # IP rate-limit
        if "ip-deny" in current_url or "no-refer-ip-deny" in current_url:
            raise RuntimeError(f"IP denied by tuvi.cohoc.net: {current_url}")

        # Cache-not-found: server generating, wait up to 90s
        if "cache-not-found" in current_url:
            logger.info("Processing page detected, waiting up to 90s...")
            try:
                await page.wait_for_selector("div.thien-ban", timeout=90000)
            except Exception:
                raise RuntimeError(
                    f"Timeout waiting for result after processing page. "
                    f"Server may still be generating cache for {dob.strftime('%d/%m/%Y')}."
                )
        else:
            try:
                await page.wait_for_selector("div.thien-ban", timeout=10000)
            except Exception:
                raise RuntimeError(f"Result page did not load: {current_url}")

        body = await page.content()
        data = parse_body(body)
        return data
    finally:
        await context.close()
```

- [ ] **Step 5: Run offline tests to verify parsing works**

```bash
cd backend && python -m pytest tests/test_scraper_cohoc.py -v -m "not live"
```

Expected: All 7 offline tests PASS (TestGetGioSinhOption: 6, TestParseBody: depends on fixture availability — skipped if no fixture).

- [ ] **Step 6: Commit**

```bash
git add backend/app/services/scraper_cohoc.py backend/tests/test_scraper_cohoc.py backend/tests/fixtures/
git commit -m "feat: add cohoc.net scraper (Playwright async port)"
```

---

### Task 7: tuvi.vn Scraper

**Files:**
- Create: `backend/app/services/scraper_tuvivn.py`
- Create: `backend/tests/test_scraper_tuvivn.py`

- [ ] **Step 1: Write failing tests for tuvi.vn parser**

Create `backend/tests/test_scraper_tuvivn.py`:
```python
import pytest

from app.models.schemas import CungDetail
from app.services.scraper_tuvivn import parse_body, sort_cung_by_month, to_string


class TestToString:
    def test_basic_cleanup(self):
        assert to_string("  Tử   Vi  ") == "Tử Vi"

    def test_removes_dashes(self):
        assert to_string("Thiên - Đồng") == "Thiên Đồng"

    def test_removes_plus(self):
        assert to_string("Sao +Tot") == "Sao Tot"


class TestSortCungByMonth:
    def test_sorts_by_month_number(self):
        cungs = [
            CungDetail(ten="B", sao=[], thang="Th.3"),
            CungDetail(ten="A", sao=[], thang="Th.1"),
            CungDetail(ten="C", sao=[], thang="Th.12"),
        ]
        result = sort_cung_by_month(cungs)
        assert [c.thang for c in result] == ["Th.1", "Th.3", "Th.12"]


class TestParseBody:
    def test_parse_produces_12_cungs(self, tuvivn_html):
        data = parse_body(tuvivn_html)
        assert len(data["cung"]) == 12

    def test_each_cung_has_stars(self, tuvivn_html):
        data = parse_body(tuvivn_html)
        for cung in data["cung"]:
            assert len(cung.sao) >= 1, f"Cung '{cung.ten}' has no stars"

    def test_each_cung_has_month(self, tuvivn_html):
        data = parse_body(tuvivn_html)
        for cung in data["cung"]:
            assert cung.thang is not None and cung.thang != ""

    def test_menh_is_first_cung(self, tuvivn_html):
        data = parse_body(tuvivn_html)
        assert "Mệnh" in data["cung"][0].ten or "mệnh" in data["cung"][0].ten.lower()

    def test_metadata_am_duong(self, tuvivn_html):
        data = parse_body(tuvivn_html)
        assert data.get("am_duong") is not None


@pytest.mark.live
class TestLiveTuViVn:
    """Live integration tests — run with: pytest -m live"""

    def test_determinism(self):
        import asyncio
        from datetime import datetime
        from app.services import scraper_browser
        from app.services.scraper_tuvivn import get_page_detail

        async def run():
            await scraper_browser.start()
            try:
                dob = datetime(1997, 10, 11, 12, 0)
                r1 = await get_page_detail(dob, "Nam", "Test", nam_xem=2026)
                r2 = await get_page_detail(dob, "Nam", "Test", nam_xem=2026)
                return r1, r2
            finally:
                await scraper_browser.shutdown()

        r1, r2 = asyncio.get_event_loop().run_until_complete(run())
        assert r1.cung.cung_12months == r2.cung.cung_12months
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd backend && python -m pytest tests/test_scraper_tuvivn.py -v -m "not live"
```

Expected: FAIL with `ModuleNotFoundError: No module named 'app.services.scraper_tuvivn'`

- [ ] **Step 3: Write tuvi.vn scraper implementation**

Create `backend/app/services/scraper_tuvivn.py`:
```python
import logging
import time
import unicodedata
from datetime import datetime
from typing import Optional

from bs4 import BeautifulSoup

from app.models import schemas
from app.services import constants, soup_utils
from app.services.scraper_browser import new_context

logger = logging.getLogger(__name__)

URL = constants.TUVIVN_FORM_URL


def to_string(text: str):
    text = unicodedata.normalize("NFC", text)
    chars = text.strip().split(" ")
    chars = [c.strip() for c in chars if c not in [" ", "\n", ""]]
    new_str = " ".join(chars)
    new_str = new_str.replace("-", "")
    new_str = new_str.replace("+", "")
    return new_str


def parse_body(body):
    soup = BeautifulSoup(body, "html.parser")

    container = "div.view-thien-ban"
    data = {
        "nam": soup_utils.find_metadata_field(soup, "Năm:", container),
        "menh": to_string(soup_utils.find_metadata_field(soup, "Bản mệnh:", container) or ""),
        "cuc": "",
        "menh_chu": soup_utils.find_metadata_field(soup, "Chủ mệnh:", container),
        "than_chu": soup_utils.find_metadata_field(soup, "Chủ thân:", container),
        "am_duong": soup_utils.find_metadata_field(soup, "Âm dương:", container),
        "cung": [],
    }

    # 12 Cung
    main_order = constants.MAIN_ORDER
    reversed_order = constants.REVERSED_ORDER
    cung_tds = soup.select("td.cung")

    cungs = []
    for td in cung_tds:
        el = td.select_one("p.text-sao-chinh-tinh")
        name = to_string(el.text) if el else ""
        cungs.append(name)

    start = unicodedata.normalize("NFC", "Mệnh")
    start_idx = None
    for idx, name in enumerate(cungs):
        if unicodedata.normalize("NFC", name) == start:
            start_idx = idx
            break

    if start_idx is None:
        raise ValueError(f"Could not find '{start}' cung. Found: {cungs}")

    am_duong = data.get("am_duong", "")
    if am_duong in ["Dương Nam", "Âm Nữ"]:
        idx_in_main = main_order.index(start_idx)
        order = main_order[idx_in_main:] + main_order[:idx_in_main]
    else:
        idx_in_main = reversed_order.index(start_idx)
        order = reversed_order[idx_in_main:] + reversed_order[:idx_in_main]

    for i in order:
        cung_td = cung_tds[i]
        ten_cung = to_string(cung_td.select_one("p.text-sao-chinh-tinh").text)

        thang_el = cung_td.select("div.view-cung-dai-van > p")
        thang = to_string(thang_el[1].text) if len(thang_el) > 1 else ""

        sao = []

        chinh_tinh_els = cung_td.select("div.chinh-tinh p.text-chinh-chinh")
        for el in chinh_tinh_els:
            text = to_string(el.text.strip())
            if text:
                sao.append(text)

        sao_tot_divs = cung_td.select("div.sao-tot > div[data-sao-id]")
        for div in sao_tot_divs:
            classes = div.get("class", [])
            if "d-none" not in classes:
                text = to_string(div.text.strip())
                if text:
                    sao.append(text)

        sao_xau_divs = cung_td.select("div.sao-xau > div[data-sao-id]")
        for div in sao_xau_divs:
            classes = div.get("class", [])
            if "d-none" not in classes:
                text = to_string(div.text.strip())
                if text:
                    sao.append(text)

        bottom_el = cung_td.select_one("div.cung-bottom > span.txt-tiny-mid")
        if bottom_el:
            text = to_string(bottom_el.text.strip())
            if text:
                sao.append(text)

        data["cung"].append(schemas.CungDetail(ten=ten_cung, sao=sao, thang=thang))

    return data


def sort_cung_by_month(cung: list[schemas.CungDetail]):
    return list(sorted(cung, key=lambda x: int(x.thang.replace("Th.", ""))))


async def get_page_detail(
    dob: datetime,
    gender: str,
    full_name: str,
    nam_xem: Optional[int] = None,
) -> schemas.LaSoTuVi:
    context = await new_context()
    try:
        page = await context.new_page()
        await page.goto(URL)
        await page.wait_for_timeout(3000)

        # Scroll form into view
        breadcrumb = page.locator(".breadcrumb")
        if await breadcrumb.count() > 0:
            await breadcrumb.scroll_into_view_if_needed()

        # Name
        await page.locator('input[name="name"]').fill(full_name)

        # Day
        await page.locator(
            f"//select[@name='dayOfDOB']/option[text()='{dob.day}']"
        ).click()

        # Month
        await page.locator(
            f"//select[@name='monthOfDOB']/option[text()='Tháng {dob.month}']"
        ).click()

        # Year
        year_input = page.locator('input[name="yearOfDOB"]')
        await year_input.clear()
        await year_input.fill(str(dob.year))

        # Hour
        await page.locator(
            f"//select[@name='hourOfDOB']/option[text()='{dob.hour} Giờ']"
        ).click()

        # Minute
        await page.locator(
            f"//select[@name='minOfDOB']/option[text()='{dob.minute} Phút']"
        ).click()

        # Calendar: Dương lịch (first radio)
        calendar_radios = page.locator('input[name="calendar"]')
        if await calendar_radios.count() > 0:
            await calendar_radios.first.click()

        # Gender
        gender_radios = page.locator('input[name="gender"]')
        if gender == "Nam" and await gender_radios.count() > 0:
            await gender_radios.first.click()
        elif await gender_radios.count() > 1:
            await gender_radios.nth(1).click()

        # Năm xem
        if nam_xem is not None:
            try:
                await page.locator(
                    f"//select[@name='viewYear']/option[text()='{nam_xem}']"
                ).click(timeout=3000)
            except Exception:
                pass

        # Submit
        await page.locator(
            "//button[@type='submit' and contains(text(), 'Lập lá số')]"
        ).click()

        # Wait for result
        try:
            await page.wait_for_selector("td.cung", timeout=15000)
        except Exception:
            pass

        await page.wait_for_timeout(2000)
        body = await page.content()
        data = parse_body(body)

        la_so = schemas.LaSoTuVi(
            ngay_sinh=dob.strftime("%Y-%m-%d"),
            gio_sinh=dob.strftime("%H:%M"),
            gender=gender,
            am_duong=data["am_duong"],
            menh=data.get("menh"),
            menh_chu=data.get("menh_chu"),
            than_chu=data.get("than_chu"),
            cung=schemas.CungInfo(
                cung_chung=data["cung"],
                cung_10yrs=[],
                cung_12months=sort_cung_by_month(data["cung"]),
            ),
        )
        return la_so
    finally:
        await context.close()
```

- [ ] **Step 4: Run offline tests to verify they pass**

```bash
cd backend && python -m pytest tests/test_scraper_tuvivn.py -v -m "not live"
```

Expected: TestToString (3 PASS), TestSortCungByMonth (1 PASS). TestParseBody tests skipped if no fixture.

- [ ] **Step 5: Commit**

```bash
git add backend/app/services/scraper_tuvivn.py backend/tests/test_scraper_tuvivn.py
git commit -m "feat: add tuvi.vn scraper (Playwright async port)"
```

---

### Task 8: Capture HTML Fixtures from Live Sites

This task captures real HTML from both sites to enable offline parsing tests.

**Files:**
- Create: `backend/tests/fixtures/tuvivn_result.html`
- Create: `backend/tests/fixtures/tuvivn_expected.json`

- [ ] **Step 1: Write a fixture capture script**

Create `backend/tests/capture_fixtures.py`:
```python
"""Run manually to capture HTML fixtures from live sites.

Usage:
    cd backend && python -m tests.capture_fixtures
"""
import asyncio
import json
from datetime import datetime
from pathlib import Path

from app.services import scraper_browser
from app.services.scraper_browser import new_context
from app.services import constants

FIXTURES_DIR = Path(__file__).parent / "fixtures"


async def capture_cohoc():
    context = await new_context()
    page = await context.new_page()

    dob = datetime(1997, 10, 11)
    time_val = 12  # 21h-23h

    await page.goto(constants.COHOC_FORM_URL)
    await page.wait_for_selector("#btGiaiDoan", timeout=15000)

    await page.locator(f"//select[@name='ddlNgay']/option[text()='{dob.day}']").click()
    await page.locator(f"//select[@name='ddlThang']/option[text()='{dob.month}']").click()
    await page.locator(f"//select[@name='ddlNam']/option[text()='{dob.year}']").click()
    await page.locator(f"//select[@name='ddlGio']/option[@value='{time_val}']").click()
    await page.locator("//input[@name='GioiTinh'][@value='rdNam']").click()
    await page.evaluate('document.getElementById("btGiaiDoan").click()')

    await page.wait_for_selector("div.thien-ban", timeout=90000)
    html = await page.content()
    (FIXTURES_DIR / "cohoc_result.html").write_text(html, encoding="utf-8")
    print(f"Saved cohoc_result.html ({len(html)} bytes)")

    from app.services.scraper_cohoc import parse_body
    data = parse_body(html)
    (FIXTURES_DIR / "cohoc_expected.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("Saved cohoc_expected.json")

    await context.close()


async def capture_tuvivn():
    context = await new_context()
    page = await context.new_page()

    dob = datetime(1997, 10, 11, 12, 0)

    await page.goto(constants.TUVIVN_FORM_URL)
    await page.wait_for_timeout(3000)

    await page.locator('input[name="name"]').fill("Test User")
    await page.locator(f"//select[@name='dayOfDOB']/option[text()='{dob.day}']").click()
    await page.locator(f"//select[@name='monthOfDOB']/option[text()='Tháng {dob.month}']").click()
    year_input = page.locator('input[name="yearOfDOB"]')
    await year_input.clear()
    await year_input.fill(str(dob.year))
    await page.locator(f"//select[@name='hourOfDOB']/option[text()='{dob.hour} Giờ']").click()
    await page.locator(f"//select[@name='minOfDOB']/option[text()='{dob.minute} Phút']").click()
    calendar_radios = page.locator('input[name="calendar"]')
    if await calendar_radios.count() > 0:
        await calendar_radios.first.click()
    gender_radios = page.locator('input[name="gender"]')
    await gender_radios.first.click()

    await page.locator("//button[@type='submit' and contains(text(), 'Lập lá số')]").click()
    try:
        await page.wait_for_selector("td.cung", timeout=15000)
    except Exception:
        pass
    await page.wait_for_timeout(2000)

    html = await page.content()
    (FIXTURES_DIR / "tuvivn_result.html").write_text(html, encoding="utf-8")
    print(f"Saved tuvivn_result.html ({len(html)} bytes)")

    from app.services.scraper_tuvivn import parse_body
    data = parse_body(html)
    serializable = {
        "am_duong": data["am_duong"],
        "nam": data["nam"],
        "menh": data["menh"],
        "cung_count": len(data["cung"]),
    }
    (FIXTURES_DIR / "tuvivn_expected.json").write_text(
        json.dumps(serializable, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("Saved tuvivn_expected.json")

    await context.close()


async def main():
    await scraper_browser.start()
    try:
        print("=== Capturing cohoc.net fixture ===")
        await capture_cohoc()
        print("\n=== Capturing tuvi.vn fixture ===")
        await capture_tuvivn()
    finally:
        await scraper_browser.shutdown()

    print("\nDone! Fixtures saved to backend/tests/fixtures/")


if __name__ == "__main__":
    asyncio.run(main())
```

- [ ] **Step 2: Run the capture script**

```bash
cd backend && python -m tests.capture_fixtures
```

Expected: Both HTML files and JSON files saved to `tests/fixtures/`.

- [ ] **Step 3: Verify offline tests now pass with real fixtures**

```bash
cd backend && python -m pytest tests/test_scraper_cohoc.py tests/test_scraper_tuvivn.py -v -m "not live"
```

Expected: All parse tests PASS (no longer skipped).

- [ ] **Step 4: Commit fixtures (but add HTML to .gitignore if too large)**

```bash
# Check sizes
ls -lh backend/tests/fixtures/

# If HTML files are >500KB, gitignore them
echo "backend/tests/fixtures/*.html" >> .gitignore

git add backend/tests/capture_fixtures.py backend/tests/fixtures/*.json .gitignore
git commit -m "feat: add fixture capture script and expected output JSON"
```

---

### Task 9: Full Integration Smoke Test

**Files:**
- Create: `backend/tests/test_integration.py`

- [ ] **Step 1: Write integration smoke test**

Create `backend/tests/test_integration.py`:
```python
"""End-to-end integration test: scrape both sites, verify combined output.

Run with: pytest -m live tests/test_integration.py -v
"""
import asyncio

import pytest

from app.models.schemas import LaSoTuVi


@pytest.mark.live
class TestFullScrape:
    @pytest.fixture(autouse=True)
    def _browser(self):
        from app.services import scraper_browser

        asyncio.get_event_loop().run_until_complete(scraper_browser.start())
        yield
        asyncio.get_event_loop().run_until_complete(scraper_browser.shutdown())

    def test_cohoc_and_tuvivn_produce_valid_output(self):
        from datetime import datetime
        from app.services.scraper_cohoc import get_page_detail as cohoc_scrape
        from app.services.scraper_tuvivn import get_page_detail as tuvivn_scrape

        async def run():
            dob = datetime(1997, 10, 11)
            cohoc_data = await cohoc_scrape(dob, 12, "Nam")

            dob_vn = datetime(1997, 10, 11, 12, 0)
            tuvivn_data = await tuvivn_scrape(dob_vn, "Nam", "Test User", nam_xem=2026)

            return cohoc_data, tuvivn_data

        cohoc, tuvivn = asyncio.get_event_loop().run_until_complete(run())

        # cohoc: lifetime + 10yr
        assert len(cohoc["cung"]) == 12
        assert len(cohoc["cung_10yrs"]) == 12
        assert cohoc["am_duong"] is not None

        # tuvivn: monthly
        assert isinstance(tuvivn, LaSoTuVi)
        assert tuvivn.cung is not None
        assert len(tuvivn.cung.cung_12months) == 12
        for cung in tuvivn.cung.cung_12months:
            assert cung.thang is not None
```

- [ ] **Step 2: Run integration test (requires network)**

```bash
cd backend && python -m pytest -m live tests/test_integration.py -v
```

Expected: 1 test PASS — both scrapers return valid data.

- [ ] **Step 3: Run full test suite to verify nothing is broken**

```bash
cd backend && python -m pytest tests/ -v -m "not live"
```

Expected: All offline tests PASS.

- [ ] **Step 4: Commit**

```bash
git add backend/tests/test_integration.py
git commit -m "feat: add end-to-end integration smoke test"
```

---

### Task 10: Final Cleanup & pytest Configuration

**Files:**
- Create: `backend/pytest.ini`

- [ ] **Step 1: Add pytest configuration**

Create `backend/pytest.ini`:
```ini
[pytest]
markers =
    live: marks tests that hit live websites (deselect with '-m "not live"')
asyncio_mode = auto
pythonpath = .
```

- [ ] **Step 2: Verify full offline suite passes cleanly**

```bash
cd backend && python -m pytest tests/ -v -m "not live"
```

Expected: All tests PASS, no warnings about unknown markers.

- [ ] **Step 3: Commit**

```bash
git add backend/pytest.ini
git commit -m "chore: add pytest configuration with live marker"
```
