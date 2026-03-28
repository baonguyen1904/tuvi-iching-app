# AI Luận Giải Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the AI luận giải engine that transforms ScoringResult + LasoData + UserProfile into personalized Vietnamese interpretations for 7 dimensions + 1 overview via Claude Sonnet API.

**Architecture:** Single `AIEngine` class loads KB markdown files at init into memory. `generate_all()` runs 8 concurrent async API calls. TDD throughout — prompt building and formatting tested with deterministic inputs, API calls mocked.

**Tech Stack:** Python 3.11+, anthropic SDK, asyncio, pytest, pytest-asyncio

---

## File Structure

| File | Responsibility |
|------|---------------|
| `backend/knowledge_base/core/scoring_rules.md` | How Dương/Âm/TB scores work |
| `backend/knowledge_base/core/alert_interpretation.md` | How to read 🔺🔻 alerts |
| `backend/knowledge_base/core/tone_guidelines.md` | Language rules + ethics |
| `backend/knowledge_base/dimensions/*.md` | Per-dimension interpretation guides (7 files) |
| `backend/knowledge_base/stars/chinh_tinh.md` | 14 major star descriptions |
| `backend/knowledge_base/stars/phu_tinh.md` | Minor star descriptions |
| `backend/knowledge_base/examples/approved_outputs/*.md` | Expert-approved sample outputs |
| `backend/app/services/ai_engine.py` | `AIEngine` class — KB loading, prompt building, API calls, orchestration |
| `backend/app/models/schemas.py` | Extend with `UserProfile`, `LasoMetadata`, `InterpretationResult` |
| `backend/tests/test_ai_kb.py` | KB loading + validation tests |
| `backend/tests/test_ai_format.py` | Score/alert formatting tests |
| `backend/tests/test_ai_prompt.py` | Prompt assembly tests |
| `backend/tests/test_ai_engine.py` | Integration tests with mocked Claude API |
| `backend/tests/fixtures/sample_scoring.json` | ScoringResult fixture |

---

### Task 1: Output Schemas + Constants

**Files:**
- Modify: `backend/app/models/schemas.py`

- [ ] **Step 1: Write failing test for new schemas**

Create `backend/tests/test_ai_schemas.py`:
```python
from backend.app.models.schemas import (
    UserProfile,
    LasoMetadata,
    InterpretationResult,
)
from datetime import date


def test_user_profile_with_name():
    user = UserProfile(
        name="Nguyễn Văn A",
        birth_date=date(1994, 7, 19),
        birth_hour="dan",
        birth_hour_label="Giờ Dần (03:00-05:00)",
        gender="male",
        gender_label="Nam",
        current_age=31,
        nam_xem=2026,
    )
    assert user.name == "Nguyễn Văn A"
    assert user.display_name == "Nguyễn Văn A"


def test_user_profile_without_name():
    user = UserProfile(
        name=None,
        birth_date=date(1994, 7, 19),
        birth_hour="dan",
        birth_hour_label="Giờ Dần (03:00-05:00)",
        gender="male",
        gender_label="Nam",
        current_age=31,
        nam_xem=2026,
    )
    assert user.display_name == "Bạn"


def test_interpretation_result_all_success():
    result = InterpretationResult(
        overview="Tổng quan...",
        dimensions={"su_nghiep": "## Tổng quan...", "tien_bac": "## Tiền bạc..."},
        errors={},
        token_usage={"su_nghiep": (5000, 1200)},
    )
    assert result.has_errors is False
    assert result.completed_count == 2


def test_interpretation_result_partial_failure():
    result = InterpretationResult(
        overview="Tổng quan...",
        dimensions={"su_nghiep": "## Tổng quan..."},
        errors={"tien_bac": "RateLimitError"},
        token_usage={},
    )
    assert result.has_errors is True
    assert result.completed_count == 1
```

- [ ] **Step 2: Implement schemas**

