# Scoring Engine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the scoring engine that transforms scraper `LasoData` into 8 dimensions × 3 timeframes of scored chart data with alert detection.

**Architecture:** Single `ScoringEngine` class loads `laso_points.xlsx` at init into an in-memory dict, then `score(LasoData) → ScoringResult` is pure computation. Anchor always from lifetime data. TDD throughout — each formula step has tests before implementation.

**Tech Stack:** Python 3.11+, openpyxl, python-slugify, dataclasses, pytest

---

## File Structure

| File | Responsibility |
|------|---------------|
| `backend/app/models/schemas.py` | Shared Pydantic/dataclass models (already planned in Task 01 — extend with scoring output types) |
| `backend/app/constants.py` | `HOUSE_WEIGHTS`, `SUMMARY_AGE_WEIGHTS`, `DIMENSION_LABELS`, `DIMENSIONS` |
| `backend/app/services/scoring.py` | `ScoringEngine` class — xlsx loading, raw scores, anchor, final scores, alerts, summary |
| `backend/tests/test_constants.py` | Sanity checks on constants (weight sums, dimension coverage) |
| `backend/tests/test_scoring_xlsx.py` | Star table loading + lookup tests |
| `backend/tests/test_scoring_raw.py` | Raw score calculation tests |
| `backend/tests/test_scoring_anchor.py` | Anchor (house weighting) tests |
| `backend/tests/test_scoring_final.py` | Final score + chart assembly tests |
| `backend/tests/test_scoring_alerts.py` | Alert detection tests |
| `backend/tests/test_scoring_summary.py` | Summary score tests |
| `backend/tests/test_scoring_integration.py` | End-to-end: LasoData → ScoringResult |
| `backend/tests/fixtures/sample_laso.json` | Test fixture with known star placements |

---

### Task 1: Constants + Output Schemas

**Files:**
- Create: `backend/app/constants.py`
- Modify: `backend/app/models/schemas.py` (add scoring output types)
- Create: `backend/tests/test_constants.py`

- [ ] **Step 1: Write failing test for constants**

Create `backend/tests/test_constants.py`:
```python
from backend.app.constants import (
    HOUSE_WEIGHTS,
    SUMMARY_AGE_WEIGHTS,
    DIMENSION_LABELS,
    DIMENSIONS,
)


def test_dimensions_count():
    assert len(DIMENSIONS) == 8


def test_dimensions_order():
    assert DIMENSIONS[0] == "van_menh"
    assert DIMENSIONS[-1] == "con_cai"


def test_house_weights_cover_all_dimensions():
    for dim in DIMENSIONS:
        assert dim in HOUSE_WEIGHTS, f"Missing house weights for {dim}"


def test_house_weights_sum_to_one():
    for dim, weights in HOUSE_WEIGHTS.items():
        total = sum(w for _, w in weights)
        assert abs(total - 1.0) < 0.01, f"{dim} weights sum to {total}, expected 1.0"


def test_summary_age_weights_cover_12_ages():
    ages = sorted(SUMMARY_AGE_WEIGHTS.keys())
    assert ages == list(range(0, 120, 10))


def test_dimension_labels_cover_all():
    for dim in DIMENSIONS:
        assert dim in DIMENSION_LABELS
        assert isinstance(DIMENSION_LABELS[dim], str)
        assert len(DIMENSION_LABELS[dim]) > 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /mnt/d/Working/TBTesu/TuViApp && python -m pytest backend/tests/test_constants.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Create constants module**

Create `backend/app/constants.py`:
```python
"""Scoring engine constants — house weights, age weights, dimension config."""

DIMENSIONS: list[str] = [
    "van_menh",
    "su_nghiep",
    "tien_bac",
    "hon_nhan",
    "suc_khoe",
    "dat_dai",
    "hoc_tap",
    "con_cai",
]

# House weighting anchor config per dimension.
# Each entry: (cung_name, weight). Weights sum to 1.0.
# "thân" is a dynamic reference resolved via laso.than_cu at runtime.
HOUSE_WEIGHTS: dict[str, list[tuple[str, float]]] = {
    "van_menh": [("mệnh", 0.4), ("thân", 0.2), ("quan lộc", 0.2), ("tài bạch", 0.2)],
    "su_nghiep": [("quan lộc", 0.4), ("mệnh", 0.2), ("tài bạch", 0.2), ("thiên di", 0.2)],
    "tien_bac": [("tài bạch", 0.4), ("mệnh", 0.2), ("quan lộc", 0.2), ("điền trạch", 0.2)],
    "hon_nhan": [("phu thê", 0.4), ("mệnh", 0.2), ("phúc đức", 0.2), ("nô bộc", 0.2)],
    "suc_khoe": [("tật ách", 0.6), ("phúc đức", 0.4)],
    "dat_dai": [("tật ách", 0.6), ("phúc đức", 0.4)],
    "hoc_tap": [("mệnh", 0.5), ("quan lộc", 0.2), ("thiên di", 0.3)],
    "con_cai": [("tử tức", 0.5), ("điền trạch", 0.1), ("phúc đức", 0.4)],
}

# 3-tier age weights for summary_score calculation.
# Prime years (20-60) weighted higher, childhood/old age weighted lower.
SUMMARY_AGE_WEIGHTS: dict[int, float] = {
    0: 0.5,
    10: 0.5,
    20: 1.5,
    30: 1.5,
    40: 1.5,
    50: 1.5,
    60: 1.5,
    70: 1.0,
    80: 1.0,
    90: 1.0,
    100: 0.5,
    110: 0.5,
}

DIMENSION_LABELS: dict[str, str] = {
    "van_menh": "Vận Mệnh",
    "su_nghiep": "Sự Nghiệp",
    "tien_bac": "Tiền Bạc",
    "hon_nhan": "Hôn Nhân",
    "suc_khoe": "Sức Khỏe",
    "dat_dai": "Đất Đai",
    "hoc_tap": "Học Tập",
    "con_cai": "Con Cái",
}
```

- [ ] **Step 4: Add scoring output types to schemas**

Add the following dataclasses to `backend/app/models/schemas.py` (below the existing scraper types — `Star`, `Cung`, `MonthlyCung`, `LasoData`):

```python
from dataclasses import dataclass, field


@dataclass
class StarRow:
    """One row from laso_points.xlsx, indexed by slug."""
    slug: str
    name: str
    point: int
    weights: dict[str, float] = field(default_factory=dict)
    alert_tags: dict[str, dict[int, str | None]] = field(default_factory=dict)
    pct_fvg: dict[int, str | None] = field(default_factory=dict)


@dataclass
class ScorePoint:
    """One data point on a chart line."""
    period: str
    duong: float
    am: float
    tb: float


@dataclass
class Alert:
    """A detected score change alert."""
    type: str        # "positive" | "negative"
    dimension: str
    period: str
    tag: str
    level: int       # 30 | 50
    star_name: str


@dataclass
class DimensionScores:
    """Complete scoring output for one dimension."""
    dimension: str
    label: str
    lifetime: list[ScorePoint] = field(default_factory=list)
    decade: list[ScorePoint] = field(default_factory=list)
    monthly: list[ScorePoint] = field(default_factory=list)
    alerts: list[Alert] = field(default_factory=list)
    summary_score: float = 0.0


@dataclass
class ScoringResult:
    """Complete scoring output for all dimensions."""
    dimensions: dict[str, DimensionScores] = field(default_factory=dict)
    all_alerts: list[Alert] = field(default_factory=list)
```

- [ ] **Step 5: Run tests**

Run: `cd /mnt/d/Working/TBTesu/TuViApp && python -m pytest backend/tests/test_constants.py -v`
Expected: All 6 tests PASS

- [ ] **Step 6: Commit**

```bash
git add backend/app/constants.py backend/app/models/schemas.py backend/tests/test_constants.py
git commit -m "feat(scoring): add constants and output schemas"
```

---

### Task 2: Star Table Loading from xlsx

**Files:**
- Create: `backend/app/services/scoring.py` (partial — `_load_star_table` only)
- Create: `backend/tests/test_scoring_xlsx.py`

- [ ] **Step 1: Write failing tests for xlsx loading**

Create `backend/tests/test_scoring_xlsx.py`:
```python
import pytest
from backend.app.services.scoring import ScoringEngine
from backend.app.models.schemas import StarRow

XLSX_PATH = "data/laso_points.xlsx"


@pytest.fixture(scope="module")
def engine():
    return ScoringEngine(xlsx_path=XLSX_PATH)


def test_star_table_loaded(engine):
    assert len(engine._star_table) > 200


def test_star_table_no_duplicates(engine):
    # 223 rows, 1 known duplicate → expect ≥ 222 unique
    assert len(engine._star_table) >= 222


def test_star_row_structure(engine):
    # Pick a known star — "Tử Vi" should always exist
    from slugify import slugify
    slug = slugify("Tử Vi".lower())
    row = engine._star_table.get(slug)
    assert row is not None
    assert isinstance(row, StarRow)
    assert isinstance(row.point, int)
    assert isinstance(row.weights, dict)
    assert "su_nghiep" in row.weights


def test_empty_weight_defaults_to_one(engine):
    """van_menh column is all NaN → all stars should have weight 1.0."""
    for slug, row in engine._star_table.items():
        assert row.weights["van_menh"] == 1.0, (
            f"Star {row.name} has van_menh weight {row.weights['van_menh']}, expected 1.0"
        )


