# AI Luận Giải Pipeline Design Spec

**Date:** 2026-03-27
**Task:** `docs/tasks/03_ai_pipeline.md`
**Status:** Approved

---

## Overview

The AI Pipeline receives `ScoringResult` (from Task 02) + `LasoData` (from Task 01) + user profile data and produces personalized Vietnamese luận giải text for 7 dimensions + 1 overview. Each dimension call sends a structured prompt containing Knowledge Base content, user data, scores, and alerts to Claude Sonnet API, returning ~500-1000 words of interpretation.

**Architecture:** Single `AIEngine` class. Loads KB markdown files at init, builds prompts per request, runs 8 concurrent async Claude API calls. Stateless after init.

---

## 1. Knowledge Base Structure

### 1.1 Directory Layout

```
backend/knowledge_base/
├── core/
│   ├── scoring_rules.md          # How Dương/Âm/TB scores work (~500 words)
│   ├── alert_interpretation.md   # How to read 🔺🔻 alerts (~300 words)
│   └── tone_guidelines.md        # Language rules + ethics (~300 words)
├── dimensions/
│   ├── su_nghiep.md              # ~500-1000 words each
│   ├── tien_bac.md
│   ├── hon_nhan.md
│   ├── suc_khoe.md
│   ├── dat_dai.md
│   ├── hoc_tap.md
│   └── con_cai.md
├── stars/
│   ├── chinh_tinh.md             # 14 major stars
│   └── phu_tinh.md               # Minor stars
└── examples/
    └── approved_outputs/
        ├── sample_su_nghiep.md   # Expert-approved example
        └── sample_tien_bac.md    # Expert-approved example
```

**No `van_menh.md` dimension file** — van_menh has charts but no AI luận giải (per spec: "van_menh có charts nhưng KHÔNG có alerts"). Overview covers the tổng quan role.

### 1.2 KB Content Sources

| KB File | Source | Status |
|---------|--------|--------|
| `core/scoring_rules.md` | Developer writes from ARCHITECTURE.md scoring formulas | Can write now |
| `core/alert_interpretation.md` | Developer writes from scoring spec | Can write now |
| `core/tone_guidelines.md` | From `reasoning_flow.md` (expert mock) + SPEC.md tone rules | Can write now (mock) |
| `dimensions/*.md` | From `dimension_*.md` (expert mock) | Mock now, replace later |
| `stars/chinh_tinh.md` | Developer writes from tử vi reference | Can write now (skeleton) |
| `stars/phu_tinh.md` | Developer writes from tử vi reference | Can write now (skeleton) |
| `examples/approved_outputs/*` | Expert must approve | Mock now |

### 1.3 KB Loading

```python
@dataclass
class KnowledgeBase:
    core: dict[str, str]              # {"scoring_rules": "...", "alert_interpretation": "...", "tone_guidelines": "..."}
    dimensions: dict[str, str]        # {"su_nghiep": "...", "tien_bac": "...", ...}
    stars: dict[str, str]             # {"chinh_tinh": "...", "phu_tinh": "..."}
    examples: dict[str, str]          # {"sample_su_nghiep": "...", ...}
```

Load all files at init into memory. Total ~20-30K tokens across all KB files. Well within context limits.

---

## 2. Prompt Structure

### 2.1 Dimension Prompt (7 calls)

Each dimension call produces a `messages` array with a single system message + single user message:

**System message:**
```
[ROLE DEFINITION]
Bạn là tư vấn viên luận giải tử vi chuyên nghiệp, sử dụng hệ thống Chánh Ngã Đồ (Tử Vi Đẩu Số + scoring analytics). Nhiệm vụ: viết luận giải cá nhân hóa cho 1 lĩnh vực dựa trên data được cung cấp.

[RULES — NON-NEGOTIABLE]
1. Chỉ nói về data được cung cấp — KHÔNG bịa đặt
2. Ngôn ngữ tích cực, empowering — giọng văn "anh trai khuyên em"
3. Mỗi cảnh báo 🔻 PHẢI đi kèm lời khuyên cụ thể
4. Dùng "cần thận trọng" thay vì "sẽ gặp họa"
5. Kết thúc bằng disclaimer
6. Viết tiếng Việt tự nhiên, không quá trang trọng, không thần bí

[KNOWLEDGE BASE — CORE]
{scoring_rules.md content}
{alert_interpretation.md content}

[KNOWLEDGE BASE — TONE]
{tone_guidelines.md content}

[KNOWLEDGE BASE — DIMENSION: {dimension_label}]
{dimensions/{dimension}.md content}

[RELEVANT STARS]
{filtered star content for stars present in user's relevant cungs}
```