Add to `backend/app/models/schemas.py`:
- `UserProfile` dataclass with `display_name` property (returns name or "Bạn")
- `LasoMetadata` dataclass
- `InterpretationResult` dataclass with `has_errors` and `completed_count` properties

- [ ] **Step 3: Run tests — all pass**

---

### Task 2: Knowledge Base Files (Mock Content)

**Files:**
- Create: All KB markdown files under `backend/knowledge_base/`

- [ ] **Step 1: Write KB loading test**

Create `backend/tests/test_ai_kb.py`:
```python
from backend.app.services.ai_engine import KnowledgeBase, load_kb
import os


def test_load_kb_all_core_files():
    kb = load_kb("backend/knowledge_base")
    assert "scoring_rules" in kb.core
    assert "alert_interpretation" in kb.core
    assert "tone_guidelines" in kb.core
    assert len(kb.core) == 3


def test_load_kb_all_dimensions():
    kb = load_kb("backend/knowledge_base")
    expected = ["su_nghiep", "tien_bac", "hon_nhan", "suc_khoe", "dat_dai", "hoc_tap", "con_cai"]
    for dim in expected:
        assert dim in kb.dimensions, f"Missing dimension: {dim}"
    assert len(kb.dimensions) == 7


def test_load_kb_stars():
    kb = load_kb("backend/knowledge_base")
    assert "chinh_tinh" in kb.stars
    assert "phu_tinh" in kb.stars


def test_load_kb_nonempty_content():
    kb = load_kb("backend/knowledge_base")
    for key, content in kb.core.items():
        assert len(content) > 50, f"Core KB '{key}' too short"
    for key, content in kb.dimensions.items():
        assert len(content) > 100, f"Dimension KB '{key}' too short"


def test_load_kb_missing_dir_raises():
    with pytest.raises(KBLoadError):
        load_kb("/nonexistent/path")


def test_load_kb_missing_core_file_raises():
    # If any core file is missing, fail fast
    # (Test by temporarily renaming — or use a temp dir with incomplete files)
    pass  # Handled by integration test
```

- [ ] **Step 2: Write core KB files**

Create `backend/knowledge_base/core/scoring_rules.md`:
- Explain Dương (positive energy), Âm (negative energy), TB (balance) scores
- What high/low values mean
- How crossover points work
- How to read patterns over time
- Source: ARCHITECTURE.md scoring formulas + mock expert reasoning_flow.md

Create `backend/knowledge_base/core/alert_interpretation.md`:
- What 🔺 (opportunity) and 🔻 (risk) represent
- Level 30 vs Level 50 significance
- How to interpret in context of surrounding scores
- Source: Scoring spec alert detection logic

Create `backend/knowledge_base/core/tone_guidelines.md`:
- Empowering tone rules
- Forbidden phrases: "sẽ gặp họa", "xấu", "hạn"
- Required patterns: every 🔻 must pair with advice
- Language style: "anh trai khuyên em" — direct but warm
- Source: Mock expert `reasoning_flow.md` + SPEC.md rules

- [ ] **Step 3: Write dimension KB files (7 files)**

Create `backend/knowledge_base/dimensions/{dim}.md` for each dimension.
Content from `data/mock_expert_input/dimension_{dim}.md`:
- Primary + secondary cungs
- Score pattern interpretations (high Dương, deep Âm, crossover, flat)
- Common alerts + expanded explanations
- Age-appropriate advice
- Common misconceptions

- [ ] **Step 4: Write star reference files**

Create `backend/knowledge_base/stars/chinh_tinh.md`:
- 14 major stars: Tử Vi, Thiên Cơ, Thái Dương, Vũ Khúc, Thiên Đồng, Liêm Trinh, Thiên Phủ, Thái Âm, Tham Lang, Cự Môn, Thiên Tướng, Thiên Lương, Thất Sát, Phá Quân
- Each: 2-3 sentences on meaning, positive/negative aspects
- Mock content — will refine with expert input

Create `backend/knowledge_base/stars/phu_tinh.md`:
- Key minor stars that commonly trigger alerts
- Skeleton with most impactful phu tinh

