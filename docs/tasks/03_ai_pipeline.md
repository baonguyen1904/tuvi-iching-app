# Task 03: AI Luận Giải Pipeline
## Scores + KB → Personalized Narrative via Claude

**Priority:** Must — core value proposition
**Estimated effort:** 3-5 days (including KB writing + prompt iteration)
**Dependencies:** Task 02 (ScoringResult), Expert sessions (KB content)
**Output:** Python module `services/ai_engine.py` + KB markdown files
**Spec file** `docs/superpowers/specs/2026-03-27-ai-pipeline-design.md`
**Plan file** `docs/superpowers/plans/2026-03-27-ai-pipeline-implementation.md`
**Mock expert data** `data/mock_expert_input/` (chờ expert điền thực tế)

---

## What to Build

1. Knowledge Base files (markdown) — expert-informed interpretation rules
2. Prompt builder — assembles system prompt + KB + user data + scores
3. AI caller — async Claude Sonnet API calls with streaming
4. Generation orchestrator — runs 8 parallel calls (overview + 7 dimensions)

---

## 1. Knowledge Base Files

### Directory: `backend/knowledge_base/`

**Core files (write first, dimension-agnostic):**

```markdown
# core/scoring_rules.md (~500 words)
Explains: What Dương/Âm/TB scores mean, how to read patterns,
what high/low values indicate, how crossover points work.

# core/alert_interpretation.md (~300 words)  
Explains: What 🔺🔻 alerts represent, when they trigger,
how to interpret alert tags in context of surrounding scores.

# core/tone_guidelines.md (~300 words)
Rules: Empowering tone, always pair warnings with advice,
"cần thận trọng" NOT "sẽ gặp họa", no fear-mongering,
data-grounded only, end with disclaimer.
```

**Dimension files (7 files, ~500-1000 words each):**

Each dimension file contains:
- Related cung (primary + secondary)
- How to read score patterns for this dimension specifically
- Alert meanings specific to this dimension
- Age-appropriate interpretation guidance
- Example good luận giải excerpts (from expert)

**Star files (reference):**
- `stars/chinh_tinh.md` — 14 major stars, their meanings, positive/negative aspects
- `stars/phu_tinh.md` — Minor stars, significance when they trigger alerts

**Example outputs (from expert):**
- `examples/approved_outputs/` — 2-3 expert-approved sample luận giải
- These are used as few-shot examples in the prompt

### KB Content Process

```
Step 1: Developer writes skeleton from existing docs + star/cung knowledge
Step 2: Expert reviews form responses → developer integrates into KB files
Step 3: Test AI output with KB → Expert reviews → iterate KB
```

---

## 2. Prompt Structure

### System Prompt (per dimension call)

```
[ROLE DEFINITION]
Bạn là tư vấn viên luận giải tử vi chuyên nghiệp...

[RULES — NON-NEGOTIABLE]
1. Chỉ nói về data được cung cấp — KHÔNG bịa đặt
2. Ngôn ngữ tích cực, empowering
3. Mỗi cảnh báo 🔻 PHẢI đi kèm lời khuyên cụ thể
4. Dùng "cần thận trọng" thay vì "sẽ gặp họa"
5. Kết thúc bằng disclaimer
6. Viết tiếng Việt tự nhiên, không quá trang trọng

[KNOWLEDGE BASE — CORE]
{content of core/scoring_rules.md}
{content of core/alert_interpretation.md}

[KNOWLEDGE BASE — DIMENSION: {dimension_name}]
{content of dimensions/{dimension}.md}

[RELEVANT STARS]
{content of stars/chinh_tinh.md — filtered to relevant stars only}

[USER DATA]
- Tên: {name or "Bạn"}
- Sinh: {birth_date} ({lunar_info}), Giờ {birth_hour}, {gender}
- Tuổi hiện tại: {current_age}
- Cung Mệnh: {cung_menh} — {ngu_hanh}
- Cung {relevant_cung}: Sao: {stars_in_relevant_cung}

[SCORE DATA — {dimension_name}]
### Cả đời (mốc 10 năm):
| Giai đoạn | Dương | Âm | TB |
{lifetime_scores_table}

### 10 năm hiện tại ({decade_range}):
| Năm | Dương | Âm | TB |
{decade_scores_table}

### 12 tháng ({current_year}):
| Tháng | Dương | Âm | TB |
{monthly_scores_table}

[ALERTS — {dimension_name}]
{formatted alerts with 🔺🔻 + period + tag}

[EXAMPLE OUTPUT] (few-shot)
{content of approved example luận giải — 1 example}

[OUTPUT FORMAT]
Viết luận giải tiếng Việt theo format sau:

## Tổng quan {dimension_label}
(3-5 câu nhận xét tổng thể dựa trên pattern cả đời)

## Giai đoạn hiện tại ({decade_range})
(Phân tích 10 năm hiện tại, xu hướng Dương/Âm)

## Các mốc cần chú ý
(Mỗi alert: giải thích tại sao + nên làm gì / tránh gì)

## Lời khuyên
(2-3 điều cụ thể, actionable)

---
*Đây là luận giải tham khảo dựa trên Tử Vi Đẩu Số. Mọi quyết định cuối cùng là của bạn.*
```