def test_point_range(engine):
    for slug, row in engine._star_table.items():
        assert -5 <= row.point <= 10, f"Star {row.name} has point {row.point} out of range"


def test_pct_fvg_values(engine):
    valid_values = {"pos", "neg", None}
    for slug, row in engine._star_table.items():
        for level in (30, 50):
            val = row.pct_fvg.get(level)
            assert val in valid_values, f"Star {row.name} pct_fvg_{level} = {val}"


def test_alert_tags_structure(engine):
    """Stars with pct_fvg should have corresponding tag columns."""
    found_any_tag = False
    for slug, row in engine._star_table.items():
        for dim in ["su_nghiep", "tien_bac", "hon_nhan", "suc_khoe", "dat_dai", "hoc_tap", "con_cai"]:
            for level in (30, 50):
                tag = row.alert_tags.get(dim, {}).get(level)
                if tag is not None:
                    found_any_tag = True
                    assert isinstance(tag, str)
                    assert len(tag) > 0
    assert found_any_tag, "No alert tags found in any star"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /mnt/d/Working/TBTesu/TuViApp && python -m pytest backend/tests/test_scoring_xlsx.py -v`
Expected: FAIL with `ImportError`

- [ ] **Step 3: Implement `ScoringEngine.__init__` + `_load_star_table`**

Create `backend/app/services/scoring.py`:
```python
"""Scoring engine — transforms LasoData into scored dimensions with alerts."""

import logging
from pathlib import Path

from openpyxl import load_workbook
from slugify import slugify

from backend.app.constants import DIMENSIONS
from backend.app.models.schemas import (
    StarRow,
    ScorePoint,
    Alert,
    DimensionScores,
    ScoringResult,
)

logger = logging.getLogger(__name__)

# Dimension columns that have alert tag columns in the xlsx.
# van_menh has NO alerts so it has no tag columns.
_ALERT_DIMENSIONS = [d for d in DIMENSIONS if d != "van_menh"]


class ScoringEngine:
    """Stateless scoring calculator. Load xlsx once, reuse across requests."""

    def __init__(self, xlsx_path: str = "data/laso_points.xlsx"):
        self._star_table: dict[str, StarRow] = self._load_star_table(xlsx_path)

    def _load_star_table(self, path: str) -> dict[str, StarRow]:
        wb = load_workbook(path, read_only=True, data_only=True)
        ws = wb["laso_points"]

        # Read header row to build column index
        rows = ws.iter_rows(values_only=True)
        header = [str(h).strip() if h else "" for h in next(rows)]
        col = {name: idx for idx, name in enumerate(header)}

        table: dict[str, StarRow] = {}

        for row_vals in rows:
            sao_raw = row_vals[col["sao"]]
            if sao_raw is None:
                continue

            slug = slugify(str(sao_raw).lower())
            if slug in table:
                logger.warning("Duplicate star slug '%s' (name: %s) — keeping first", slug, sao_raw)
                continue

            point_val = row_vals[col["point"]]
            point = int(point_val) if point_val is not None else 0

            # Build dimension weights — empty/NaN → 1.0
            weights: dict[str, float] = {}
            for dim in DIMENSIONS:
                val = row_vals[col[dim]] if dim in col else None
                if val is None or val == "":
                    weights[dim] = 1.0
                else:
                    try:
                        weights[dim] = float(val)
                    except (ValueError, TypeError):
                        weights[dim] = 1.0

            # Build pct_fvg
            pct_fvg: dict[int, str | None] = {}
            for level in (30, 50):
                fvg_col = f"pct_fvg_{level}"
                if fvg_col in col:
                    val = row_vals[col[fvg_col]]
                    if val and str(val).strip() in ("pos", "neg"):
                        pct_fvg[level] = str(val).strip()
                    else:
                        pct_fvg[level] = None
                else:
                    pct_fvg[level] = None

            # Build alert tags per dimension per level
            alert_tags: dict[str, dict[int, str | None]] = {}
            for dim in _ALERT_DIMENSIONS:
                dim_tags: dict[int, str | None] = {}
                for level in (30, 50):
                    tag_col = f"{dim}_tag_{level}"
                    if tag_col in col:
                        val = row_vals[col[tag_col]]
                        if val and str(val).strip():
                            dim_tags[level] = str(val).strip()
                        else:
                            dim_tags[level] = None
                    else:
                        dim_tags[level] = None
                alert_tags[dim] = dim_tags

            table[slug] = StarRow(
                slug=slug,
                name=str(sao_raw),
                point=point,
                weights=weights,
                alert_tags=alert_tags,
                pct_fvg=pct_fvg,
            )

        wb.close()
        logger.info("Loaded %d stars from %s", len(table), path)
        return table
```

- [ ] **Step 4: Run tests**

Run: `cd /mnt/d/Working/TBTesu/TuViApp && python -m pytest backend/tests/test_scoring_xlsx.py -v`
Expected: All 7 tests PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app/services/scoring.py backend/tests/test_scoring_xlsx.py
git commit -m "feat(scoring): load star table from laso_points.xlsx"
```

---

### Task 3: Raw Score Calculation

**Files:**
- Modify: `backend/app/services/scoring.py` (add `_build_raw_scores`)
- Create: `backend/tests/test_scoring_raw.py`

- [ ] **Step 1: Write failing tests for raw scores**

Create `backend/tests/test_scoring_raw.py`:
```python
import pytest
from dataclasses import dataclass
from backend.app.services.scoring import ScoringEngine
from backend.app.models.schemas import StarRow

XLSX_PATH = "data/laso_points.xlsx"


@pytest.fixture(scope="module")
def engine():
    return ScoringEngine(xlsx_path=XLSX_PATH)


@dataclass
class FakeStar:
    slug: str


@dataclass
class FakeCung:
    name: str
    stars: list


def test_raw_scores_positive_stars(engine):
    """Cung with only positive-point stars → raw_pos > 0, raw_neg == 0."""
    # Find a star with positive point from the table
    pos_stars = [s for s in engine._star_table.values() if s.point > 0]
    assert len(pos_stars) > 0
    star = pos_stars[0]

    cungs = [FakeCung(name="test_cung", stars=[FakeStar(slug=star.slug)])]
    raws = engine._build_raw_scores(cungs, "su_nghiep")

    assert "test_cung" in raws
    raw_pos, raw_neg = raws["test_cung"]
    assert raw_pos > 0
    assert raw_neg == 0.0


def test_raw_scores_negative_stars(engine):
    """Cung with only negative-point stars → raw_pos == 0, raw_neg < 0."""
    neg_stars = [s for s in engine._star_table.values() if s.point < 0]
    assert len(neg_stars) > 0
    star = neg_stars[0]

    cungs = [FakeCung(name="test_cung", stars=[FakeStar(slug=star.slug)])]
    raws = engine._build_raw_scores(cungs, "su_nghiep")

    raw_pos, raw_neg = raws["test_cung"]
    assert raw_pos == 0.0
    assert raw_neg < 0


def test_raw_scores_zero_point_goes_to_neg(engine):
    """Stars with point == 0 contribute to neg bucket (point ≤ 0)."""
    zero_stars = [s for s in engine._star_table.values() if s.point == 0]
    if not zero_stars:
        pytest.skip("No zero-point stars in dataset")
    star = zero_stars[0]

    cungs = [FakeCung(name="test_cung", stars=[FakeStar(slug=star.slug)])]
    raws = engine._build_raw_scores(cungs, "su_nghiep")

    raw_pos, raw_neg = raws["test_cung"]
    # 0 * weight = 0, so both should be 0
    assert raw_pos == 0.0
    assert raw_neg == 0.0


def test_raw_scores_formula_point_times_weight(engine):
    """Verify raw = point × weight for a known star."""
    from slugify import slugify
    slug = slugify("Tử Vi".lower())
    star_row = engine._star_table[slug]

    cungs = [FakeCung(name="cung_a", stars=[FakeStar(slug=slug)])]
    raws = engine._build_raw_scores(cungs, "su_nghiep")

    raw_pos, raw_neg = raws["cung_a"]
    expected = star_row.point * star_row.weights["su_nghiep"]
    if star_row.point > 0:
        assert abs(raw_pos - expected) < 0.001
        assert raw_neg == 0.0
    else:
        assert raw_pos == 0.0
        assert abs(raw_neg - expected) < 0.001


def test_raw_scores_van_menh_uses_weight_one(engine):
    """van_menh column is all NaN → weight defaults to 1.0, so raw = point × 1."""
    from slugify import slugify
    slug = slugify("Tử Vi".lower())
    star_row = engine._star_table[slug]

    cungs = [FakeCung(name="cung_a", stars=[FakeStar(slug=slug)])]
    raws = engine._build_raw_scores(cungs, "van_menh")

    raw_pos, raw_neg = raws["cung_a"]
    expected = star_row.point * 1.0  # weight should be 1.0
    if star_row.point > 0:
        assert abs(raw_pos - expected) < 0.001


def test_raw_scores_unknown_star_skipped(engine):
    """Unknown star slug → skipped with no error."""
    cungs = [FakeCung(name="cung_a", stars=[FakeStar(slug="nonexistent-star-xyz")])]
    raws = engine._build_raw_scores(cungs, "su_nghiep")
    raw_pos, raw_neg = raws["cung_a"]
    assert raw_pos == 0.0
    assert raw_neg == 0.0


def test_raw_scores_multiple_cungs(engine):
    """Multiple cungs each get their own entry."""
    stars = [s for s in engine._star_table.values() if s.point > 0][:2]
    cungs = [
        FakeCung(name="mệnh", stars=[FakeStar(slug=stars[0].slug)]),
        FakeCung(name="quan lộc", stars=[FakeStar(slug=stars[1].slug)]),
    ]
    raws = engine._build_raw_scores(cungs, "su_nghiep")
    assert "mệnh" in raws
    assert "quan lộc" in raws


def test_raw_scores_cung_name_lowered(engine):
    """Cung names are lowered in the output dict keys."""
    stars = [s for s in engine._star_table.values() if s.point > 0][:1]
    cungs = [FakeCung(name="Mệnh", stars=[FakeStar(slug=stars[0].slug)])]
    raws = engine._build_raw_scores(cungs, "su_nghiep")
    assert "mệnh" in raws
    assert "Mệnh" not in raws
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /mnt/d/Working/TBTesu/TuViApp && python -m pytest backend/tests/test_scoring_raw.py -v`
Expected: FAIL with `AttributeError: 'ScoringEngine' object has no attribute '_build_raw_scores'`

