# Task 02: Scoring Engine
## Lá Số Data → Scores + Alerts per Dimension

**Priority:** Must — blocks AI pipeline
**Estimated effort:** 3-4 days
**Dependencies:** Task 01 (LasoData), `laso_points.xlsx`
**Output:** `services/scoring.py`

---

## SCORING FORMULA (Confirmed from Codebase)

### Step 1: Raw Score per Cung

For each cung, for each star in that cung:

```
raw_pos(cung, dim) = Σ { point[i] × weight[i][dim] }  for stars where point > 0
raw_neg(cung, dim) = Σ { point[i] × weight[i][dim] }  for stars where point ≤ 0
raw_sum(cung, dim) = raw_pos + raw_neg
```

Where:
- `point[i]` = `point` column from laso_points (-5 to +10)
- `weight[i][dim]` = dimension column (e.g., `su_nghiep`) from laso_points
- If weight is NaN/empty → use `1` as default multiplier (NOT skip)
- Star matching: `slugify(star_name.lower())` must match `sao_index` in laso_points

### Step 2: House Weighting (Anchor)

Each dimension has **anchor cungs** with weights. The anchor is a **constant** calculated once from the lifetime chart, then applied to ALL time horizons.

```
anchor_pos(dim) = Σ { raw_pos(anchor_cung[j]) × anchor_weight[j] }
anchor_neg(dim) = Σ { raw_neg(anchor_cung[j]) × anchor_weight[j] }
```

### Step 3: Final Score

```
final_pos(cung) = (raw_pos(cung) + anchor_pos) / 2
final_neg(cung) = (raw_neg(cung) + anchor_neg) / 2
final_sum(cung) = final_pos + final_neg
```

### Chart Lines
- **Dương** = `final_pos` (positive energy line)
- **Âm** = `final_neg` (negative energy line — values are negative)
- **Trung bình (TB)** = `final_sum` = `final_pos + final_neg` (NOT average — algebraic sum)

---

## HOUSE WEIGHTING TABLE (from existing code)

Each dimension function has specific anchor cungs and weights:

### van_menh (Vận Mệnh)
```python
anchor_pos = (
    raw_pos("mệnh") * 0.4
    + raw_pos("thân") * 0.2      # thân = than_cu cung
    + raw_pos("quan lộc") * 0.2
    + raw_pos("tài bạch") * 0.2
)
# anchor_neg: same cungs, same weights, neg values
```

### su_nghiep (Sự Nghiệp)
```python
anchor_pos = (
    raw_pos("quan lộc") * 0.4
    + raw_pos("mệnh") * 0.2
    + raw_pos("tài bạch") * 0.2
    + raw_pos("thiên di") * 0.2
)
```

### tien_bac (Tiền Bạc)
```python
anchor_pos = (
    raw_pos("tài bạch") * 0.4
    + raw_pos("mệnh") * 0.2
    + raw_pos("quan lộc") * 0.2
    + raw_pos("điền trạch") * 0.2
)
```

### hon_nhan (Hôn Nhân)
```python
anchor_pos = (
    raw_pos("phu thê") * 0.4
    + raw_pos("mệnh") * 0.2
    + raw_pos("phúc đức") * 0.2
    + raw_pos("nô bộc") * 0.2       # hoặc "giao hữu"
)
```

### suc_khoe (Sức Khỏe)
```python
anchor_pos = (
    raw_pos("tật ách") * 0.6
    + raw_pos("phúc đức") * 0.4
)
```

### dat_dai (Đất Đai)
```python
anchor_pos = (
    raw_pos("tật ách") * 0.6        # NOTE: same as suc_khoe
    + raw_pos("phúc đức") * 0.4     # Intentional copy from suc_khoe
)
```

### hoc_tap (Học Tập)
```python
# NEED TO VERIFY — extract from existing code's hoc_tap_all() function
# Likely:
anchor_pos = (
    raw_pos("relevant_cung_1") * weight_1
    + raw_pos("relevant_cung_2") * weight_2
)
```
⚠️ **ACTION:** Check `hoc_tap_all()` in export_report.py for exact anchor cungs.