**User message:**
```
[USER DATA]
- Tên: {name or "Bạn"}
- Sinh: {birth_date} ({lunar_year_name}), Giờ {birth_hour_label}, {gender_label}
- Tuổi hiện tại: {current_age}
- Cung Mệnh: {cung_menh} — Mệnh {menh_ngu_hanh}
- Cung {primary_cung_for_dimension}: {stars_list}

[SCORE DATA — {dimension_label}]
### Cả đời (mốc 10 năm):
| Giai đoạn | Dương | Âm | TB |
{lifetime_scores_table}

### 10 năm hiện tại ({decade_start}-{decade_end}):
| Năm | Dương | Âm | TB |
{decade_scores_table}

### 12 tháng ({current_year}):
| Tháng | Dương | Âm | TB |
{monthly_scores_table}

[ALERTS — {dimension_label}]
{formatted_alerts or "Không có cảnh báo đặc biệt."}

[EXAMPLE OUTPUT]
{example if available, else omit section}

[OUTPUT FORMAT]
Viết luận giải tiếng Việt theo format:

## Tổng quan {dimension_label}
(3-5 câu nhận xét tổng thể dựa trên pattern cả đời)

## Giai đoạn hiện tại ({decade_range})
(Phân tích 10 năm hiện tại, xu hướng Dương/Âm)

## Các mốc cần chú ý
(Mỗi alert: giải thích tại sao + nên làm gì / tránh gì. Nếu không có alert, viết về các mốc đáng lưu ý từ score patterns)

## Lời khuyên
(2-3 điều cụ thể, actionable, phù hợp với tuổi {current_age})

---
*Đây là luận giải tham khảo dựa trên Tử Vi Đẩu Số. Mọi quyết định cuối cùng là của bạn.*
```

### 2.2 Overview Prompt (1 call)

**System message:** Same role + rules + core KB + tone KB (no dimension-specific KB).

**User message:**
```
[USER DATA — same as above]

[ALL DIMENSION SUMMARIES]
{for each dim: "{label}: TB trung bình {summary_score}, {alert_count} cảnh báo ({pos_count} 🔺, {neg_count} 🔻)"}

[OUTPUT FORMAT]
Viết tổng quan vận mệnh trong 3-5 câu. Nhận xét bức tranh lớn:
- Xu hướng tổng thể
- Lĩnh vực mạnh nhất
- Lĩnh vực cần chú ý nhất
Ngắn gọn, súc tích, gợi mở để người xem muốn đọc chi tiết từng lĩnh vực.

---
*Đây là tổng quan tham khảo dựa trên Tử Vi Đẩu Số. Mọi quyết định cuối cùng là của bạn.*
```

### 2.3 Star Filtering for Prompts

Not all star info is included in every dimension call. Filter:
1. Get the primary cung(s) for the dimension (from HOUSE_WEIGHTS keys)
2. Get all stars in those cungs from LasoData
3. Filter `chinh_tinh.md` content to only include stars present in user's relevant cungs

This keeps the prompt focused and reduces token count.

---

## 3. Data Structures

### 3.1 Input Types

```python
@dataclass
class UserProfile:
    name: str | None                  # "Nguyễn Văn A" or None → "Bạn"
    birth_date: date                  # dương lịch
    birth_hour: str                   # "dan", "ty", etc.
    birth_hour_label: str             # "Giờ Dần (03:00-05:00)"
    gender: str                       # "male" / "female"
    gender_label: str                 # "Nam" / "Nữ"
    current_age: int                  # calculated
    nam_xem: int                     # 2026

@dataclass
class LasoMetadata:
    nam: str                          # "Giáp Tuất"
    menh: str                         # "Mộc"
    cuc: str                          # "Thủy Nhị Cục"
    am_duong: str                     # "Dương Nam"
    cung_menh: str                    # Cung name where Mệnh resides
```

These come from scraper (LasoData) and the API request. AIEngine doesn't need to know about scraper internals.

### 3.2 Output

```python
@dataclass
class InterpretationResult:
    overview: str                              # Overview markdown text
    dimensions: dict[str, str]                 # {"su_nghiep": "## Tổng quan...", ...}
    errors: dict[str, str]                     # {"tien_bac": "APIError"} — partial failures
    token_usage: dict[str, tuple[int, int]]    # {"su_nghiep": (input_tokens, output_tokens)}
```