- [ ] **Step 3: Implement `_build_raw_scores`**

Add to `ScoringEngine` class in `backend/app/services/scoring.py`:

```python
    def _build_raw_scores(
        self, cungs: list, dim: str
    ) -> dict[str, tuple[float, float]]:
        """Calculate raw pos/neg scores per cung for a dimension.

        Args:
            cungs: List of Cung (or any object with .name and .stars[].slug).
            dim: Dimension key (e.g., "su_nghiep").

        Returns:
            Dict mapping lowered cung name → (raw_pos, raw_neg).
        """
        result: dict[str, tuple[float, float]] = {}

        for cung in cungs:
            raw_pos = 0.0
            raw_neg = 0.0

            for star in cung.stars:
                row = self._star_table.get(star.slug)
                if row is None:
                    logger.warning(
                        "Star not found in table: slug='%s' (cung='%s')",
                        star.slug,
                        cung.name,
                    )
                    continue

                weight = row.weights.get(dim, 1.0)
                contribution = row.point * weight

                if row.point > 0:
                    raw_pos += contribution
                else:
                    raw_neg += contribution

            result[cung.name.lower()] = (raw_pos, raw_neg)

        return result
```

- [ ] **Step 4: Run tests**

Run: `cd /mnt/d/Working/TBTesu/TuViApp && python -m pytest backend/tests/test_scoring_raw.py -v`
Expected: All 8 tests PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app/services/scoring.py backend/tests/test_scoring_raw.py
git commit -m "feat(scoring): implement raw score calculation"
```

---

### Task 4: Anchor (House Weighting) Calculation

**Files:**
- Modify: `backend/app/services/scoring.py` (add `_calc_anchor`)
- Create: `backend/tests/test_scoring_anchor.py`

- [ ] **Step 1: Write failing tests for anchor calculation**

Create `backend/tests/test_scoring_anchor.py`:
```python
import pytest
from dataclasses import dataclass
from backend.app.services.scoring import ScoringEngine
from backend.app.constants import HOUSE_WEIGHTS

XLSX_PATH = "data/laso_points.xlsx"


@pytest.fixture(scope="module")
def engine():
    return ScoringEngine(xlsx_path=XLSX_PATH)


@dataclass
class FakeStar:
    slug: str


@dataclass
class FakeCung:
    name: str
    stars: list


def _make_cungs_with_known_star(engine, cung_names):
    """Create fake cungs where each cung has one known positive star."""
    pos_stars = [s for s in engine._star_table.values() if s.point > 0]
    cungs = []
    for i, name in enumerate(cung_names):
        star = pos_stars[i % len(pos_stars)]
        cungs.append(FakeCung(name=name, stars=[FakeStar(slug=star.slug)]))
    return cungs


def test_anchor_su_nghiep_uses_correct_cungs(engine):
    """su_nghiep anchor: quan lộc 0.4, mệnh 0.2, tài bạch 0.2, thiên di 0.2."""
    cung_names = [
        "Mệnh", "Phụ Mẫu", "Phúc Đức", "Điền Trạch", "Quan Lộc", "Nô Bộc",
        "Thiên Di", "Tật Ách", "Tài Bạch", "Tử Tức", "Phu Thê", "Huynh Đệ",
    ]
    cungs = _make_cungs_with_known_star(engine, cung_names)
    lifetime_raws = engine._build_raw_scores(cungs, "su_nghiep")

    anchor_pos, anchor_neg = engine._calc_anchor(lifetime_raws, "su_nghiep", than_cu="Thiên Di")

    # Verify anchor is a weighted sum (not zero if cungs have stars)
    assert anchor_pos > 0 or anchor_neg < 0


def test_anchor_van_menh_resolves_than(engine):
    """van_menh has 'thân' in config — must resolve to than_cu cung."""
    cung_names = [
        "Mệnh", "Phụ Mẫu", "Phúc Đức", "Điền Trạch", "Quan Lộc", "Nô Bộc",
        "Thiên Di", "Tật Ách", "Tài Bạch", "Tử Tức", "Phu Thê", "Huynh Đệ",
    ]
    cungs = _make_cungs_with_known_star(engine, cung_names)
    lifetime_raws = engine._build_raw_scores(cungs, "van_menh")

    # than_cu = "Quan Lộc" → "thân" should resolve to "quan lộc"
    anchor_pos, anchor_neg = engine._calc_anchor(lifetime_raws, "van_menh", than_cu="Quan Lộc")
    assert isinstance(anchor_pos, float)
    assert isinstance(anchor_neg, float)


def test_anchor_formula_manual_check(engine):
    """Manually verify anchor = Σ(raw_score[cung] × house_weight) for suc_khoe."""
    cung_names = [
        "Mệnh", "Phụ Mẫu", "Phúc Đức", "Điền Trạch", "Quan Lộc", "Nô Bộc",
        "Thiên Di", "Tật Ách", "Tài Bạch", "Tử Tức", "Phu Thê", "Huynh Đệ",
    ]
    cungs = _make_cungs_with_known_star(engine, cung_names)
    lifetime_raws = engine._build_raw_scores(cungs, "suc_khoe")

    anchor_pos, anchor_neg = engine._calc_anchor(lifetime_raws, "suc_khoe", than_cu="Thiên Di")

    # suc_khoe: tật ách × 0.6 + phúc đức × 0.4
    tat_ach_pos, tat_ach_neg = lifetime_raws["tật ách"]
    phuc_duc_pos, phuc_duc_neg = lifetime_raws["phúc đức"]
    expected_pos = tat_ach_pos * 0.6 + phuc_duc_pos * 0.4
    expected_neg = tat_ach_neg * 0.6 + phuc_duc_neg * 0.4

    assert abs(anchor_pos - expected_pos) < 0.001
    assert abs(anchor_neg - expected_neg) < 0.001


def test_anchor_missing_cung_contributes_zero(engine):
    """If a cung referenced in house weights is missing from raws → 0 contribution."""
    # Only provide "mệnh", missing "quan lộc", "tài bạch", "thiên di"
    pos_stars = [s for s in engine._star_table.values() if s.point > 0]
    cungs = [FakeCung(name="Mệnh", stars=[FakeStar(slug=pos_stars[0].slug)])]
    lifetime_raws = engine._build_raw_scores(cungs, "su_nghiep")

    anchor_pos, anchor_neg = engine._calc_anchor(lifetime_raws, "su_nghiep", than_cu="Thiên Di")

    # Only mệnh contributes (weight 0.2), others are 0
    menh_pos, _ = lifetime_raws["mệnh"]
    expected_pos = menh_pos * 0.2
    assert abs(anchor_pos - expected_pos) < 0.001


def test_anchor_all_dimensions_produce_values(engine):
    """All 8 dimensions produce anchor values without errors."""
    cung_names = [
        "Mệnh", "Phụ Mẫu", "Phúc Đức", "Điền Trạch", "Quan Lộc", "Nô Bộc",
        "Thiên Di", "Tật Ách", "Tài Bạch", "Tử Tức", "Phu Thê", "Huynh Đệ",
    ]
    cungs = _make_cungs_with_known_star(engine, cung_names)

    for dim in HOUSE_WEIGHTS:
        lifetime_raws = engine._build_raw_scores(cungs, dim)
        anchor_pos, anchor_neg = engine._calc_anchor(lifetime_raws, dim, than_cu="Thiên Di")
        assert isinstance(anchor_pos, float)
        assert isinstance(anchor_neg, float)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /mnt/d/Working/TBTesu/TuViApp && python -m pytest backend/tests/test_scoring_anchor.py -v`
Expected: FAIL with `AttributeError: 'ScoringEngine' object has no attribute '_calc_anchor'`

- [ ] **Step 3: Implement `_calc_anchor`**

Add to `ScoringEngine` class in `backend/app/services/scoring.py`:

```python
    def _calc_anchor(
        self,
        lifetime_raws: dict[str, tuple[float, float]],
        dim: str,
        than_cu: str,
    ) -> tuple[float, float]:
        """Calculate house weighting anchor from lifetime raw scores.

        Args:
            lifetime_raws: Dict from _build_raw_scores (cung_name_lower → (pos, neg)).
            dim: Dimension key.
            than_cu: Which cung "Thân" resides in (e.g., "Quan Lộc").

        Returns:
            (anchor_pos, anchor_neg) tuple.
        """
        anchor_pos = 0.0
        anchor_neg = 0.0

        for cung_name, house_weight in HOUSE_WEIGHTS[dim]:
            resolved = than_cu.lower() if cung_name == "thân" else cung_name
            raw_pos, raw_neg = lifetime_raws.get(resolved, (0.0, 0.0))
            anchor_pos += raw_pos * house_weight
            anchor_neg += raw_neg * house_weight

        return anchor_pos, anchor_neg
