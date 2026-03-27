# Scoring Engine Design Spec

**Date:** 2026-03-27
**Task:** `docs/tasks/02_scoring.md`
**Status:** Approved

---

## Overview

The Scoring Engine receives `LasoData` (scraper output: 12 lifetime cungs, 12 decade cungs, 12 monthly cungs with star placements) and produces `ScoringResult` — scored data for 8 dimensions across 3 timeframes with alert detection.

**Architecture:** Single `ScoringEngine` class (Approach A). Load `laso_points.xlsx` once at init, then pure computation per request. Stateless after init, thread-safe.

---

## 1. Data Structures

### 1.1 Input: `LasoData` (from Task 01 — no changes)

Consumed as-is from scraper output. Key fields used by scoring:
- `cung: list[Cung]` — 12 lifetime cungs with stars
- `cung_10yrs: list[Cung]` — 12 decade cungs (use first 10)
- `cung_12months: list[MonthlyCung]` — 12 monthly cungs
- `than_cu: str` — which cung "Thân" resides in (for dynamic anchor resolution)

### 1.2 Star Table (loaded from xlsx)

```python
@dataclass
class StarRow:
    slug: str                                    # slugify(sao.lower())
    name: str                                    # original sao name from xlsx
    point: int                                   # base point (-5 to +10)
    weights: dict[str, float]                    # dimension → weight (default 1.0 if NaN)
    alert_tags: dict[str, dict[int, str | None]] # dimension → {30: tag_text, 50: tag_text}
    pct_fvg: dict[int, str | None]               # {30: "pos"/"neg"/None, 50: "pos"/"neg"/None}
```

**Loading rules:**
- Read sheet `laso_points` from `data/laso_points.xlsx` via `openpyxl`
- Build slug: `slugify(row["sao"].lower())`
- For each dimension weight column: if NaN/empty → store `1.0`
- For `pct_fvg_30` / `pct_fvg_50`: store as `"pos"`, `"neg"`, or `None`
- For `{dim}_tag_30` / `{dim}_tag_50`: store alert text strings
- Deduplicate: if duplicate slug encountered, log warning, keep first

### 1.3 Output Structures

```python
@dataclass
class ScorePoint:
    period: str       # "0-10", "2026", "Th.1/2026"
    duong: float      # final_pos (positive energy)
    am: float         # final_neg (negative value)
    tb: float         # duong + am (algebraic sum)

@dataclass
class Alert:
    type: str         # "positive" | "negative"
    dimension: str    # "su_nghiep", "tien_bac", etc.
    period: str       # "20-30", "2027", "Th.5/2026"
    tag: str          # Vietnamese alert text from xlsx
    level: int        # 30 | 50
    star_name: str    # which star triggered the alert

@dataclass
class DimensionScores:
    dimension: str                    # "van_menh", "su_nghiep", etc.
    label: str                        # Vietnamese display name
    lifetime: list[ScorePoint]        # 12 points
    decade: list[ScorePoint]          # 10 points
    monthly: list[ScorePoint]         # 13 points (first month prepended)
    alerts: list[Alert]               # alerts for this dimension
    summary_score: float              # weighted average of lifetime tb

@dataclass
class ScoringResult:
    dimensions: dict[str, DimensionScores]  # 8 keys
    all_alerts: list[Alert]                 # flattened, sorted by level desc (50 first)
```

---

## 2. Constants

### 2.1 House Weights (Anchor Config)

```python
HOUSE_WEIGHTS: dict[str, list[tuple[str, float]]] = {
    "van_menh":  [("mệnh", 0.4), ("thân", 0.2), ("quan lộc", 0.2), ("tài bạch", 0.2)],
    "su_nghiep": [("quan lộc", 0.4), ("mệnh", 0.2), ("tài bạch", 0.2), ("thiên di", 0.2)],
    "tien_bac":  [("tài bạch", 0.4), ("mệnh", 0.2), ("quan lộc", 0.2), ("điền trạch", 0.2)],
    "hon_nhan":  [("phu thê", 0.4), ("mệnh", 0.2), ("phúc đức", 0.2), ("nô bộc", 0.2)],
    "suc_khoe":  [("tật ách", 0.6), ("phúc đức", 0.4)],
    "dat_dai":   [("tật ách", 0.6), ("phúc đức", 0.4)],
    "hoc_tap":   [("mệnh", 0.5), ("quan lộc", 0.2), ("thiên di", 0.3)],
    "con_cai":   [("tử tức", 0.5), ("điền trạch", 0.1), ("phúc đức", 0.4)],
}
```