### con_cai (Con Cái)
```python
# NEED TO VERIFY — extract from existing code's con_cai_all() function
anchor_pos = (
    raw_pos("tử tức") * weight_1
    + raw_pos("relevant_cung") * weight_2
)
```
⚠️ **ACTION:** Check `con_cai_all()` in export_report.py for exact anchor cungs.

---

## ALERT SYSTEM (Confirmed)

### How it works

Alerts are NOT based on absolute score values. They're based on **percentage change between consecutive periods**:

```python
# Step 1: Calculate pct_change between consecutive periods
df["pct_change"] = df[col].pct_change() * 100

# Step 2: For neg column, invert sign
# (neg going from -100 → -50 is IMPROVING, should be positive change)
if col == "neg":
    df["pct_change"] *= -1

# Step 3: Classify by threshold
level_50 = df[abs(df["pct_change"]) >= 50]  # Major change
level_30 = df[(abs(df["pct_change"]) >= 30) & ~in_level_50]  # Moderate change

# Step 4: For each flagged period, find matching star tags
for period in flagged_periods:
    cung = get_cung_for_period(period)
    for star in cung.stars:
        row = lookup_star(star)
        # Check: does this star have pct_fvg_30/50 == "pos"/"neg"?
        # If change is positive AND star has pct_fvg == "pos" → 🔺 alert
        # If change is negative AND star has pct_fvg == "neg" → 🔻 alert
        tag = row[f"{dimension}_tag_{threshold}"]
        if tag:
            alerts.append(Alert(type=kind, tag=tag, ...))
```

### Alert direction matching
- Period has **positive pct_change ≥ threshold** → look for stars with `pct_fvg = "pos"`
- Period has **negative pct_change ≤ -threshold** → look for stars with `pct_fvg = "neg"`

### Alert display rules
- **Lifetime:** Don't show alerts after age 80 (age 60 for con_cai)
- **van_menh:** No alerts at all (lifetime chart)
- **con_cai slides:** Only shown for female gender

### Level priority
- Level 50 alerts take priority — if a period triggers both 30 and 50, only 50 is used

---

## SPECIAL RULES (from codebase analysis)

### Rule 1: Subject multiplier default
```python
if weight == "" or weight is NaN:
    mul = 1  # DEFAULT to 1, NOT skip
```
⚠️ This is different from the initial assumption. Empty weight → star still contributes with multiplier 1.

### Rule 2: 10-year anchor uses LIFETIME data
```python
def su_nghiep_10yrs(cung_point_10, org_df):  # org_df = LIFETIME data
    pos_a = get_col_value(org_df, "quan lộc", "pos") * 0.4  # ← from lifetime, NOT 10yr
    ...
```
The anchor is always calculated from `cung` (lifetime), even when scoring `cung_10yrs` or `cung_12months`.

### Rule 3: Monthly 13 data points
Monthly chart has 13 points: month 1 is duplicated at the start to create a wrapping effect:
```
x_data = [Th.1, Th.1, Th.2, Th.3, ..., Th.12]  # First month appears twice
```
Actually: first cung is prepended, creating `[cung[0], cung[0], cung[1], ..., cung[11]]`.

### Rule 4: van_menh monthly uses base points only
`van_menh_12m()` does NOT use subject multiplier — it uses raw `point` values only. All other `*_12m()` functions DO use their subject multipliers.

### Rule 5: 10-year uses only 10 of 12 cungs
```python
cungs = list(cung_point.keys())[:-2]  # Skip last 2 Đại Vận periods
```

### Rule 6: Lifetime x-axis
```python
x_data = list(range(0, 120, 10))  # [0, 10, 20, ..., 110]
# But chart typically shows 12 data points (12 cungs)
```

---

## DATA STRUCTURES