- [ ] **Step 5: Write example output files**

Create `backend/knowledge_base/examples/approved_outputs/sample_su_nghiep.md`:
- A complete example luận giải for sự nghiệp dimension
- Follows the exact output format from spec
- Source: Synthesized from mock case study #2

- [ ] **Step 6: Implement `load_kb()` function + `KnowledgeBase` dataclass**

In `backend/app/services/ai_engine.py`:
```python
@dataclass
class KnowledgeBase:
    core: dict[str, str]
    dimensions: dict[str, str]
    stars: dict[str, str]
    examples: dict[str, str]

class KBLoadError(Exception):
    pass

def load_kb(kb_dir: str) -> KnowledgeBase:
    """Load all KB markdown files. Raises KBLoadError if required files missing."""
    ...
```

- [ ] **Step 7: Run tests — all KB tests pass**

---

### Task 3: Score & Alert Formatting

**Files:**
- Create: `backend/app/services/ai_engine.py` (add formatting functions)
- Create: `backend/tests/test_ai_format.py`

- [ ] **Step 1: Write failing formatting tests**

Create `backend/tests/test_ai_format.py`:
```python
from backend.app.services.ai_engine import format_scores_table, format_alerts
from backend.app.models.schemas import ScorePoint, Alert


def test_format_lifetime_table():
    points = [
        ScorePoint(period="0-10", duong=15.20, am=-8.30, tb=6.90),
        ScorePoint(period="10-20", duong=18.40, am=-5.10, tb=13.30),
    ]
    table = format_scores_table(points)
    assert "| Giai đoạn | Dương | Âm | TB |" in table
    assert "| 0-10 | 15.20 | -8.30 | 6.90 |" in table
    assert "| 10-20 | 18.40 | -5.10 | 13.30 |" in table


def test_format_decade_table():
    points = [ScorePoint(period="2026", duong=12.50, am=-6.20, tb=6.30)]
    table = format_scores_table(points, header="Năm")
    assert "| Năm | Dương | Âm | TB |" in table


def test_format_monthly_table():
    points = [ScorePoint(period="Th.1/2026", duong=10.00, am=-4.50, tb=5.50)]
    table = format_scores_table(points, header="Tháng")
    assert "| Tháng | Dương | Âm | TB |" in table


def test_format_alerts_positive():
    alerts = [
        Alert(type="positive", dimension="su_nghiep", period="2027",
              tag="có bước thăng tiến", level=50, star_name="hoa-cai"),
    ]
    text = format_alerts(alerts)
    assert "🔺" in text
    assert "2027" in text
    assert "có bước thăng tiến" in text


def test_format_alerts_negative():
    alerts = [
        Alert(type="negative", dimension="su_nghiep", period="2029",
              tag="cẩn thận kiện cáo", level=30, star_name="da-la"),
    ]
    text = format_alerts(alerts)
    assert "🔻" in text


def test_format_alerts_empty():
    text = format_alerts([])
    assert "Không có cảnh báo đặc biệt" in text


def test_format_alerts_sorted_by_level():
    alerts = [
        Alert(type="negative", dimension="su_nghiep", period="2029",
              tag="cẩn thận", level=30, star_name="x"),
        Alert(type="positive", dimension="su_nghiep", period="2027",
              tag="thăng tiến", level=50, star_name="y"),
    ]
    text = format_alerts(alerts)
    # Level 50 should appear before level 30
    pos_50 = text.index("thăng tiến")
    pos_30 = text.index("cẩn thận")
    assert pos_50 < pos_30
```

- [ ] **Step 2: Implement formatting functions**

```python
def format_scores_table(points: list[ScorePoint], header: str = "Giai đoạn") -> str:
    """Format score points as markdown table."""
    ...

def format_alerts(alerts: list[Alert]) -> str:
    """Format alerts as readable text with 🔺🔻 markers."""
    ...
```

- [ ] **Step 3: Run tests — all pass**

---

### Task 4: Prompt Builder — Dimension