**Note:** `"thân"` in `van_menh` is a dynamic reference — resolved at runtime to the cung name from `laso.than_cu`.

**Confirmed decisions:**
- `dat_dai` shares anchors with `suc_khoe` (intentional, per original logic)
- `hoc_tap` anchors: from `export_report.py` → `("mệnh", 0.5), ("quan lộc", 0.2), ("thiên di", 0.3)`
- `con_cai` anchors: from `export_report.py` → `("tử tức", 0.5), ("điền trạch", 0.1), ("phúc đức", 0.4)`

### 2.2 Summary Score Age Weights

3-tier system for weighted average of lifetime `tb` values:

```python
SUMMARY_AGE_WEIGHTS: dict[int, float] = {
    0: 0.5, 10: 0.5,                              # childhood / infancy
    20: 1.5, 30: 1.5, 40: 1.5, 50: 1.5, 60: 1.5,  # prime years
    70: 1.0, 80: 1.0, 90: 1.0,                     # normal
    100: 0.5, 110: 0.5,                             # very old
}
```

### 2.3 Dimension Labels

```python
DIMENSION_LABELS: dict[str, str] = {
    "van_menh":  "Vận Mệnh",
    "su_nghiep": "Sự Nghiệp",
    "tien_bac":  "Tiền Bạc",
    "hon_nhan":  "Hôn Nhân",
    "suc_khoe":  "Sức Khỏe",
    "dat_dai":   "Đất Đai",
    "hoc_tap":   "Học Tập",
    "con_cai":   "Con Cái",
}
```

---

## 3. Scoring Formula

### 3.1 Raw Scores (per Cung x Dimension)

For each cung in a chart, iterate its stars and accumulate:

```
for star in cung.stars:
    row = star_table.get(star.slug)
    if row is None:
        log warning, skip
        continue
    weight = row.weights[dimension]   # already defaulted to 1.0 if NaN
    if row.point > 0:
        raw_pos += row.point * weight
    else:
        raw_neg += row.point * weight
```

**Star matching:** Both sides use `slugify(name.lower())`. The star's `slug` field (from scraper) must match the xlsx star table slug.

**Unmatched stars:** Log warning with star name + cung name, skip. Do not fail.

### 3.2 Anchor (House Weighting)

Calculated **once per dimension** from **lifetime** cung data only. Reused for all 3 timeframes.

```
anchor_pos = 0.0
anchor_neg = 0.0
for (cung_name, house_weight) in HOUSE_WEIGHTS[dimension]:
    resolved_name = laso.than_cu if cung_name == "thân" else cung_name
    anchor_pos += lifetime_raw_pos[resolved_name] * house_weight
    anchor_neg += lifetime_raw_neg[resolved_name] * house_weight
```

### 3.3 Final Scores

Per cung, per timeframe:

```
final_pos = (raw_pos + anchor_pos) / 2
final_neg = (raw_neg + anchor_neg) / 2
final_tb  = final_pos + final_neg      # algebraic sum, NOT average
```

### 3.4 Chart Data Points

| Chart | Source | Count | X-axis labels |
|-------|--------|-------|---------------|
| Lifetime | `laso.cung` (all 12) | 12 | "0-10", "10-20", ..., "100-110" |
| Decade | `laso.cung_10yrs[:-2]` | 10 | "2026", "2027", ..., "2035" |
| Monthly | `laso.cung_12months` | 13 | Prepend first month, then Th.1..Th.12 |

**Monthly prepend:** The first monthly cung is duplicated at index 0, creating a 13-point chart: `[month1, month1, month2, ..., month12]`.

### 3.5 Summary Score

Weighted average of lifetime `tb` values using `SUMMARY_AGE_WEIGHTS`:

```
summary = sum(tb[i] * SUMMARY_AGE_WEIGHTS[age[i]] for i in range(12))
         / sum(SUMMARY_AGE_WEIGHTS[age[i]] for i in range(12))
```

Ages map to: 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110.