```

Also add the import at the top of `scoring.py`:
```python
from backend.app.constants import DIMENSIONS, HOUSE_WEIGHTS
```

- [ ] **Step 4: Run tests**

Run: `cd /mnt/d/Working/TBTesu/TuViApp && python -m pytest backend/tests/test_scoring_anchor.py -v`
Expected: All 5 tests PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app/services/scoring.py backend/tests/test_scoring_anchor.py
git commit -m "feat(scoring): implement anchor (house weighting) calculation"
```

---

### Task 5: Final Scores + Chart Assembly

**Files:**
- Modify: `backend/app/services/scoring.py` (add `_calc_final`, `_summary_score`)
- Create: `backend/tests/test_scoring_final.py`

- [ ] **Step 1: Write failing tests for final scores**

Create `backend/tests/test_scoring_final.py`:
```python
import pytest
from backend.app.services.scoring import ScoringEngine
from backend.app.models.schemas import ScorePoint

XLSX_PATH = "data/laso_points.xlsx"


@pytest.fixture(scope="module")
def engine():
    return ScoringEngine(xlsx_path=XLSX_PATH)


def test_calc_final_formula(engine):
    """final_pos = (raw + anchor) / 2, tb = pos + neg."""
    raws = {
        "cung_a": (10.0, -4.0),
        "cung_b": (6.0, -2.0),
    }
    anchor = (8.0, -3.0)
    periods = ["P1", "P2"]
    cung_order = ["cung_a", "cung_b"]

    points = engine._calc_final(raws, anchor, periods, cung_order)

    assert len(points) == 2

    # cung_a: final_pos = (10 + 8) / 2 = 9.0, final_neg = (-4 + -3) / 2 = -3.5
    assert abs(points[0].duong - 9.0) < 0.001
    assert abs(points[0].am - (-3.5)) < 0.001
    assert abs(points[0].tb - 5.5) < 0.001
    assert points[0].period == "P1"

    # cung_b: final_pos = (6 + 8) / 2 = 7.0, final_neg = (-2 + -3) / 2 = -2.5
    assert abs(points[1].duong - 7.0) < 0.001
    assert abs(points[1].am - (-2.5)) < 0.001
    assert abs(points[1].tb - 4.5) < 0.001
    assert points[1].period == "P2"


def test_calc_final_tb_is_algebraic_sum(engine):
    """tb = duong + am, NOT average."""
    raws = {"c": (20.0, -10.0)}
    anchor = (0.0, 0.0)
    points = engine._calc_final(raws, anchor, ["X"], ["c"])

    # duong = (20 + 0) / 2 = 10, am = (-10 + 0) / 2 = -5, tb = 10 + (-5) = 5
    assert abs(points[0].tb - (points[0].duong + points[0].am)) < 0.001
    assert abs(points[0].tb - 5.0) < 0.001


def test_calc_final_missing_cung_returns_anchor_only(engine):
    """If a cung is not in raws, raw = (0, 0), so final = anchor / 2."""
    raws = {}
    anchor = (10.0, -6.0)
    points = engine._calc_final(raws, anchor, ["P1"], ["missing_cung"])

    assert abs(points[0].duong - 5.0) < 0.001
    assert abs(points[0].am - (-3.0)) < 0.001


def test_summary_score_weighted_average(engine):
    """Summary = weighted average of tb using SUMMARY_AGE_WEIGHTS."""
    from backend.app.constants import SUMMARY_AGE_WEIGHTS

    # All tb = 10.0 → summary should be 10.0 regardless of weights
    points = [ScorePoint(period=f"{age}-{age+10}", duong=15.0, am=-5.0, tb=10.0)
              for age in range(0, 120, 10)]

    summary = engine._summary_score(points)
    assert abs(summary - 10.0) < 0.001


def test_summary_score_prime_years_weighted_higher(engine):
    """Prime years (20-60) should dominate when their values differ from others."""
    points = []
    for age in range(0, 120, 10):
        if 20 <= age <= 60:
            tb = 20.0  # high for prime years
        else:
            tb = 0.0   # zero for non-prime
        points.append(ScorePoint(period=f"{age}-{age+10}", duong=tb, am=0.0, tb=tb))

    summary = engine._summary_score(points)
    # Prime years dominate → summary should be closer to 20 than to 0
    assert summary > 10.0


def test_summary_score_12_points_required(engine):
    """Must handle exactly 12 points (matching SUMMARY_AGE_WEIGHTS keys)."""
    points = [ScorePoint(period=f"{age}-{age+10}", duong=5.0, am=-2.0, tb=3.0)
              for age in range(0, 120, 10)]
    assert len(points) == 12

    summary = engine._summary_score(points)
    assert abs(summary - 3.0) < 0.001
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /mnt/d/Working/TBTesu/TuViApp && python -m pytest backend/tests/test_scoring_final.py -v`
Expected: FAIL with `AttributeError`

- [ ] **Step 3: Implement `_calc_final` and `_summary_score`**

Add to `ScoringEngine` class in `backend/app/services/scoring.py`:

```python
    def _calc_final(
        self,
        raws: dict[str, tuple[float, float]],
        anchor: tuple[float, float],
        periods: list[str],
        cung_order: list[str],
    ) -> list[ScorePoint]:
        """Calculate final scores for a list of cungs.

        Args:
            raws: cung_name_lower → (raw_pos, raw_neg).
            anchor: (anchor_pos, anchor_neg) from _calc_anchor.
            periods: X-axis labels in order.
            cung_order: Cung names (lowered) matching periods order.

        Returns:
            List of ScorePoint, one per period.
        """
        anchor_pos, anchor_neg = anchor
        points: list[ScorePoint] = []

        for period, cung_name in zip(periods, cung_order):
            raw_pos, raw_neg = raws.get(cung_name, (0.0, 0.0))
            final_pos = (raw_pos + anchor_pos) / 2
            final_neg = (raw_neg + anchor_neg) / 2
            final_tb = final_pos + final_neg

            points.append(ScorePoint(
                period=str(period),
                duong=round(final_pos, 2),
                am=round(final_neg, 2),
                tb=round(final_tb, 2),
            ))

        return points

    def _summary_score(self, lifetime_points: list[ScorePoint]) -> float:
        """Weighted average of lifetime tb values using SUMMARY_AGE_WEIGHTS."""
        ages = list(range(0, 120, 10))
        if len(lifetime_points) != len(ages):
            logger.error(
                "Expected %d lifetime points, got %d", len(ages), len(lifetime_points)
            )
            return 0.0

        weighted_sum = 0.0
        weight_total = 0.0

        for point, age in zip(lifetime_points, ages):
            w = SUMMARY_AGE_WEIGHTS.get(age, 1.0)
            weighted_sum += point.tb * w
            weight_total += w

        return round(weighted_sum / weight_total, 2) if weight_total > 0 else 0.0
```

Also add import:
```python
from backend.app.constants import DIMENSIONS, HOUSE_WEIGHTS, SUMMARY_AGE_WEIGHTS
```

- [ ] **Step 4: Run tests**

Run: `cd /mnt/d/Working/TBTesu/TuViApp && python -m pytest backend/tests/test_scoring_final.py -v`
Expected: All 6 tests PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app/services/scoring.py backend/tests/test_scoring_final.py
git commit -m "feat(scoring): implement final score calculation and summary score"
```

---

### Task 6: Alert Detection

**Files:**
- Modify: `backend/app/services/scoring.py` (add `_detect_alerts`)
- Create: `backend/tests/test_scoring_alerts.py`

- [ ] **Step 1: Write failing tests for alert detection**

Create `backend/tests/test_scoring_alerts.py`:
```python
import pytest
from dataclasses import dataclass
from backend.app.services.scoring import ScoringEngine
from backend.app.models.schemas import ScorePoint, Alert

XLSX_PATH = "data/laso_points.xlsx"


@pytest.fixture(scope="module")
def engine():
    return ScoringEngine(xlsx_path=XLSX_PATH)


@dataclass
class FakeStar:
    slug: str


@dataclass
class FakeCung:
    name: str
    stars: list


def _make_points(values_duong, values_am, period_labels):
    """Helper: build ScorePoint list from parallel arrays."""
    return [
        ScorePoint(period=str(p), duong=d, am=a, tb=d + a)
        for p, d, a in zip(period_labels, values_duong, values_am)
    ]