### 3.3 Dimension → Cung Mapping (for star filtering)

```python
DIMENSION_PRIMARY_CUNGS: dict[str, list[str]] = {
    "su_nghiep": ["quan lộc", "mệnh"],
    "tien_bac":  ["tài bạch", "mệnh"],
    "hon_nhan":  ["phu thê", "mệnh"],
    "suc_khoe":  ["tật ách", "phúc đức"],
    "dat_dai":   ["điền trạch", "tài bạch"],
    "hoc_tap":   ["mệnh", "quan lộc"],
    "con_cai":   ["tử tức", "phúc đức"],
}
```

---

## 4. Class API

```python
class AIEngine:
    """Stateless AI text generator. Load KB once, reuse across requests."""

    def __init__(self, kb_dir: str, api_key: str):
        self._kb: KnowledgeBase = self._load_kb(kb_dir)
        self._client: anthropic.AsyncAnthropic = anthropic.AsyncAnthropic(api_key=api_key)

    async def generate_all(
        self,
        user: UserProfile,
        metadata: LasoMetadata,
        laso: LasoData,
        scoring: ScoringResult,
        progress_callback: Callable[[int, int], Awaitable[None]] | None = None,
    ) -> InterpretationResult:
        """Generate overview + 7 dimensions concurrently. Main entry point."""
        ...

    async def generate_dimension(
        self,
        dimension: str,
        user: UserProfile,
        metadata: LasoMetadata,
        laso: LasoData,
        dim_scores: DimensionScores,
    ) -> str:
        """Generate luận giải for a single dimension."""
        ...

    async def generate_overview(
        self,
        user: UserProfile,
        metadata: LasoMetadata,
        scoring: ScoringResult,
    ) -> str:
        """Generate overview summary across all dimensions."""
        ...

    # --- Private ---
    def _load_kb(self, kb_dir: str) -> KnowledgeBase: ...
    def _build_dimension_prompt(self, ...) -> tuple[str, str]: ...  # (system, user)
    def _build_overview_prompt(self, ...) -> tuple[str, str]: ...
    def _format_scores_table(self, points: list[ScorePoint]) -> str: ...
    def _format_alerts(self, alerts: list[Alert]) -> str: ...
    def _filter_stars_for_dimension(self, dim: str, laso: LasoData) -> str: ...
```

---

## 5. Claude API Configuration

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| `model` | `claude-sonnet-4-20250514` | Best quality/speed/cost balance |
| `max_tokens` | 2000 | ~500-1000 words per dimension |
| `temperature` | 0.7 | Natural text, not too random |
| `system` | Full system prompt | Role + rules + KB in system message |

### 5.1 Retry Strategy

```python
MAX_RETRIES = 3
RETRY_DELAYS = [2, 5, 10]  # seconds — exponential backoff
TIMEOUT_PER_CALL = 60      # seconds

RETRYABLE_ERRORS = [
    anthropic.RateLimitError,
    anthropic.APIConnectionError,
    anthropic.InternalServerError,
]
```

### 5.2 Cost Estimation

```
Per dimension call:
  System prompt:  ~3-5K tokens (role + rules + core KB + dimension KB + stars)
  User message:   ~2-3K tokens (user data + 3 score tables + alerts + format)
  Total input:    ~5-8K tokens
  Output:         ~800-1500 tokens
  Cost:           ~$0.005-0.01

Per profile (8 calls):
  Total input:    ~40-64K tokens
  Total output:   ~6-12K tokens
  Cost:           ~$0.04-0.08

50 test users: ~$2-4
```

---

## 6. Concurrency & Error Handling

### 6.1 Parallel Execution

```python
async def generate_all(...) -> InterpretationResult:
    tasks = {}
    # 7 dimension tasks
    for dim in ["su_nghiep", "tien_bac", "hon_nhan", "suc_khoe", "dat_dai", "hoc_tap", "con_cai"]:
        tasks[dim] = self.generate_dimension(dim, ...)
    # 1 overview task
    tasks["overview"] = self.generate_overview(...)

    results = await asyncio.gather(*tasks.values(), return_exceptions=True)

    # Process results — partial failure OK
    dimensions = {}
    errors = {}
    for key, result in zip(tasks.keys(), results):
        if isinstance(result, Exception):
            errors[key] = f"{type(result).__name__}: {str(result)}"
        elif key == "overview":
            overview = result
        else:
            dimensions[key] = result

        if progress_callback:
            await progress_callback(completed_count, 8)
```