**Files:**
- Modify: `backend/app/services/ai_engine.py`
- Create: `backend/tests/test_ai_prompt.py`
- Create: `backend/tests/fixtures/sample_scoring.json`

- [ ] **Step 1: Create scoring fixture**

Create `backend/tests/fixtures/sample_scoring.json`:
- A complete `ScoringResult` with 2-3 dimensions filled
- Include alerts for at least 1 dimension
- Include an empty-alert dimension
- Use realistic Vietnamese data

- [ ] **Step 2: Write failing prompt building tests**

Create `backend/tests/test_ai_prompt.py`:
```python
def test_dimension_prompt_has_system_and_user():
    system, user = engine._build_dimension_prompt("su_nghiep", ...)
    assert isinstance(system, str)
    assert isinstance(user, str)
    assert len(system) > 500  # KB content included
    assert len(user) > 200    # Score data included


def test_dimension_prompt_contains_role():
    system, _ = engine._build_dimension_prompt("su_nghiep", ...)
    assert "tư vấn viên luận giải tử vi" in system


def test_dimension_prompt_contains_rules():
    system, _ = engine._build_dimension_prompt("su_nghiep", ...)
    assert "KHÔNG bịa đặt" in system
    assert "cần thận trọng" in system


def test_dimension_prompt_contains_core_kb():
    system, _ = engine._build_dimension_prompt("su_nghiep", ...)
    assert "Dương" in system  # from scoring_rules.md
    assert "🔺" in system or "🔻" in system  # from alert_interpretation.md


def test_dimension_prompt_contains_dimension_kb():
    system, _ = engine._build_dimension_prompt("su_nghiep", ...)
    assert "Quan Lộc" in system  # su_nghiep specific


def test_dimension_prompt_user_contains_scores():
    _, user = engine._build_dimension_prompt("su_nghiep", ...)
    assert "| Giai đoạn |" in user  # lifetime table
    assert "| Năm |" in user        # decade table
    assert "| Tháng |" in user      # monthly table


def test_dimension_prompt_user_contains_alerts():
    _, user = engine._build_dimension_prompt("su_nghiep", ...)
    assert "🔺" in user or "🔻" in user or "Không có cảnh báo" in user


def test_dimension_prompt_user_contains_format():
    _, user = engine._build_dimension_prompt("su_nghiep", ...)
    assert "## Tổng quan" in user
    assert "## Lời khuyên" in user
    assert "disclaimer" in user.lower() or "tham khảo" in user


def test_dimension_prompt_user_name_none_uses_ban():
    user_profile = UserProfile(name=None, ...)
    _, user_msg = engine._build_dimension_prompt("su_nghiep", user_profile, ...)
    assert "Bạn" in user_msg


def test_dimension_prompt_different_dimensions_have_different_kb():
    sys_sn, _ = engine._build_dimension_prompt("su_nghiep", ...)
    sys_tb, _ = engine._build_dimension_prompt("tien_bac", ...)
    assert sys_sn != sys_tb  # Different dimension KB included
```

- [ ] **Step 3: Implement `_build_dimension_prompt`**

Returns `(system_message: str, user_message: str)` tuple.

System message assembly:
1. Role definition (hardcoded)
2. Non-negotiable rules (hardcoded)
3. Core KB: scoring_rules + alert_interpretation
4. Tone KB: tone_guidelines
5. Dimension KB: from `kb.dimensions[dim]`
6. Filtered star content

User message assembly:
1. User data block
2. 3 score tables (lifetime, decade, monthly)
3. Alerts
4. Example output (if available)
5. Output format instructions

- [ ] **Step 4: Implement `_filter_stars_for_dimension`**

Get stars present in the dimension's primary cungs from LasoData, then filter chinh_tinh.md content to relevant entries.

- [ ] **Step 5: Run tests — all pass**

---

### Task 5: Prompt Builder — Overview

**Files:**
- Modify: `backend/app/services/ai_engine.py`
- Modify: `backend/tests/test_ai_prompt.py`