def test_alert_50pct_positive_detected(engine):
    """A 60% jump on duong line → level 50 alert."""
    points = _make_points(
        values_duong=[10.0, 16.0],  # 60% increase
        values_am=[-5.0, -5.0],
        period_labels=["0-10", "10-20"],
    )
    # Use fake cungs with a star that has pct_fvg_50 = "pos"
    pos_fvg_stars = [
        s for s in engine._star_table.values()
        if s.pct_fvg.get(50) == "pos"
    ]
    if not pos_fvg_stars:
        pytest.skip("No stars with pct_fvg_50=pos in dataset")
    star = pos_fvg_stars[0]

    cungs = [
        FakeCung(name="0-10", stars=[]),  # source period
        FakeCung(name="10-20", stars=[FakeStar(slug=star.slug)]),  # destination
    ]

    alerts = engine._detect_alerts(points, cungs, "su_nghiep", "lifetime")
    level_50 = [a for a in alerts if a.level == 50]
    assert len(level_50) >= 1
    assert level_50[0].type == "positive"
    assert level_50[0].period == "10-20"


def test_alert_30pct_detected(engine):
    """A 35% jump → level 30 alert."""
    points = _make_points(
        values_duong=[10.0, 13.5],  # 35% increase
        values_am=[-5.0, -5.0],
        period_labels=["0-10", "10-20"],
    )
    pos_fvg_stars = [
        s for s in engine._star_table.values()
        if s.pct_fvg.get(30) == "pos"
    ]
    if not pos_fvg_stars:
        pytest.skip("No stars with pct_fvg_30=pos")
    star = pos_fvg_stars[0]

    cungs = [
        FakeCung(name="0-10", stars=[]),
        FakeCung(name="10-20", stars=[FakeStar(slug=star.slug)]),
    ]

    alerts = engine._detect_alerts(points, cungs, "su_nghiep", "lifetime")
    level_30 = [a for a in alerts if a.level == 30]
    assert len(level_30) >= 1


def test_alert_50_takes_priority_over_30(engine):
    """When pct >= 50, only level 50 alert should appear, not 30."""
    points = _make_points(
        values_duong=[10.0, 20.0],  # 100% increase
        values_am=[-5.0, -5.0],
        period_labels=["0-10", "10-20"],
    )
    pos_fvg_stars = [
        s for s in engine._star_table.values()
        if s.pct_fvg.get(50) == "pos" and s.pct_fvg.get(30) == "pos"
    ]
    if not pos_fvg_stars:
        pytest.skip("No stars with both pct_fvg levels")
    star = pos_fvg_stars[0]

    cungs = [
        FakeCung(name="0-10", stars=[]),
        FakeCung(name="10-20", stars=[FakeStar(slug=star.slug)]),
    ]

    alerts = engine._detect_alerts(points, cungs, "su_nghiep", "lifetime")
    # Should have level 50, but NOT level 30 for the same transition
    periods_50 = {a.period for a in alerts if a.level == 50 and a.star_name == star.slug}
    periods_30 = {a.period for a in alerts if a.level == 30 and a.star_name == star.slug}
    overlap = periods_50 & periods_30
    assert len(overlap) == 0, f"Same transition has both 30 and 50: {overlap}"


def test_alert_neg_line_inverted(engine):
    """Am line: going from -10 to -5 is improvement → positive pct_change."""
    points = _make_points(
        values_duong=[10.0, 10.0],
        values_am=[-10.0, -5.0],  # 50% improvement (less negative)
        period_labels=["0-10", "10-20"],
    )
    pos_fvg_stars = [
        s for s in engine._star_table.values()
        if s.pct_fvg.get(50) == "pos"
    ]
    if not pos_fvg_stars:
        pytest.skip("No stars with pct_fvg_50=pos")
    star = pos_fvg_stars[0]

    cungs = [
        FakeCung(name="0-10", stars=[]),
        FakeCung(name="10-20", stars=[FakeStar(slug=star.slug)]),
    ]

    alerts = engine._detect_alerts(points, cungs, "su_nghiep", "lifetime")
    # After inversion, this should be detected as positive change
    pos_alerts = [a for a in alerts if a.type == "positive"]
    assert len(pos_alerts) >= 1


def test_alert_zero_previous_skipped(engine):
    """If previous value is 0, skip alert detection for that transition."""
    points = _make_points(
        values_duong=[0.0, 10.0],
        values_am=[0.0, -5.0],
        period_labels=["0-10", "10-20"],
    )
    cungs = [
        FakeCung(name="0-10", stars=[]),
        FakeCung(name="10-20", stars=[]),
    ]

    alerts = engine._detect_alerts(points, cungs, "su_nghiep", "lifetime")
    assert len(alerts) == 0


def test_alert_van_menh_no_alerts(engine):
    """van_menh should never have alerts — enforced by caller, but verify here."""
    # This is a design rule: _detect_alerts should still work if called,
    # but the caller (score method) skips calling it for van_menh.
    # We test the caller behavior in integration tests.
    pass


def test_alert_lifetime_after_age_80_skipped(engine):
    """No alerts for transitions after age 80 on lifetime chart."""
    # 12 points: ages 0, 10, 20, ..., 110
    duong_values = [10.0] * 9 + [20.0, 40.0, 80.0]  # big jumps at 80, 90, 100
    am_values = [-5.0] * 12
    period_labels = [f"{age}-{age+10}" for age in range(0, 120, 10)]

    points = _make_points(duong_values, am_values, period_labels)

    # Even with big jumps, no alerts after age 80
    cungs = [FakeCung(name=p, stars=[]) for p in period_labels]
    alerts = engine._detect_alerts(points, cungs, "su_nghiep", "lifetime")

    late_alerts = [a for a in alerts if a.period in ("80-90", "90-100", "100-110")]
    assert len(late_alerts) == 0


def test_alert_con_cai_after_age_60_skipped(engine):
    """con_cai: no alerts after age 60 on lifetime chart."""
    duong_values = [10.0] * 7 + [20.0, 40.0, 80.0, 160.0, 320.0]
    am_values = [-5.0] * 12
    period_labels = [f"{age}-{age+10}" for age in range(0, 120, 10)]

    points = _make_points(duong_values, am_values, period_labels)
    cungs = [FakeCung(name=p, stars=[]) for p in period_labels]

    alerts = engine._detect_alerts(points, cungs, "con_cai", "lifetime")

    late_alerts = [a for a in alerts if a.period in (
        "60-70", "70-80", "80-90", "90-100", "100-110"
    )]
    assert len(late_alerts) == 0


def test_alert_below_30pct_no_alert(engine):
    """Changes < 30% should NOT trigger alerts."""
    points = _make_points(
        values_duong=[10.0, 12.0],  # 20% increase — below threshold
        values_am=[-5.0, -5.0],
        period_labels=["0-10", "10-20"],
    )
    cungs = [
        FakeCung(name="0-10", stars=[]),
        FakeCung(name="10-20", stars=[]),
    ]

    alerts = engine._detect_alerts(points, cungs, "su_nghiep", "lifetime")
    assert len(alerts) == 0
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /mnt/d/Working/TBTesu/TuViApp && python -m pytest backend/tests/test_scoring_alerts.py -v`
Expected: FAIL with `AttributeError`

- [ ] **Step 3: Implement `_detect_alerts`**

Add to `ScoringEngine` class in `backend/app/services/scoring.py`:

```python
    def _detect_alerts(
        self,
        points: list[ScorePoint],
        cungs: list,
        dim: str,
        timeframe: str,
    ) -> list[Alert]:
        """Detect score change alerts between consecutive periods.

        Args:
            points: ScorePoint list (ordered by period).
            cungs: Matching cung list (same order as points) — stars used for tag lookup.
            dim: Dimension key.
            timeframe: "lifetime", "decade", or "monthly".

        Returns:
            List of Alert objects.
        """
        alerts: list[Alert] = []

        # Determine age cutoff for lifetime charts
        max_age = None
        if timeframe == "lifetime":
            max_age = 60 if dim == "con_cai" else 80

        for col_attr, col_name in [("duong", "pos"), ("am", "neg")]:
            values = [getattr(p, col_attr) for p in points]

            for i in range(1, len(values)):
                prev = values[i - 1]
                curr = values[i]

                # Skip if previous is zero
                if abs(prev) < 1e-9:
                    continue

                pct_change = ((curr - prev) / abs(prev)) * 100

                # Invert for neg column
                if col_name == "neg":
                    pct_change *= -1

                # Skip after age cutoff on lifetime
                if max_age is not None and timeframe == "lifetime":
                    try:
                        age = int(points[i].period.split("-")[0])
                        if age >= max_age:
                            continue
                    except (ValueError, IndexError):
                        pass

                # Determine alert level
                abs_pct = abs(pct_change)
                if abs_pct >= 50:
                    level = 50
                elif abs_pct >= 30:
                    level = 30
                else:
                    continue

                direction = "pos" if pct_change > 0 else "neg"

                # Find matching stars in destination cung
                if i < len(cungs):
                    for star in cungs[i].stars:
                        row = self._star_table.get(star.slug)
                        if row is None:
                            continue

                        # Check pct_fvg direction match
                        if row.pct_fvg.get(level) != direction:
                            continue

                        # Get tag text
                        tag = row.alert_tags.get(dim, {}).get(level)
                        if not tag:
                            continue

                        alerts.append(Alert(
                            type="positive" if direction == "pos" else "negative",
                            dimension=dim,
                            period=points[i].period,
                            tag=tag,
                            level=level,
                            star_name=row.name,
                        ))

        return alerts