### Input (from Task 01)
```python
LasoData with:
  cung: list[Cung]              # 12 cungs, lifetime
  cung_10yrs: list[Cung]        # 12 cungs, Đại Vận ordered
  cung_12months: list[MonthlyCung]  # 12 monthly cungs
```

### Intermediate: cung_point dict
```python
# Built from LasoData — maps cung_name → {star_slug: base_point}
cung_point = {
    "mệnh": {"tu-vi": 10, "thien-phu-d": 9, "van-xuong-d": 8, ...},
    "quan lộc": {"pha-quan-d": 6, ...},
    ...  # 12 entries
}
```

### Output
```python
@dataclass
class Alert:
    type: str               # "positive" or "negative"
    dimension: str          # "su_nghiep", etc.
    period: str             # "20-30" or "2025" or "Th.3/2026"
    tag: str                # Vietnamese alert text
    level: int              # 30 or 50
    star_name: str          # Which star triggered

@dataclass
class ScorePoint:
    period: str             # x-axis label
    duong: float            # final_pos (Dương line)
    am: float               # final_neg (Âm line, negative value)
    tb: float               # final_sum = duong + am (Trung bình)

@dataclass
class DimensionScores:
    dimension: str          # key
    label: str              # Vietnamese label
    lifetime: list[ScorePoint]     # 12 points (ages 0-110, step 10)
    decade: list[ScorePoint]       # 10 points (years)
    monthly: list[ScorePoint]      # 13 points (12 months + wrap)
    alerts: list[Alert]
    summary_score: float           # aggregate for overview card

@dataclass
class ScoringResult:
    dimensions: dict[str, DimensionScores]  # 7 dimensions + van_menh = 8
    all_alerts: list[Alert]
```

**Note:** Actually **8 dimensions** in the code (including van_menh). van_menh has charts but no alerts. The laso_points `van_menh` column is empty → van_menh uses `mul = 1` for all stars (base points only).

---

## IMPLEMENTATION

### Module 1: Star Lookup

```python
from slugify import slugify
import pandas as pd

class StarLookup:
    def __init__(self, xlsx_path: str):
        self.df = pd.read_excel(xlsx_path, sheet_name='laso_points')
        self.df = self.df.drop_duplicates(subset=['sao'], keep='first')
        self.df['sao_index'] = self.df['sao'].apply(lambda x: slugify(str(x).lower()))
    
    def lookup(self, star_slug: str) -> pd.Series | None:
        """Lookup by pre-computed slug."""
        matches = self.df[self.df['sao_index'] == star_slug]
        if len(matches) == 0:
            return None
        return matches.iloc[0]
    
    def get_point_and_weight(self, star_slug: str, dimension: str) -> tuple[int, float] | None:
        """Returns (point, weight) for a star × dimension."""
        row = self.lookup(star_slug)
        if row is None:
            return None
        
        point = int(row['point'])
        weight = row.get(dimension)
        
        # CRITICAL: empty/NaN weight defaults to 1, NOT skip
        if weight is None or pd.isna(weight) or weight == '':
            weight = 1.0
        
        return point, float(weight)
```

### Module 2: Cung Point Builder

```python
def build_cung_point(cungs: list[Cung], lookup: StarLookup) -> dict[str, dict[str, int]]:
    """
    Build cung_point dict: {cung_name_lower: {star_slug: base_point}}
    """
    result = {}
    for cung in cungs:
        stars_dict = {}
        for star in cung.stars:
            row = lookup.lookup(star.slug)
            if row is not None:
                stars_dict[star.slug] = int(row['point'])
            else:
                logging.warning(f"Star not found: {star.name} (slug: {star.slug})")
        result[cung.name.lower()] = stars_dict
    return result
```

### Module 3: Scoring Engine