- [ ] **Step 1: Write failing overview prompt tests**

```python
def test_overview_prompt_has_all_dimension_summaries():
    system, user = engine._build_overview_prompt(...)
    assert "Sự Nghiệp" in user
    assert "Tiền Bạc" in user
    assert "Hôn Nhân" in user
    # ... all 7


def test_overview_prompt_no_dimension_kb():
    system, _ = engine._build_overview_prompt(...)
    # System should have core KB but NOT dimension-specific KB
    assert "Quan Lộc" not in system  # su_nghiep specific content


def test_overview_prompt_output_format():
    _, user = engine._build_overview_prompt(...)
    assert "3-5 câu" in user
    assert "tổng quan" in user.lower()
```

- [ ] **Step 2: Implement `_build_overview_prompt`**

System: role + rules + core KB + tone KB (no dimension KB, no stars).
User: user data + all 7 dimension summaries (label + summary_score + alert counts) + output format.

- [ ] **Step 3: Run tests — all pass**

---

### Task 6: Claude API Caller with Retry

**Files:**
- Modify: `backend/app/services/ai_engine.py`
- Create: `backend/tests/test_ai_engine.py`

- [ ] **Step 1: Write failing API call tests (mocked)**

Create `backend/tests/test_ai_engine.py`:
```python
import pytest
from unittest.mock import AsyncMock, patch, MagicMock


@pytest.mark.asyncio
async def test_generate_dimension_returns_text():
    """Mock Claude API, verify text returned."""
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="## Tổng quan Sự Nghiệp\nLuận giải...")]
    mock_response.usage.input_tokens = 5000
    mock_response.usage.output_tokens = 1200

    engine = AIEngine(kb_dir="backend/knowledge_base", api_key="test-key")
    with patch.object(engine._client.messages, "create", new_callable=AsyncMock, return_value=mock_response):
        result = await engine.generate_dimension("su_nghiep", user, metadata, laso, dim_scores)

    assert "Tổng quan" in result
    assert isinstance(result, str)


@pytest.mark.asyncio
async def test_generate_dimension_retries_on_rate_limit():
    """Verify exponential backoff on rate limit."""
    error = anthropic.RateLimitError(message="rate limited", response=..., body=...)
    success = MagicMock()
    success.content = [MagicMock(text="OK")]
    success.usage.input_tokens = 100
    success.usage.output_tokens = 50

    engine = AIEngine(...)
    with patch.object(engine._client.messages, "create", new_callable=AsyncMock,
                      side_effect=[error, error, success]):
        result = await engine.generate_dimension(...)

    assert result == "OK"


@pytest.mark.asyncio
async def test_generate_dimension_raises_after_max_retries():
    error = anthropic.RateLimitError(...)

    engine = AIEngine(...)
    with patch.object(engine._client.messages, "create", new_callable=AsyncMock,
                      side_effect=[error, error, error]):
        with pytest.raises(anthropic.RateLimitError):
            await engine.generate_dimension(...)
```

- [ ] **Step 2: Implement `generate_dimension`**

```python
async def generate_dimension(self, dimension, user, metadata, laso, dim_scores) -> str:
    system, user_msg = self._build_dimension_prompt(dimension, user, metadata, laso, dim_scores)

    for attempt in range(MAX_RETRIES):
        try:
            response = await self._client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                temperature=0.7,
                system=system,
                messages=[{"role": "user", "content": user_msg}],
            )
            return response.content[0].text
        except RETRYABLE_ERRORS as e:
            if attempt == MAX_RETRIES - 1:
                raise
            await asyncio.sleep(RETRY_DELAYS[attempt])
```

- [ ] **Step 3: Implement `generate_overview`**

Same pattern as `generate_dimension` but uses overview prompt.

- [ ] **Step 4: Run tests — all pass**

---

### Task 7: Generation Orchestrator

**Files:**
- Modify: `backend/app/services/ai_engine.py`
- Modify: `backend/tests/test_ai_engine.py`

- [ ] **Step 1: Write failing orchestration tests**