```

- [ ] **Step 4: Run tests**

Run: `cd /mnt/d/Working/TBTesu/TuViApp && python -m pytest backend/tests/test_scoring_alerts.py -v`
Expected: All 9 tests PASS (1 empty test for van_menh passes trivially)

- [ ] **Step 5: Commit**

```bash
git add backend/app/services/scoring.py backend/tests/test_scoring_alerts.py
git commit -m "feat(scoring): implement alert detection with age cutoffs and direction matching"
```

---

### Task 7: Main `score()` Method — Full Pipeline

**Files:**
- Modify: `backend/app/services/scoring.py` (add `score` method)
- Create: `backend/tests/test_scoring_integration.py`
- Create: `backend/tests/fixtures/sample_laso.json`

- [ ] **Step 1: Create test fixture**

Create `backend/tests/fixtures/sample_laso.json` — a minimal but realistic `LasoData` fixture. This uses the standard 12 cung names with 1-2 known stars each.

Create `backend/tests/fixtures/sample_laso.json`:
```json
{
  "nam": "Giáp Tuất",
  "menh": "Mộc",
  "cuc": "Thủy Nhị Cục",
  "than_cu": "Thiên Di",
  "menh_chu": "Tham Lang",
  "than_chu": "Cự Môn",
  "am_duong": "Dương Nam",
  "cung": [
    {"name": "Mệnh", "stars": [{"name": "Tử Vi", "raw_name": "Tử Vi", "variant": null, "slug": "tu-vi"}]},
    {"name": "Phụ Mẫu", "stars": [{"name": "Thiên Cơ", "raw_name": "Thiên Cơ", "variant": null, "slug": "thien-co"}]},
    {"name": "Phúc Đức", "stars": [{"name": "Thái Dương", "raw_name": "Thái Dương", "variant": null, "slug": "thai-duong"}]},
    {"name": "Điền Trạch", "stars": [{"name": "Vũ Khúc", "raw_name": "Vũ Khúc", "variant": null, "slug": "vu-khuc"}]},
    {"name": "Quan Lộc", "stars": [{"name": "Thiên Đồng", "raw_name": "Thiên Đồng", "variant": null, "slug": "thien-dong"}]},
    {"name": "Nô Bộc", "stars": [{"name": "Liêm Trinh", "raw_name": "Liêm Trinh", "variant": null, "slug": "liem-trinh"}]},
    {"name": "Thiên Di", "stars": [{"name": "Thiên Phủ", "raw_name": "Thiên Phủ", "variant": null, "slug": "thien-phu"}]},
    {"name": "Tật Ách", "stars": [{"name": "Thái Âm", "raw_name": "Thái Âm", "variant": null, "slug": "thai-am"}]},
    {"name": "Tài Bạch", "stars": [{"name": "Tham Lang", "raw_name": "Tham Lang", "variant": null, "slug": "tham-lang"}]},
    {"name": "Tử Tức", "stars": [{"name": "Cự Môn", "raw_name": "Cự Môn", "variant": null, "slug": "cu-mon"}]},
    {"name": "Phu Thê", "stars": [{"name": "Thiên Tướng", "raw_name": "Thiên Tướng", "variant": null, "slug": "thien-tuong"}]},
    {"name": "Huynh Đệ", "stars": [{"name": "Thiên Lương", "raw_name": "Thiên Lương", "variant": null, "slug": "thien-luong"}]}
  ],
  "cung_10yrs": [
    {"name": "Mệnh", "stars": [{"name": "Tử Vi", "raw_name": "Tử Vi", "variant": null, "slug": "tu-vi"}]},
    {"name": "Phụ Mẫu", "stars": [{"name": "Thiên Cơ", "raw_name": "Thiên Cơ", "variant": null, "slug": "thien-co"}]},
    {"name": "Phúc Đức", "stars": [{"name": "Thái Dương", "raw_name": "Thái Dương", "variant": null, "slug": "thai-duong"}]},
    {"name": "Điền Trạch", "stars": [{"name": "Vũ Khúc", "raw_name": "Vũ Khúc", "variant": null, "slug": "vu-khuc"}]},
    {"name": "Quan Lộc", "stars": [{"name": "Thiên Đồng", "raw_name": "Thiên Đồng", "variant": null, "slug": "thien-dong"}]},
    {"name": "Nô Bộc", "stars": [{"name": "Liêm Trinh", "raw_name": "Liêm Trinh", "variant": null, "slug": "liem-trinh"}]},
    {"name": "Thiên Di", "stars": [{"name": "Thiên Phủ", "raw_name": "Thiên Phủ", "variant": null, "slug": "thien-phu"}]},
    {"name": "Tật Ách", "stars": [{"name": "Thái Âm", "raw_name": "Thái Âm", "variant": null, "slug": "thai-am"}]},
    {"name": "Tài Bạch", "stars": [{"name": "Tham Lang", "raw_name": "Tham Lang", "variant": null, "slug": "tham-lang"}]},
    {"name": "Tử Tức", "stars": [{"name": "Cự Môn", "raw_name": "Cự Môn", "variant": null, "slug": "cu-mon"}]},
    {"name": "Phu Thê", "stars": [{"name": "Thiên Tướng", "raw_name": "Thiên Tướng", "variant": null, "slug": "thien-tuong"}]},
    {"name": "Huynh Đệ", "stars": [{"name": "Thiên Lương", "raw_name": "Thiên Lương", "variant": null, "slug": "thien-luong"}]}
  ],
  "cung_12months": [
    {"name": "Mệnh", "month": 1, "month_label": "Th.1", "stars": [{"name": "Tử Vi", "raw_name": "Tử Vi", "variant": null, "slug": "tu-vi"}]},
    {"name": "Phụ Mẫu", "month": 2, "month_label": "Th.2", "stars": [{"name": "Thiên Cơ", "raw_name": "Thiên Cơ", "variant": null, "slug": "thien-co"}]},
    {"name": "Phúc Đức", "month": 3, "month_label": "Th.3", "stars": [{"name": "Thái Dương", "raw_name": "Thái Dương", "variant": null, "slug": "thai-duong"}]},
    {"name": "Điền Trạch", "month": 4, "month_label": "Th.4", "stars": [{"name": "Vũ Khúc", "raw_name": "Vũ Khúc", "variant": null, "slug": "vu-khuc"}]},
    {"name": "Quan Lộc", "month": 5, "month_label": "Th.5", "stars": [{"name": "Thiên Đồng", "raw_name": "Thiên Đồng", "variant": null, "slug": "thien-dong"}]},
    {"name": "Nô Bộc", "month": 6, "month_label": "Th.6", "stars": [{"name": "Liêm Trinh", "raw_name": "Liêm Trinh", "variant": null, "slug": "liem-trinh"}]},
    {"name": "Thiên Di", "month": 7, "month_label": "Th.7", "stars": [{"name": "Thiên Phủ", "raw_name": "Thiên Phủ", "variant": null, "slug": "thien-phu"}]},
    {"name": "Tật Ách", "month": 8, "month_label": "Th.8", "stars": [{"name": "Thái Âm", "raw_name": "Thái Âm", "variant": null, "slug": "thai-am"}]},
    {"name": "Tài Bạch", "month": 9, "month_label": "Th.9", "stars": [{"name": "Tham Lang", "raw_name": "Tham Lang", "variant": null, "slug": "tham-lang"}]},
    {"name": "Tử Tức", "month": 10, "month_label": "Th.10", "stars": [{"name": "Cự Môn", "raw_name": "Cự Môn", "variant": null, "slug": "cu-mon"}]},
    {"name": "Phu Thê", "month": 11, "month_label": "Th.11", "stars": [{"name": "Thiên Tướng", "raw_name": "Thiên Tướng", "variant": null, "slug": "thien-tuong"}]},
    {"name": "Huynh Đệ", "month": 12, "month_label": "Th.12", "stars": [{"name": "Thiên Lương", "raw_name": "Thiên Lương", "variant": null, "slug": "thien-luong"}]}
  ]
}
```

- [ ] **Step 2: Write failing integration tests**

Create `backend/tests/test_scoring_integration.py`:
```python
import json
import pytest
from dataclasses import dataclass
from pathlib import Path
from backend.app.services.scoring import ScoringEngine
from backend.app.constants import DIMENSIONS, DIMENSION_LABELS

XLSX_PATH = "data/laso_points.xlsx"
FIXTURE_PATH = Path("backend/tests/fixtures/sample_laso.json")


@dataclass
class FixtureStar:
    name: str
    raw_name: str
    variant: str | None
    slug: str


@dataclass
class FixtureCung:
    name: str
    stars: list[FixtureStar]


@dataclass
class FixtureMonthlyCung:
    name: str
    month: int
    month_label: str
    stars: list[FixtureStar]


@dataclass
class FixtureLasoData:
    nam: str
    menh: str
    cuc: str
    than_cu: str
    menh_chu: str
    than_chu: str
    am_duong: str
    cung: list[FixtureCung]
    cung_10yrs: list[FixtureCung]
    cung_12months: list[FixtureMonthlyCung]