```python
DIMENSIONS = ['van_menh', 'su_nghiep', 'tien_bac', 'hon_nhan', 'suc_khoe', 'dat_dai', 'hoc_tap', 'con_cai']

# House weighting configuration per dimension
HOUSE_WEIGHTS = {
    'van_menh': [("mệnh", 0.4), ("thân", 0.2), ("quan lộc", 0.2), ("tài bạch", 0.2)],
    'su_nghiep': [("quan lộc", 0.4), ("mệnh", 0.2), ("tài bạch", 0.2), ("thiên di", 0.2)],
    'tien_bac': [("tài bạch", 0.4), ("mệnh", 0.2), ("quan lộc", 0.2), ("điền trạch", 0.2)],
    'hon_nhan': [("phu thê", 0.4), ("mệnh", 0.2), ("phúc đức", 0.2), ("nô bộc", 0.2)],
    'suc_khoe': [("tật ách", 0.6), ("phúc đức", 0.4)],
    'dat_dai': [("tật ách", 0.6), ("phúc đức", 0.4)],  # same as suc_khoe (intentional)
    'hoc_tap': [],  # TODO: extract from hoc_tap_all()
    'con_cai': [],  # TODO: extract from con_cai_all()
}

class ScoringEngine:
    def __init__(self, lookup: StarLookup):
        self.lookup = lookup
    
    def _raw_score(self, cung_point: dict, cung_name: str, dimension: str) -> tuple[float, float]:
        """Calculate raw pos/neg for one cung × one dimension."""
        stars = cung_point.get(cung_name.lower(), {})
        pos = 0.0
        neg = 0.0
        
        for star_slug, base_point in stars.items():
            result = self.lookup.get_point_and_weight(star_slug, dimension)
            if result is None:
                continue
            point, weight = result
            contribution = point * weight
            
            if point > 0:
                pos += contribution
            else:
                neg += contribution
        
        return pos, neg
    
    def _calc_anchor(self, cung_point: dict, dimension: str) -> tuple[float, float]:
        """Calculate house weighting anchor (constant from lifetime data)."""
        weights = HOUSE_WEIGHTS.get(dimension, [])
        anchor_pos = 0.0
        anchor_neg = 0.0
        
        for cung_name, weight in weights:
            pos, neg = self._raw_score(cung_point, cung_name, dimension)
            anchor_pos += pos * weight
            anchor_neg += neg * weight
        
        return anchor_pos, anchor_neg
    
    def _final_scores(self, cung_point: dict, cung_names: list[str], 
                       x_labels: list[str], dimension: str,
                       anchor_pos: float, anchor_neg: float) -> list[ScorePoint]:
        """Calculate final weighted scores for a list of cungs."""
        results = []
        for cung_name, label in zip(cung_names, x_labels):
            raw_pos, raw_neg = self._raw_score(cung_point, cung_name, dimension)
            final_pos = (raw_pos + anchor_pos) / 2
            final_neg = (raw_neg + anchor_neg) / 2
            final_sum = final_pos + final_neg
            results.append(ScorePoint(
                period=str(label),
                duong=round(final_pos, 2),
                am=round(final_neg, 2),
                tb=round(final_sum, 2)
            ))
        return results
    
    def calculate(self, laso: LasoData, birth_year: int, nam_xem: int = 2026) -> ScoringResult:
        """Full scoring pipeline."""
        # Build cung_point dicts
        cp_lifetime = build_cung_point(laso.cung, self.lookup)
        cp_10yrs = build_cung_point(laso.cung_10yrs, self.lookup)
        cp_monthly = build_cung_point(
            [MonthlyCung_to_Cung(mc) for mc in laso.cung_12months], 
            self.lookup
        )
        
        # Anchor is ALWAYS from lifetime data
        dimensions = {}
        all_alerts = []
        
        for dim in DIMENSIONS:
            anchor_pos, anchor_neg = self._calc_anchor(cp_lifetime, dim)
            
            # Lifetime: 12 cungs × ages 0-110
            lifetime_cungs = [c.name.lower() for c in laso.cung]
            lifetime_labels = list(range(0, 120, 10))
            lifetime = self._final_scores(cp_lifetime, lifetime_cungs, lifetime_labels, dim, anchor_pos, anchor_neg)
            
            # 10-year: first 10 of 12 cungs
            decade_cungs = [c.name.lower() for c in laso.cung_10yrs[:-2]]  # skip last 2
            decade_labels = list(range(nam_xem, nam_xem + 10))
            decade = self._final_scores(cp_10yrs, decade_cungs, decade_labels, dim, anchor_pos, anchor_neg)
            
            # Monthly: 13 points (first month duplicated)
            monthly_cungs = [laso.cung_12months[0].name.lower()]  # prepend first
            monthly_cungs += [mc.name.lower() for mc in laso.cung_12months]
            monthly_labels = [f"Th.1/{nam_xem}"]  # prepend label
            monthly_labels += [f"Th.{mc.month}/{nam_xem}" for mc in laso.cung_12months]
            
            # van_menh monthly: base points only (mul=1) — handled by empty weight default
            monthly = self._final_scores(cp_monthly, monthly_cungs, monthly_labels, dim, anchor_pos, anchor_neg)
            
            # Alerts (not for van_menh lifetime)
            alerts = []
            if dim != 'van_menh':
                alerts = self._calc_alerts(lifetime, decade, dim, cp_lifetime, cp_10yrs, birth_year)
            
            summary = sum(sp.tb for sp in lifetime) / len(lifetime) if lifetime else 0
            
            dimensions[dim] = DimensionScores(
                dimension=dim,
                label=DIMENSION_LABELS[dim],
                lifetime=lifetime,
                decade=decade,
                monthly=monthly,
                alerts=alerts,
                summary_score=round(summary, 2)
            )
            all_alerts.extend(alerts)
        
        return ScoringResult(dimensions=dimensions, all_alerts=all_alerts)
```