```python
@pytest.mark.asyncio
async def test_generate_all_returns_7_dimensions_and_overview():
    """All 8 calls succeed."""
    ...
    result = await engine.generate_all(user, metadata, laso, scoring)
    assert len(result.dimensions) == 7
    assert result.overview is not None
    assert result.has_errors is False


@pytest.mark.asyncio
async def test_generate_all_partial_failure():
    """1 dimension fails, 6 + overview succeed."""
    ...
    result = await engine.generate_all(...)
    assert len(result.dimensions) == 6
    assert len(result.errors) == 1
    assert result.has_errors is True


@pytest.mark.asyncio
async def test_generate_all_progress_callback():
    """Progress callback called 8 times."""
    progress_calls = []
    async def on_progress(completed, total):
        progress_calls.append((completed, total))

    result = await engine.generate_all(..., progress_callback=on_progress)
    assert len(progress_calls) == 8
    assert progress_calls[-1] == (8, 8)


@pytest.mark.asyncio
async def test_generate_all_concurrent_execution():
    """Verify calls run concurrently (total time < sum of individual times)."""
    ...
```

- [ ] **Step 2: Implement `generate_all`**

```python
async def generate_all(self, user, metadata, laso, scoring, progress_callback=None):
    DIMS = ["su_nghiep", "tien_bac", "hon_nhan", "suc_khoe", "dat_dai", "hoc_tap", "con_cai"]

    tasks = {"overview": self.generate_overview(user, metadata, scoring)}
    for dim in DIMS:
        tasks[dim] = self.generate_dimension(dim, user, metadata, laso, scoring.dimensions[dim])

    results = await asyncio.gather(*tasks.values(), return_exceptions=True)

    interpretation = InterpretationResult(...)
    completed = 0
    for key, result in zip(tasks.keys(), results):
        completed += 1
        if isinstance(result, Exception):
            interpretation.errors[key] = str(result)
        elif key == "overview":
            interpretation.overview = result
        else:
            interpretation.dimensions[key] = result

        if progress_callback:
            await progress_callback(completed, 8)

    return interpretation
```

- [ ] **Step 3: Run tests — all pass**

---

### Task 8: Output Validation

**Files:**
- Modify: `backend/app/services/ai_engine.py`
- Create: `backend/tests/test_ai_validation.py`

- [ ] **Step 1: Write failing validation tests**

```python
def test_validate_output_clean():
    text = "## Tổng quan...\n---\n*Đây là luận giải tham khảo...*"
    warnings = validate_output(text, "su_nghiep")
    assert warnings == []


def test_validate_output_forbidden_phrase():
    text = "Bạn sẽ gặp họa trong năm 2027..."
    warnings = validate_output(text, "su_nghiep")
    assert any("sẽ gặp họa" in w for w in warnings)


def test_validate_output_no_disclaimer():
    text = "## Tổng quan...\nLuận giải xong."
    warnings = validate_output(text, "su_nghiep")
    assert any("disclaimer" in w.lower() or "tham khảo" in w.lower() for w in warnings)


def test_validate_output_too_short():
    text = "OK."
    warnings = validate_output(text, "su_nghiep")
    assert any("SHORT" in w for w in warnings)
```

- [ ] **Step 2: Implement `validate_output`**