def _load_fixture() -> FixtureLasoData:
    data = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    return FixtureLasoData(
        nam=data["nam"],
        menh=data["menh"],
        cuc=data["cuc"],
        than_cu=data["than_cu"],
        menh_chu=data["menh_chu"],
        than_chu=data["than_chu"],
        am_duong=data["am_duong"],
        cung=[
            FixtureCung(
                name=c["name"],
                stars=[FixtureStar(**s) for s in c["stars"]],
            )
            for c in data["cung"]
        ],
        cung_10yrs=[
            FixtureCung(
                name=c["name"],
                stars=[FixtureStar(**s) for s in c["stars"]],
            )
            for c in data["cung_10yrs"]
        ],
        cung_12months=[
            FixtureMonthlyCung(
                name=c["name"],
                month=c["month"],
                month_label=c["month_label"],
                stars=[FixtureStar(**s) for s in c["stars"]],
            )
            for c in data["cung_12months"]
        ],
    )


@pytest.fixture(scope="module")
def engine():
    return ScoringEngine(xlsx_path=XLSX_PATH)


@pytest.fixture(scope="module")
def laso():
    return _load_fixture()


@pytest.fixture(scope="module")
def result(engine, laso):
    return engine.score(laso)


def test_result_has_8_dimensions(result):
    assert len(result.dimensions) == 8
    for dim in DIMENSIONS:
        assert dim in result.dimensions


def test_dimension_labels_correct(result):
    for dim_key, dim_scores in result.dimensions.items():
        assert dim_scores.label == DIMENSION_LABELS[dim_key]


def test_lifetime_has_12_points(result):
    for dim_key, dim_scores in result.dimensions.items():
        assert len(dim_scores.lifetime) == 12, f"{dim_key} lifetime has {len(dim_scores.lifetime)} points"


def test_decade_has_10_points(result):
    for dim_key, dim_scores in result.dimensions.items():
        assert len(dim_scores.decade) == 10, f"{dim_key} decade has {len(dim_scores.decade)} points"


def test_monthly_has_13_points(result):
    for dim_key, dim_scores in result.dimensions.items():
        assert len(dim_scores.monthly) == 13, f"{dim_key} monthly has {len(dim_scores.monthly)} points"


def test_monthly_first_two_periods_same(result):
    """First month is prepended → first two periods should match."""
    for dim_key, dim_scores in result.dimensions.items():
        assert dim_scores.monthly[0].period == dim_scores.monthly[1].period, (
            f"{dim_key}: monthly[0].period={dim_scores.monthly[0].period} "
            f"!= monthly[1].period={dim_scores.monthly[1].period}"
        )


def test_tb_equals_duong_plus_am(result):
    """tb must always equal duong + am (algebraic sum)."""
    for dim_key, dim_scores in result.dimensions.items():
        for chart_name in ("lifetime", "decade", "monthly"):
            for point in getattr(dim_scores, chart_name):
                expected_tb = round(point.duong + point.am, 2)
                assert abs(point.tb - expected_tb) < 0.02, (
                    f"{dim_key}.{chart_name} period {point.period}: "
                    f"tb={point.tb} != duong({point.duong}) + am({point.am}) = {expected_tb}"
                )


def test_van_menh_has_no_alerts(result):
    assert len(result.dimensions["van_menh"].alerts) == 0


def test_all_alerts_flattened(result):
    total_from_dims = sum(len(d.alerts) for d in result.dimensions.values())
    assert len(result.all_alerts) == total_from_dims


def test_all_alerts_sorted_by_level_desc(result):
    for i in range(1, len(result.all_alerts)):
        assert result.all_alerts[i - 1].level >= result.all_alerts[i].level


def test_summary_score_is_number(result):
    for dim_key, dim_scores in result.dimensions.items():
        assert isinstance(dim_scores.summary_score, float)


def test_lifetime_periods_are_age_ranges(result):
    expected = [f"{a}-{a+10}" for a in range(0, 120, 10)]
    for dim_key, dim_scores in result.dimensions.items():
        actual = [p.period for p in dim_scores.lifetime]
        assert actual == expected, f"{dim_key} lifetime periods: {actual}"


def test_decade_periods_are_years(result):
    dim_scores = result.dimensions["su_nghiep"]
    periods = [p.period for p in dim_scores.decade]
    # Should be consecutive years
    for p in periods:
        assert p.isdigit(), f"Decade period '{p}' is not a year"
    years = [int(p) for p in periods]
    assert years == list(range(years[0], years[0] + 10))
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `cd /mnt/d/Working/TBTesu/TuViApp && python -m pytest backend/tests/test_scoring_integration.py -v`
Expected: FAIL with `AttributeError: 'ScoringEngine' object has no attribute 'score'`

- [ ] **Step 4: Implement `score()` method**

Add to `ScoringEngine` class in `backend/app/services/scoring.py`:

```python
    def score(self, laso, nam_xem: int = 2026) -> ScoringResult:
        """Main entry point: LasoData → ScoringResult.

        Args:
            laso: LasoData (or compatible object with cung, cung_10yrs, cung_12months, than_cu).
            nam_xem: Year being analyzed (for decade/monthly x-axis labels).

        Returns:
            ScoringResult with 8 dimensions scored.
        """
        # Validate input
        if len(laso.cung) != 12:
            raise ScoringError(f"Expected 12 lifetime cungs, got {len(laso.cung)}")
        if len(laso.cung_12months) < 12:
            raise ScoringError(f"Expected 12 monthly cungs, got {len(laso.cung_12months)}")

        than_cu = laso.than_cu

        dimensions: dict[str, DimensionScores] = {}
        all_alerts: list[Alert] = []

        for dim in DIMENSIONS:
            # Step 1: Build raw scores for all 3 timeframes
            lifetime_raws = self._build_raw_scores(laso.cung, dim)
            decade_raws = self._build_raw_scores(laso.cung_10yrs, dim)
            monthly_raws = self._build_raw_scores(laso.cung_12months, dim)

            # Step 2: Anchor from LIFETIME data only
            anchor = self._calc_anchor(lifetime_raws, dim, than_cu)

            # Step 3: Final scores — Lifetime (12 points)
            lifetime_cung_order = [c.name.lower() for c in laso.cung]
            lifetime_periods = [f"{a}-{a+10}" for a in range(0, 120, 10)]
            lifetime_points = self._calc_final(
                lifetime_raws, anchor, lifetime_periods, lifetime_cung_order
            )

            # Step 3: Final scores — Decade (first 10 of 12 cungs)
            decade_cungs = laso.cung_10yrs[:-2]
            decade_cung_order = [c.name.lower() for c in decade_cungs]
            decade_periods = [str(y) for y in range(nam_xem, nam_xem + 10)]
            decade_points = self._calc_final(
                decade_raws, anchor, decade_periods, decade_cung_order
            )

            # Step 3: Final scores — Monthly (13 points, first prepended)
            monthly_cung_order = [laso.cung_12months[0].name.lower()]
            monthly_cung_order += [mc.name.lower() for mc in laso.cung_12months]
            monthly_periods = [f"Th.{laso.cung_12months[0].month}/{nam_xem}"]
            monthly_periods += [
                f"Th.{mc.month}/{nam_xem}" for mc in laso.cung_12months
            ]
            monthly_points = self._calc_final(
                monthly_raws, anchor, monthly_periods, monthly_cung_order
            )

            # Step 4: Alerts (skip for van_menh)
            alerts: list[Alert] = []
            if dim != "van_menh":
                # Lifetime alerts
                lifetime_alert_cungs = list(laso.cung)
                alerts.extend(
                    self._detect_alerts(lifetime_points, lifetime_alert_cungs, dim, "lifetime")
                )
                # Decade alerts
                alerts.extend(
                    self._detect_alerts(decade_points, list(decade_cungs), dim, "decade")
                )
                # Monthly alerts
                monthly_alert_cungs = [laso.cung_12months[0]] + list(laso.cung_12months)
                alerts.extend(
                    self._detect_alerts(monthly_points, monthly_alert_cungs, dim, "monthly")
                )

            # Step 5: Summary score
            summary = self._summary_score(lifetime_points)

            dimensions[dim] = DimensionScores(
                dimension=dim,
                label=DIMENSION_LABELS[dim],
                lifetime=lifetime_points,
                decade=decade_points,
                monthly=monthly_points,
                alerts=alerts,
                summary_score=summary,
            )
            all_alerts.extend(alerts)

        # Sort all_alerts: level desc, then by dimension order
        dim_order = {d: i for i, d in enumerate(DIMENSIONS)}
        all_alerts.sort(key=lambda a: (-a.level, dim_order.get(a.dimension, 99)))

        return ScoringResult(dimensions=dimensions, all_alerts=all_alerts)
```

Also add the `ScoringError` exception class near the top of `scoring.py`:

```python
class ScoringError(Exception):
    """Raised when scoring input data is invalid."""
    pass
```

And add the `DIMENSION_LABELS` import:
```python
from backend.app.constants import DIMENSIONS, HOUSE_WEIGHTS, SUMMARY_AGE_WEIGHTS, DIMENSION_LABELS
```