### Module 4: Alert Calculator

```python
def _calc_alerts(self, lifetime: list[ScorePoint], decade: list[ScorePoint],
                  dimension: str, cp_lifetime: dict, cp_10yrs: dict,
                  birth_year: int) -> list[Alert]:
    """Calculate alerts based on pct_change between periods."""
    alerts = []
    
    # Process both pos and neg columns for both timeframes
    for scores, cp, timeframe in [
        (lifetime, cp_lifetime, "lifetime"),
        (decade, cp_10yrs, "decade")
    ]:
        for col in ["duong", "am"]:
            col_name = "pos" if col == "duong" else "neg"
            values = [getattr(sp, col) for sp in scores]
            
            for i in range(1, len(values)):
                if values[i-1] == 0:
                    continue
                pct_change = ((values[i] - values[i-1]) / abs(values[i-1])) * 100
                
                # Invert for neg column
                if col_name == "neg":
                    pct_change *= -1
                
                # Skip display after age 80 (60 for con_cai) on lifetime
                if timeframe == "lifetime":
                    age = int(scores[i].period)
                    max_age = 60 if dimension == 'con_cai' else 80
                    if age >= max_age:
                        continue
                
                # Check thresholds (50 first, then 30 if not 50)
                level = None
                if abs(pct_change) >= 50:
                    level = 50
                elif abs(pct_change) >= 30:
                    level = 30
                
                if level is None:
                    continue
                
                kind = "pos" if pct_change > 0 else "neg"
                period = scores[i].period
                
                # Find matching star tags in the cung for this period
                cung_name = self._get_cung_for_period(scores, i, cp)
                cung_stars = cp.get(cung_name, {})
                
                for star_slug in cung_stars:
                    tag = self._get_tag(star_slug, dimension, kind, level)
                    if tag:
                        alerts.append(Alert(
                            type="positive" if kind == "pos" else "negative",
                            dimension=dimension,
                            period=str(period),
                            tag=tag,
                            level=level,
                            star_name=star_slug
                        ))
    
    return alerts

def _get_tag(self, star_slug: str, dimension: str, kind: str, level: int) -> str | None:
    """Look up alert tag text from laso_points."""
    row = self.lookup.lookup(star_slug)
    if row is None:
        return None
    
    pct_col = f'pct_fvg_{level}'
    tag_col = f'{dimension}_tag_{level}'
    
    pct_val = row.get(pct_col)
    if pct_val != kind:  # Must match pos/neg direction
        return None
    
    tag = row.get(tag_col)
    if tag is None or pd.isna(tag) or str(tag).strip() == '':
        return None
    
    return str(tag)
```

