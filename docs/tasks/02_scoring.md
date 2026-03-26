# Task 02: Scoring Engine
## Lá Số Data → Scores + Alerts per Dimension

**Priority:** Must — blocks AI pipeline
**Estimated effort:** 2-3 days
**Dependencies:** Task 01 (LasoData output), Google Sheet export (laso_points)
**Output:** Python module `services/scoring.py`

---

## What to Build

Port the existing Google Sheet scoring logic to Python:
1. Load lookup table (`laso_points.csv`) — maps stars to dimension scores
2. Given a LasoData, calculate scores per dimension per time period
3. Detect alert triggers (🔺🔻)
4. Return structured scoring result

---

## Input

- `LasoData` from Task 01 (12 cung × sao list)
- `laso_points.csv` — exported from Google Sheet (pre-existing, validated by expert)

### laso_points.csv Structure (expected)

```csv
star_name,cung,dimension,time_period,duong,am,tb,alert_tag,alert_type
Thiên Đồng,Mệnh,su_nghiep,lifetime_20-30,8,0,3,,
Thiên Đồng,Mệnh,su_nghiep,lifetime_30-40,12,-2,5,,
Tả Phù,Quan Lộc,su_nghiep,decade_2025,5,0,2,"có bước thăng tiến",positive
...
```

**NOTE:** The actual CSV structure may differ. Before coding, export the Sheet and analyze its structure. Adapt the parsing accordingly.

---

## Output

```python
@dataclass
class Alert:
    type: str               # "positive" or "negative"
    dimension: str          # "su_nghiep", "tien_bac", etc.
    period: str             # "2025", "30-40", "2026-03"
    tag: str                # alert text, e.g., "có bước thăng tiến"

@dataclass
class ScorePoint:
    period: str             # "10-20", "2025", "2026-01"
    duong: float
    am: float
    tb: float

@dataclass
class DimensionScores:
    dimension: str          # "su_nghiep"
    label: str              # "Sự nghiệp"
    lifetime: list[ScorePoint]   # mốc 10 năm
    decade: list[ScorePoint]     # mốc từng năm (current decade)
    monthly: list[ScorePoint]    # mốc từng tháng (current year)
    alerts: list[Alert]
    summary_score: float         # aggregate score for overview

@dataclass
class ScoringResult:
    dimensions: dict[str, DimensionScores]   # 7 dimensions
    all_alerts: list[Alert]                   # all alerts across dimensions
```

---

## Dimensions

| Key | Label | Related Cung (primary) |
|-----|-------|----------------------|
| `su_nghiep` | Sự nghiệp | Quan Lộc |
| `tien_bac` | Tiền bạc | Tài Bạch |
| `hon_nhan` | Hôn nhân | Phu Thê |
| `suc_khoe` | Sức khỏe | Tật Ách |
| `dat_dai` | Đất đai | Điền Trạch |
| `hoc_tap` | Học tập | (varies) |
| `con_cai` | Con cái | Tử Tức |

**NOTE:** Verify with expert which cung maps to which dimension. The mapping above is conventional but may differ in the scoring sheet.

---

## Implementation Steps

1. **Export & analyze Google Sheet:**
   - Export `laso_points` sheet as CSV
   - Understand columns: which star × which cung × which dimension × which time period → scores
   - Document any formulas or conditional logic in the Sheet

2. **Load lookup table:**
   ```python
   def load_scoring_table(csv_path: str) -> dict:
       # Parse CSV into efficient lookup structure
       # Key: (star_name, cung_name, dimension, time_period) → (duong, am, tb, alert_tag)
   ```

3. **Calculate scores:**
   ```python
   def calculate_scores(laso: LasoData, birth_year: int) -> ScoringResult:
       # For each dimension:
       #   For each time horizon (lifetime, decade, monthly):
       #     For each time period:
       #       Sum scores from all relevant stars in relevant cungs
       #       Check alert triggers
   ```

4. **Determine current decade:**
   - Based on user's birth year and current year (2026)
   - Calculate which decade to show (e.g., if born 1968, current age ~58, decade = 2020-2029)

5. **Calculate summary score:**
   - Aggregate lifetime scores into a single number per dimension
   - Used for the overview cards on result page

---

## Validation Strategy

**CRITICAL:** The scoring engine MUST match the Google Sheet output exactly.

1. Pick 5 test profiles (same as Task 01)
2. For each: manually run through Google Sheet → record expected output
3. Run through Python scoring engine → compare
4. Discrepancies must be resolved before proceeding

```python
def test_scoring_matches_sheet():
    # Load fixture: test_case_1.json (contains LasoData + expected scores)
    laso = load_fixture("test_case_1_laso.json")
    expected = load_fixture("test_case_1_expected_scores.json")
    result = calculate_scores(laso, birth_year=1968)
    
    for dim in expected.dimensions:
        assert result.dimensions[dim].lifetime == expected.dimensions[dim].lifetime
        assert result.dimensions[dim].alerts == expected.dimensions[dim].alerts
```

---

## Acceptance Criteria

- [ ] Loads `laso_points.csv` and parses all rows correctly
- [ ] Calculates scores for all 7 dimensions × 3 time horizons
- [ ] Alert triggers match Google Sheet output for all test cases
- [ ] Summary score per dimension is calculated
- [ ] Output matches Google Sheet for ≥ 5 test profiles (exact or within ±1 rounding)
- [ ] Handles edge case: star in lá số not found in lookup table → log warning, skip (don't crash)
- [ ] Performance: scoring for 1 profile < 100ms

---

## Edge Cases

- Star name mismatch between scraper output and CSV (encoding, spacing, variant names)
- Time period calculation for very young (born 2010) or very old (born 1920) people
- Missing data: some time periods may not have scores (e.g., monthly scores not defined for all stars)
- Duplicate stars in same cung (if possible in Tử Vi) → sum their scores, don't double-count alerts