Check for:
- Forbidden phrases ("sẽ gặp họa", "chắc chắn sẽ", "tuyệt đối")
- Disclaimer present (ends with italic text containing "tham khảo")
- Length bounds (200-5000 chars)
- Structure markers (## headings present)

- [ ] **Step 3: Integrate validation into `generate_dimension`**

After getting API response, run validation. Log warnings. Do NOT block — warnings are for monitoring.

- [ ] **Step 4: Run tests — all pass**

---

### Task 9: Integration Test — Full Pipeline

**Files:**
- Create: `backend/tests/test_ai_integration.py`

- [ ] **Step 1: Write full pipeline integration test**

```python
@pytest.mark.asyncio
async def test_full_pipeline_with_mocked_api():
    """
    Load real KB files → build prompts → mock API returns canned response →
    verify InterpretationResult structure.
    """
    engine = AIEngine(kb_dir="backend/knowledge_base", api_key="test")

    # Load fixture
    scoring = load_fixture("sample_scoring.json")
    user = UserProfile(name="Nguyễn Văn A", ...)
    metadata = LasoMetadata(nam="Giáp Tuất", ...)
    laso = load_fixture("sample_laso.json")

    # Mock API to return dimension-specific canned text
    async def mock_create(**kwargs):
        msg = MagicMock()
        msg.content = [MagicMock(text=f"## Tổng quan\nMock luận giải.\n\n---\n*Tham khảo.*")]
        msg.usage.input_tokens = 5000
        msg.usage.output_tokens = 1000
        return msg

    with patch.object(engine._client.messages, "create", side_effect=mock_create):
        result = await engine.generate_all(user, metadata, laso, scoring)

    assert len(result.dimensions) == 7
    assert result.overview is not None
    assert not result.has_errors
    for dim, text in result.dimensions.items():
        assert len(text) > 10
```

- [ ] **Step 2: Write prompt token estimation test**

```python
def test_prompt_token_count_within_budget():
    """Verify prompts don't exceed expected token budget."""
    engine = AIEngine(kb_dir="backend/knowledge_base", api_key="test")
    system, user = engine._build_dimension_prompt("su_nghiep", ...)

    # Rough estimate: 1 token ≈ 4 chars for Vietnamese
    total_chars = len(system) + len(user)
    estimated_tokens = total_chars / 3  # Vietnamese uses ~3 chars/token
    assert estimated_tokens < 10000, f"Prompt too large: ~{estimated_tokens:.0f} tokens"
```

- [ ] **Step 3: Run all tests — everything passes**

---

### Task 10: Wire into FastAPI (Preparation)

**Files:**
- Document integration point for Task 04 (frontend/backend API)

- [ ] **Step 1: Document AIEngine integration**

Add comments to `ai_engine.py` for how router will use it:

```python
# Integration with FastAPI:
#
# In main.py lifespan:
#   engine = AIEngine(kb_dir="backend/knowledge_base", api_key=os.environ["ANTHROPIC_API_KEY"])
#   app.state.ai_engine = engine
#
# In router:
#   engine = request.app.state.ai_engine
#   result = await engine.generate_all(user, metadata, laso, scoring, progress_callback)
#   # Store result in SQLite
#   # Update profile status to "completed"
```

- [ ] **Step 2: Verify all tests pass together**

Run full test suite:
```bash
cd backend && python -m pytest tests/test_ai_*.py -v
```

- [ ] **Step 3: Document what needs expert input**

Create `backend/knowledge_base/TODO_EXPERT.md`:
- List all KB files that are using mock content
- What specifically needs expert review
- How to replace mock content with real expert data
- Link to `data/mock_expert_input/` for reference

---

## Dependency Notes

- **Task 01 (Scraper):** Need `LasoData` dataclass from schemas.py. If not yet implemented, create minimal version in schemas.py with same structure.
- **Task 02 (Scoring):** Need `ScoringResult`, `DimensionScores`, `ScorePoint`, `Alert` from schemas.py. Same — use from shared schemas or create compatible fixtures.
- **anthropic SDK:** `pip install anthropic` — async client used throughout.
- **pytest-asyncio:** `pip install pytest-asyncio` — for async test functions.

## Definition of Done

All of the following must be true:
1. `backend/knowledge_base/` has all required files (3 core + 7 dimensions + 2 stars + examples)
2. `AIEngine` loads KB at init, builds correct prompts, handles retries
3. `generate_all()` runs 8 concurrent calls, handles partial failures
4. Output validation checks for forbidden phrases and disclaimer
5. All tests pass: `pytest tests/test_ai_*.py` — 100% green
6. Prompt token count within budget (~5-8K input per call)
7. `TODO_EXPERT.md` documents what needs real expert content