### 6.2 Partial Failure

If a dimension call fails after retries:
- Other dimensions still return normally
- Failed dimension gets error message in `errors` dict
- Frontend displays: "Luận giải đang được xử lý, vui lòng thử lại sau."
- Overview can fail independently — frontend shows dimension cards without summary

### 6.3 Total Timeout

`generate_all` has a 90-second overall timeout. If not all calls complete, return whatever finished + errors for the rest.

---

## 7. Score Formatting

### 7.1 Lifetime Table

```
| Giai đoạn | Dương | Âm | TB |
|-----------|-------|-----|-----|
| 0-10 | 15.20 | -8.30 | 6.90 |
| 10-20 | 18.40 | -5.10 | 13.30 |
...
```

### 7.2 Decade Table

```
| Năm | Dương | Âm | TB |
|-----|-------|-----|-----|
| 2026 | 12.50 | -6.20 | 6.30 |
...
```

### 7.3 Monthly Table

```
| Tháng | Dương | Âm | TB |
|-------|-------|-----|-----|
| Th.1/2026 | 10.00 | -4.50 | 5.50 |
...
```

### 7.4 Alert Formatting

```
🔺 2027 (Level 50): có bước thăng tiến hoặc đạt được sự công nhận [sao: Hóa Cái]
🔻 2029 (Level 30): cẩn thận kiện cáo hoặc tranh chấp [sao: Đà La]
```

---

## 8. File Structure

```
backend/
├── app/
│   ├── services/
│   │   └── ai_engine.py        # AIEngine class (~350-450 lines)
│   └── models/
│       └── schemas.py           # InterpretationResult, UserProfile (extend existing)
├── knowledge_base/              # KB markdown files (loaded at runtime)
│   ├── core/
│   ├── dimensions/
│   ├── stars/
│   └── examples/
└── tests/
    ├── test_ai_kb.py            # KB loading tests
    ├── test_ai_prompt.py        # Prompt building tests
    ├── test_ai_format.py        # Score/alert formatting tests
    ├── test_ai_engine.py        # Integration tests (mocked API)
    └── fixtures/
        └── sample_scoring.json  # ScoringResult fixture for prompt tests
```

### Dependencies

- `anthropic` — Claude API client (async)
- Existing: `dataclasses`, `asyncio`, `pathlib`
- No other new external dependencies

---

## 9. Edge Cases

| Case | Behavior |
|------|----------|
| User name is None | Use "Bạn" in prompts |
| No alerts for a dimension | Prompt includes: "Không có cảnh báo đặc biệt." AI writes about score patterns instead |
| Many alerts (>5) per dimension | Include all in prompt — AI's instructions say prioritize most important |
| Very young (born 2005+) | `current_age` included in prompt — AI adjusts language naturally |
| Very old (born 1930s) | Same — age context guides AI |
| Claude rate limit | Retry with exponential backoff (3 retries) |
| Claude timeout | 60s per call, return error for that dimension |
| KB file missing | Raise `KBLoadError` at startup — fail fast |
| Star in cung not in KB stars file | OK — star filtering produces whatever matches, AI works with available data |
| Empty score table (all zeros) | Still format as table — AI interprets flat pattern |

---

## 10. Quality Validation

### 10.1 Automated Checks

Every AI output is checked after generation:

```python
def validate_output(text: str, dimension: str) -> list[str]:
    """Returns list of warnings (empty = pass)."""
    warnings = []
    if "sẽ gặp họa" in text:
        warnings.append("TONE: Contains forbidden phrase 'sẽ gặp họa'")
    if not text.strip().endswith("*"):  # disclaimer ends with italic marker
        warnings.append("MISSING: No disclaimer at end")
    if len(text) < 200:
        warnings.append("SHORT: Output under 200 chars")
    if len(text) > 5000:
        warnings.append("LONG: Output over 5000 chars")
    return warnings
```

Warnings are logged, not blocking. For MVP, human review is the quality gate.

### 10.2 Expert Review Process

1. Generate 5+ profiles with mock KB
2. Expert reviews AI output alongside real lá số data
3. Rate each output 1-10
4. Integrate feedback into KB files
5. Target: ≥ 7/10 average