- [ ] **Step 5: Run tests**

Run: `cd /mnt/d/Working/TBTesu/TuViApp && python -m pytest backend/tests/test_scoring_integration.py -v`
Expected: All 13 tests PASS

- [ ] **Step 6: Run all scoring tests together**

Run: `cd /mnt/d/Working/TBTesu/TuViApp && python -m pytest backend/tests/ -v`
Expected: All tests PASS across all test files

- [ ] **Step 7: Commit**

```bash
git add backend/app/services/scoring.py backend/tests/test_scoring_integration.py backend/tests/fixtures/sample_laso.json
git commit -m "feat(scoring): implement full scoring pipeline with integration tests"
```

---

### Task 8: Summary Score Tests

**Files:**
- Create: `backend/tests/test_scoring_summary.py`

- [ ] **Step 1: Write dedicated summary score tests**

Create `backend/tests/test_scoring_summary.py`:
```python
import pytest
from backend.app.services.scoring import ScoringEngine
from backend.app.models.schemas import ScorePoint
from backend.app.constants import SUMMARY_AGE_WEIGHTS

XLSX_PATH = "data/laso_points.xlsx"


@pytest.fixture(scope="module")
def engine():
    return ScoringEngine(xlsx_path=XLSX_PATH)


def _make_lifetime(tb_values):
    """Build 12-point lifetime list from tb values."""
    ages = list(range(0, 120, 10))
    return [
        ScorePoint(period=f"{a}-{a+10}", duong=max(tb, 0), am=min(tb, 0), tb=tb)
        for a, tb in zip(ages, tb_values)
    ]


def test_uniform_tb_returns_same_value(engine):
    points = _make_lifetime([7.0] * 12)
    assert abs(engine._summary_score(points) - 7.0) < 0.01


def test_prime_years_dominate(engine):
    """If prime years (20-60) are 100 and rest are 0, summary > 50."""
    tb_values = [0, 0, 100, 100, 100, 100, 100, 0, 0, 0, 0, 0]
    summary = engine._summary_score(_make_lifetime(tb_values))
    # Weighted: 5 * 1.5 * 100 = 750, total weight = 5*0.5 + 5*1.5 + 2*1.0 = 12
    # Wait, let me compute exactly:
    # ages 0,10 → 0.5 each = 0
    # ages 20-60 → 1.5 each = 5 * 1.5 * 100 = 750
    # ages 70-90 → 1.0 each = 0
    # ages 100,110 → 0.5 each = 0
    # total weight = 2*0.5 + 5*1.5 + 3*1.0 + 2*0.5 = 1 + 7.5 + 3 + 1 = 12.5
    # summary = 750 / 12.5 = 60.0
    assert abs(summary - 60.0) < 0.01


def test_negative_tb_values(engine):
    points = _make_lifetime([-3.0] * 12)
    assert abs(engine._summary_score(points) - (-3.0)) < 0.01


def test_mixed_positive_negative(engine):
    """Verify weighted average handles mixed values."""
    # All prime = +10, all non-prime = -10
    tb_values = [-10, -10, 10, 10, 10, 10, 10, -10, -10, -10, -10, -10]
    summary = engine._summary_score(_make_lifetime(tb_values))

    # Manual: prime contribution = 5 * 1.5 * 10 = 75
    # non-prime: (2*0.5 + 3*1.0 + 2*0.5) * (-10) = 5 * (-10) = -50
    # total_weight = 12.5
    # summary = (75 - 50) / 12.5 = 2.0
    assert abs(summary - 2.0) < 0.01
```

- [ ] **Step 2: Run tests**

Run: `cd /mnt/d/Working/TBTesu/TuViApp && python -m pytest backend/tests/test_scoring_summary.py -v`
Expected: All 4 tests PASS

- [ ] **Step 3: Commit**

```bash
git add backend/tests/test_scoring_summary.py
git commit -m "test(scoring): add dedicated summary score tests"
```

---

### Task 9: Edge Cases + Error Handling

**Files:**
- Modify: `backend/tests/test_scoring_integration.py` (add edge case tests)

- [ ] **Step 1: Add edge case tests**

Append to `backend/tests/test_scoring_integration.py`:

```python
def test_scoring_error_on_insufficient_cungs(engine):
    """Raise ScoringError if fewer than 12 lifetime cungs."""
    from backend.app.services.scoring import ScoringError

    bad_laso = FixtureLasoData(
        nam="Test", menh="Mộc", cuc="Test", than_cu="Mệnh",
        menh_chu="Test", than_chu="Test", am_duong="Test",
        cung=[FixtureCung(name="Mệnh", stars=[])],  # only 1
        cung_10yrs=[FixtureCung(name=f"C{i}", stars=[]) for i in range(12)],
        cung_12months=[
            FixtureMonthlyCung(name=f"C{i}", month=i+1, month_label=f"Th.{i+1}", stars=[])
            for i in range(12)
        ],
    )
    with pytest.raises(ScoringError, match="12 lifetime"):
        engine.score(bad_laso)


def test_scoring_error_on_insufficient_months(engine):
    """Raise ScoringError if fewer than 12 monthly cungs."""
    from backend.app.services.scoring import ScoringError

    bad_laso = FixtureLasoData(
        nam="Test", menh="Mộc", cuc="Test", than_cu="Mệnh",
        menh_chu="Test", than_chu="Test", am_duong="Test",
        cung=[FixtureCung(name=f"C{i}", stars=[]) for i in range(12)],
        cung_10yrs=[FixtureCung(name=f"C{i}", stars=[]) for i in range(12)],
        cung_12months=[
            FixtureMonthlyCung(name="C0", month=1, month_label="Th.1", stars=[])
        ],  # only 1
    )
    with pytest.raises(ScoringError, match="12 monthly"):
        engine.score(bad_laso)


def test_scoring_with_empty_stars_produces_zero_scores(engine):
    """All cungs with no stars → all scores should be 0."""
    empty_laso = FixtureLasoData(
        nam="Test", menh="Mộc", cuc="Test", than_cu="Mệnh",
        menh_chu="Test", than_chu="Test", am_duong="Test",
        cung=[FixtureCung(name=f"C{i}", stars=[]) for i in range(12)],
        cung_10yrs=[FixtureCung(name=f"C{i}", stars=[]) for i in range(12)],
        cung_12months=[
            FixtureMonthlyCung(name=f"C{i}", month=i+1, month_label=f"Th.{i+1}", stars=[])
            for i in range(12)
        ],
    )
    result = engine.score(empty_laso)

    for dim_key, dim_scores in result.dimensions.items():
        for point in dim_scores.lifetime:
            assert point.duong == 0.0
            assert point.am == 0.0
            assert point.tb == 0.0


def test_scoring_performance(engine, laso):
    """Scoring must complete in < 200ms."""
    import time
    start = time.perf_counter()
    for _ in range(10):
        engine.score(laso)
    elapsed = (time.perf_counter() - start) / 10
    assert elapsed < 0.2, f"Scoring took {elapsed:.3f}s, expected < 0.2s"
```

- [ ] **Step 2: Run all tests**

Run: `cd /mnt/d/Working/TBTesu/TuViApp && python -m pytest backend/tests/ -v`
Expected: All tests PASS

- [ ] **Step 3: Commit**

```bash
git add backend/tests/test_scoring_integration.py
git commit -m "test(scoring): add edge cases, error handling, and performance test"
```

---

### Task 10: Update Task Doc + Final Verification

**Files:**
- Modify: `docs/tasks/02_scoring.md` (update plan file reference, resolve unknowns)

- [ ] **Step 1: Run full test suite one more time**

Run: `cd /mnt/d/Working/TBTesu/TuViApp && python -m pytest backend/tests/ -v --tb=short`
Expected: All tests PASS

- [ ] **Step 2: Update task doc with resolved unknowns**

In `docs/tasks/02_scoring.md`, update the REMAINING UNKNOWNS section and the HOUSE_WEIGHTS for hoc_tap and con_cai:

Replace the `hoc_tap` entry:
```python
    'hoc_tap': [("mệnh", 0.5), ("quan lộc", 0.2), ("thiên di", 0.3)],
```

Replace the `con_cai` entry:
```python
    'con_cai': [("tử tức", 0.5), ("điền trạch", 0.1), ("phúc đức", 0.4)],
```

Update the plan file reference line:
```
**Plan file** `docs/superpowers/plans/2026-03-27-scoring-engine-implementation.md`
```

Mark REMAINING UNKNOWNS as resolved:
```markdown
## REMAINING UNKNOWNS — ALL RESOLVED

| # | What | Resolution |
|---|------|------------|
| 1 | hoc_tap anchor cungs | ✅ ("mệnh", 0.5), ("quan lộc", 0.2), ("thiên di", 0.3) |
| 2 | con_cai anchor cungs | ✅ ("tử tức", 0.5), ("điền trạch", 0.1), ("phúc đức", 0.4) |
| 3 | "thân" cung mapping | ✅ Dynamic: `laso.than_cu` resolves at runtime |
| 4 | Cung name for "nô bộc" | ✅ Use "nô bộc" (scraper strips to this form) |
```

- [ ] **Step 3: Commit**

```bash
git add docs/tasks/02_scoring.md
git commit -m "docs: update scoring task with resolved unknowns and plan reference"
```