---

## DIMENSIONS COUNT — Actually 8

The code processes **8 dimensions** (including van_menh), but van_menh has special rules:

| Dimension | Has charts | Has alerts | Subject multiplier | In laso_points |
|-----------|-----------|------------|-------------------|---------------|
| van_menh | ✅ | ❌ (lifetime) | Uses `1` (column empty) | Column exists but empty |
| su_nghiep | ✅ | ✅ | From column | ✅ |
| tien_bac | ✅ | ✅ | From column | ✅ |
| hon_nhan | ✅ | ✅ | From column | ✅ |
| suc_khoe | ✅ | ✅ | From column | ✅ |
| dat_dai | ✅ | ✅ | From column | ✅ |
| hoc_tap | ✅ | ✅ | From column | ✅ |
| con_cai | ✅ | ✅ (female only slides) | From column | ✅ |

**Decision for MVP:** Include all 8 in scoring. Frontend can choose to display van_menh or not. Con_cai shown for all genders (remove gender restriction for MVP — it was a slide display choice, not a data choice).

---

## VALIDATION

### Must match existing output for test case:
```python
payload = {"ngay_sinh": "19/07/1994", "gio_sinh": "06h00", "gender": "Nam", "nam_xem": 2026}
```

Run through existing codebase → capture all DataFrames → save as fixtures → compare.

### Test checklist
```python
def test_scoring_accuracy():
    # For each test case:
    # 1. Load laso fixture (from Task 01)
    # 2. Run scoring engine
    # 3. Compare lifetime[dim].duong values with expected (tolerance ±0.5)
    # 4. Compare alerts count and tags
    # 5. Verify anchor values match
```

---

## ACCEPTANCE CRITERIA

- [ ] Loads laso_points.xlsx (222 unique stars after dedup)
- [ ] Star matching via `slugify(name.lower())` — same algorithm as existing code
- [ ] Empty weight defaults to `1` (not skip) — verified
- [ ] Raw score formula: `point × weight`, split by point > 0 (pos) vs point ≤ 0 (neg)
- [ ] House weighting: anchor from lifetime data, applied to all timeframes
- [ ] Final: `(raw + anchor) / 2` for pos and neg separately
- [ ] TB = pos + neg (algebraic sum, not average)
- [ ] 8 dimensions (including van_menh)
- [ ] Lifetime: 12 data points
- [ ] Decade: 10 data points (skip last 2 cungs)
- [ ] Monthly: 13 data points (first month prepended)
- [ ] Alerts: pct_change ≥ 30% (level 30) or ≥ 50% (level 50), level 50 priority
- [ ] Alert neg column: pct_change inverted before threshold check
- [ ] No alerts for van_menh lifetime
- [ ] No alerts after age 80 (60 for con_cai)
- [ ] Output matches existing codebase for ≥ 3 test cases (±0.5 tolerance)
- [ ] Performance: < 200ms per profile

---

## REMAINING UNKNOWNS

| # | What | Action |
|---|------|--------|
| 1 | hoc_tap anchor cungs + weights | Extract from `hoc_tap_all()` in export_report.py |
| 2 | con_cai anchor cungs + weights | Extract from `con_cai_all()` in export_report.py |
| 3 | "thân" cung mapping | `than_cu` field from CohocData tells which cung = Thân |
| 4 | Cung name for "nô bộc" | May appear as "Nô Bộc" or "Giao Hữu" in scraper output |

**Ask founder:** Can you run Claude Code again on the codebase to extract the exact `hoc_tap_all()` and `con_cai_all()` functions? Or share those specific functions.