---

## 4. Alert Detection

### 4.1 Percentage Change

Between consecutive periods `i-1` and `i`:

```
if |value[i-1]| == 0:
    skip (no alert for this transition)

pct_change = (value[i] - value[i-1]) / |value[i-1]| * 100
```

For the **Âm line**, invert: `pct_change *= -1` (so "less negative = improvement" reads as positive).

### 4.2 Thresholds

- `|pct_change| >= 50%` → Level 50 alert (high priority)
- `|pct_change| >= 30%` and `< 50%` → Level 30 alert
- Same transition cannot produce both levels — 50 takes priority

### 4.3 Star Tag Lookup

- Positive change ≥ threshold → match stars in destination cung with `pct_fvg = "pos"` at that level
- Negative change ≤ -threshold → match stars with `pct_fvg = "neg"`
- Alert `tag` text from `{dimension}_tag_{level}` column
- Only stars present in the **destination cung** (period `i`) can trigger alerts

### 4.4 Special Rules

| Rule | Detail |
|------|--------|
| **van_menh** | NO alerts — skip entirely |
| **Lifetime after age 80** | No alerts for transitions 80→90, 90→100, 100→110 |
| **con_cai after age 60** | No alerts on lifetime chart after age 60 |
| **Both lines** | Alerts detected independently on Duong and Am lines |
| **Level priority** | Level 50 supersedes Level 30 for same transition |

### 4.5 Alert Sorting

`ScoringResult.all_alerts` is the flattened list from all dimensions, sorted:
1. Level descending (50 first)
2. Within same level, by dimension order (van_menh..con_cai)

---

## 5. Class API

```python
class ScoringEngine:
    """Stateless scoring calculator. Load xlsx once, reuse across requests."""

    def __init__(self, xlsx_path: str = "data/laso_points.xlsx"):
        self._star_table: dict[str, StarRow] = self._load_star_table(xlsx_path)

    def score(self, laso: LasoData) -> ScoringResult:
        """Main entry point. Pure computation, no I/O after init."""
        ...

    # --- Private methods ---
    def _load_star_table(self, path: str) -> dict[str, StarRow]: ...
    def _build_raw_scores(self, cungs: list[Cung], dim: str) -> dict[str, tuple[float, float]]: ...
    def _calc_anchor(self, lifetime_raws: dict, dim: str, than_cu: str) -> tuple[float, float]: ...
    def _calc_final(self, raws: dict, anchor: tuple, periods: list[str]) -> list[ScorePoint]: ...
    def _detect_alerts(self, points: list[ScorePoint], cungs: list, dim: str) -> list[Alert]: ...
    def _summary_score(self, lifetime_points: list[ScorePoint]) -> float: ...
```

### Integration

- FastAPI instantiates `ScoringEngine` once at startup (lifespan event)
- Router calls `engine.score(laso_data)` per request
- Thread-safe: no shared mutable state after init

---

## 6. File Structure

```
backend/
├── app/
│   ├── services/
│   │   └── scoring.py          # ScoringEngine class (~400 lines)
│   ├── models/
│   │   └── schemas.py          # All dataclasses (shared with scraper)
│   └── constants.py            # HOUSE_WEIGHTS, SUMMARY_AGE_WEIGHTS, DIMENSION_LABELS
├── data/
│   └── laso_points.xlsx        # Star reference data
└── tests/
    ├── test_scoring.py         # Unit tests
    └── fixtures/
        └── sample_laso.json    # Test fixture with known LasoData
```

### Dependencies

- `openpyxl` — xlsx reading
- `python-slugify` — star name matching
- No other external dependencies

---

## 7. Edge Cases & Error Handling

| Case | Behavior |
|------|----------|
| Star in cung not found in xlsx | Log warning, skip star |
| Cung name not found in house weights | Log error, use raw score only (anchor contribution = 0) |
| `value[i-1] == 0` in alert detection | Skip alert for that transition |
| Duplicate star slug in xlsx | Keep first occurrence, log warning |
| `van_menh` weight column all NaN | All stars use weight 1.0 (correct by design) |
| Fewer than 12 cungs in lifetime | Raise `ScoringError` — data integrity issue |
| Monthly chart < 12 months | Raise `ScoringError` — data integrity issue |