### Overview Prompt (separate call)

```
[ROLE + RULES — same as above]

[ALL DIMENSION SUMMARIES]
- Sự nghiệp: score {X}, {Y} alerts
- Tiền bạc: score {X}, {Y} alerts
... (7 dimensions)

[USER DATA — same]

[OUTPUT FORMAT]
Viết tổng quan vận mệnh trong 3-5 câu. Nhận xét bức tranh lớn:
xu hướng tổng thể, lĩnh vực mạnh nhất, lĩnh vực cần chú ý nhất.
Ngắn gọn, súc tích, gợi mở để user muốn xem chi tiết.
```

---

## 3. Implementation

### ai_engine.py

```python
class AIEngine:
    def __init__(self, kb_dir: str, api_key: str):
        self.kb = self._load_kb(kb_dir)
        self.client = anthropic.AsyncAnthropic(api_key=api_key)
    
    def _load_kb(self, kb_dir: str) -> dict:
        """Load all KB markdown files into memory at startup."""
        ...
    
    def _build_dimension_prompt(
        self, 
        dimension: str,
        user_data: dict,
        scores: DimensionScores,
        laso: LasoData
    ) -> list[dict]:
        """Build messages array for a single dimension call."""
        ...
    
    def _build_overview_prompt(
        self,
        user_data: dict,
        all_scores: dict[str, DimensionScores]
    ) -> list[dict]:
        """Build messages array for overview call."""
        ...
    
    async def generate_dimension(
        self,
        dimension: str,
        user_data: dict,
        scores: DimensionScores,
        laso: LasoData
    ) -> str:
        """Generate luận giải for a single dimension."""
        messages = self._build_dimension_prompt(dimension, user_data, scores, laso)
        response = await self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            temperature=0.7,
            messages=messages
        )
        return response.content[0].text
    
    async def generate_all(
        self,
        user_data: dict,
        scoring_result: ScoringResult,
        laso: LasoData,
        progress_callback: Callable | None = None
    ) -> dict:
        """Generate overview + all 7 dimensions concurrently."""
        
        tasks = []
        # Overview
        tasks.append(self._generate_overview(user_data, scoring_result))
        # 7 dimensions
        for dim_key, dim_scores in scoring_result.dimensions.items():
            tasks.append(self.generate_dimension(dim_key, user_data, dim_scores, laso))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle partial failures
        interpretations = {}
        for i, (key, result) in enumerate(zip(["overview"] + list(scoring_result.dimensions.keys()), results)):
            if isinstance(result, Exception):
                interpretations[key] = f"Luận giải đang được xử lý, vui lòng thử lại sau.\n\n*Lỗi: {type(result).__name__}*"
            else:
                interpretations[key] = result
            
            if progress_callback:
                await progress_callback(i + 1, len(tasks))
        
        return interpretations
```

### Claude API Configuration

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| model | claude-sonnet-4-20250514 | Best balance of quality, speed, cost |
| max_tokens | 2000 | ~500-1000 words per dimension |
| temperature | 0.7 | Creative enough for natural text, not too random |
| system | (empty — role in user message) | Some models prefer role in first message |

### Cost per Profile

```
Per dimension call:
  Input:  ~5-8K tokens (system + KB + data)
  Output: ~800-1500 tokens
  Cost:   ~$0.005-0.01

Per profile (8 calls):
  Total:  ~$0.04-0.08

For 50 test users: ~$2-4
```

---

## 4. Quality Iteration Process

### Step 1: First draft prompts
- Write prompts with skeleton KB
- Generate 3 test outputs
- Review: Is the structure correct? Is the tone right?

### Step 2: Expert review
- Show expert 3 AI outputs alongside real lá số data
- Get feedback: What's accurate? What's wrong? What's missing?
- Integrate feedback into KB files + prompt rules

### Step 3: Iterate
- Regenerate with improved KB
- Expert reviews again
- Target: ≥ 7/10 rating from expert on 10 samples

---

## Acceptance Criteria

- [ ] KB files exist for all 7 dimensions + 3 core files
- [ ] Prompt builder produces valid Claude API messages
- [ ] Single dimension generation returns Vietnamese markdown text (~500-1000 words)
- [ ] Overview generation returns 3-5 sentence summary
- [ ] All 8 calls run concurrently in < 30 seconds
- [ ] Partial failure handling: if 1 dimension fails, others still return
- [ ] Progress callback works (for processing screen updates)
- [ ] Tone compliance: no fear-mongering, always pairs warnings with advice
- [ ] Every output ends with disclaimer
- [ ] Expert reviews 5+ outputs and rates ≥ 7/10 average

---

## Edge Cases

- Claude API rate limit → implement retry with exponential backoff (max 3 retries)
- Claude API timeout → 60 second timeout per call, return error message for that dimension
- Very few alerts for a dimension → AI should still generate meaningful content from scores alone
- Very many alerts (>5) for a dimension → AI should prioritize most important, not list all equally
- User name is None → use "Bạn" in text
- Very young person (born 2005+) → less content for lifetime analysis, focus on near-term
- Very old person (born 1930s) → historical analysis, focus on current decade