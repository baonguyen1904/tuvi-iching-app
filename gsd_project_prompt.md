# Kinh Dịch × Tử Vi — AI Luận Giải MVP

---

## WHAT WE'RE BUILDING

A web app that takes a user's birth data (ngày giờ sinh), generates a Vietnamese Tử Vi (astrology) chart with scores across life dimensions, and uses an AI agent (Claude) to produce personalized narrative interpretations ("luận giải") for each dimension.

**One-sentence:** User nhập ngày giờ sinh → Hệ thống tính lá số + scores → AI sinh luận giải cá nhân hóa cho từng lĩnh vực → User đọc trên web.

**This is an MVP.** We're building the minimum to test with ~20-50 existing clients of our expert partner. Not a full product launch.

---

## CONTEXT DOCUMENTS (Agent nên đọc để hiểu sâu hơn)

The following files trong project chứa research và specs chi tiết hơn. **Hãy đọc chúng trước khi hỏi questions:**

- `docs/research_plan_kinh_dich_tu_vi_app.md` — Market research, competitive landscape, persona hypotheses, monetization analysis, technical architecture concepts
- `docs/mvp_scope_ai_agent_plan.md` — MVP scope definition, user flow, AI agent architecture, knowledge base structure, prompt templates, development plan (2-4 weeks)
- `docs/discovery_framework_v1.md` — User research framework (JTBD interviews, validation methodology) — this is the FUTURE validation plan, not yet executed

**Quan trọng:** The discovery framework has NOT been executed yet. All personas and positioning in the research plan are HYPOTHESES. This MVP exists to generate evidence before full validation.

---

## BUSINESS LOGIC DOMAINS

### Domain 1: Data Pipeline — Lá Số Generation

**What it does:** Given birth data, produce a complete Tử Vi chart (lá số).

**Business rules:**
- Input: Ngày sinh (dương lịch), giờ sinh (1 of 12 canh giờ, or "không rõ"), giới tính (Nam/Nữ), tên (optional)
- Dương lịch → Âm lịch conversion is required (the Tử Vi system uses lunar calendar)
- The system must determine: Cung Mệnh, 12 cung positions, and placement of all major (chính tinh) and minor (phụ tinh) stars
- **Current approach:** Scrape tuvi.cohoc.net/lap-la-so-tu-vi.html by POSTing birth data → parse returned HTML to extract 12 cung × sao placements
- **Fallback concern:** If cohoc.net changes HTML structure or blocks requests, we need graceful error handling. Consider caching results.
- Output: Structured data representing the full lá số (12 cung, mỗi cung có list of sao)

### Domain 2: Scoring Engine — Quantifying the Chart

**What it does:** Transform raw lá số data into numerical scores across dimensions and time periods.

**Business rules:**
- Each sao (star) has predefined point values per dimension (sự nghiệp, tiền bạc, hôn nhân, sức khỏe, đất đai, học tập, con cái)
- Points are categorized as: Dương (positive energy), Âm (negative energy), TB (neutral/average)
- Scores are calculated for multiple time horizons: cả đời (lifetime, mốc 10 năm), 10 năm (decade, mốc từng năm), 12 tháng (monthly)
- **Alert system:** When certain sao combinations align at specific time periods, alerts trigger:
  - 🔺 = Positive alert (opportunity, breakthrough)
  - 🔻 = Negative alert (risk, caution needed)
  - Each alert has a tag text describing the nature (e.g., "có bước thăng tiến", "cẩn thận tiểu nhân")
- **Current implementation:** Google Sheet with lookup tables (laso_points). Must be ported to code.
- The scoring logic is the EXISTING working engine — it's been validated by the expert over many readings.
- Output: Per-dimension score arrays + triggered alerts

### Domain 3: Knowledge Base — Expert Interpretation Rules

**What it does:** Provide the AI agent with domain-specific interpretation rules so it can generate accurate, expert-level luận giải.

**Business rules:**
- KB is organized per dimension (7 files: sự nghiệp, tiền bạc, hôn nhân, sức khỏe, đất đai, học tập, con cái)
- Plus core files: scoring_rules.md, alert_interpretation.md, tone_guidelines.md
- Plus star reference files: chính tinh (14 major stars), phụ tinh (minor stars)
- KB content includes:
  - How to read score patterns (high Dương, low Âm, crossover points)
  - What each alert means in context (which sao cause it, what it implies)
  - Age-appropriate interpretation guidance (20-30, 30-45, 45-60, 60+)
  - Example luận giải that expert has approved
- **KB is NOT a database** — it's markdown files injected into the AI prompt as context
- Total KB size per dimension call: ~5-10K tokens (fits within Claude's context window, no RAG needed)
- **Critical dependency:** Expert must review and annotate KB files. Planned: 3 sessions × ~1.5-2h each.
- Output: Markdown files ready to be injected into AI prompts

### Domain 4: AI Luận Giải Engine — Narrative Generation

**What it does:** Given scoring data + KB context + user birth data, generate a personalized narrative interpretation.

**Business rules:**
- One API call per dimension (not all dimensions at once)
- Prompt structure: System prompt (role + rules) + KB (dimension-specific) + User data + Score data + Alerts
- **Tone rules (non-negotiable):**
  - Ngôn ngữ tích cực, empowering — KHÔNG gieo sợ hãi
  - Mỗi cảnh báo 🔻 PHẢI đi kèm lời khuyên cụ thể
  - Dùng "cần thận trọng" thay vì "sẽ gặp họa"
  - KHÔNG bịa đặt — chỉ nói về những gì data cho thấy
  - Kết thúc bằng disclaimer
- Output structure per dimension:
  1. Tổng quan (3-5 câu overview based on lifetime pattern)
  2. Phân tích giai đoạn hiện tại (current decade analysis)
  3. Các mốc cần chú ý (expand each alert with context + advice)
  4. Lời khuyên tổng thể (2-3 actionable recommendations)
  5. Disclaimer
- Also generate: Tổng quan vận mệnh (a 3-5 sentence overview across ALL dimensions, shown on result page before user picks a dimension)
- Streaming: AI response should be streamed to frontend for better UX
- Output: Structured Vietnamese text, ~1-2 pages per dimension

### Domain 5: Chart Visualization

**What it does:** Render score data as visual charts on the web.

**Business rules:**
- Two chart types per dimension:
  - Cả đời (lifetime): X-axis = age ranges (10-year blocks), Y-axis = score, lines for Dương/Âm/TB
  - 10 năm (decade): X-axis = individual years, Y-axis = score, lines for Dương/Âm/TB
- Overview chart on result page: Summary visualization across all dimensions
- Alert markers should be visible on charts (🔺🔻 at relevant time points)
- Charts are rendered client-side from score data JSON
- Must be mobile-responsive

### Domain 6: User Flow & Web Interface

**What it does:** The web application tying everything together.

**User flow:**
1. Landing page → CTA "Bắt đầu"
2. Input form: Ngày sinh (date picker), Giờ sinh (dropdown 12 canh), Giới tính (Nam/Nữ), Họ tên (optional)
3. Processing screen (5-10 giây): "Đang lấy lá số..." → "Đang phân tích..." → "Đang tạo luận giải..."
4. Result page: Header (tên, birth info) + Overview chart + AI summary + 7 dimension buttons
5. Dimension detail page: Dimension-specific charts + Streamed AI luận giải text
6. Each result has a shareable URL (no login required)

**NOT in MVP:** Login/accounts, payment, chatbot, Kinh Dịch gieo quẻ, PDF export, push notifications, multi-dimension comparison

---

## KEY TECHNICAL DECISIONS (already made)

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Frontend | Next.js | SSR cho SEO, React ecosystem |
| Backend | Python FastAPI | Scraper + scoring logic already in Python-like pseudocode |
| AI Model | Claude Sonnet API | Vietnamese quality tốt, 200K context, structured prompts |
| AI approach | Structured prompt + inline KB | No RAG needed — KB fits in context window |
| Database | SQLite or Supabase | MVP only needs caching |
| Charts | Chart.js hoặc Recharts | Standard, well-documented |
| Deploy | Vercel (frontend) + Railway (backend) | Fast deployment |
| Auth | None for MVP | Reduce friction, shareable links instead |

---

## WHAT SUCCESS LOOKS LIKE (MVP test metrics)

- **Completion rate** > 80% (users who start → see result)
- **Dimension click-through** > 60% (users who view at least 1 detailed dimension)
- **Time on dimension page** > 2 minutes
- **Expert accuracy rating** > 7/10 (expert reviews 10 AI outputs)
- **User feedback** > 50% positive (simple survey)
- **Share rate** > 10%

---

## CRITICAL RISKS

1. **Scraper dependency** — cohoc.net could change or block. Need caching + error handling.
2. **AI hallucination** — Must be constrained to provided data only. Expert review cycle required.
3. **Scoring port accuracy** — Google Sheet logic → Python must be validated with 20+ test cases.
4. **Expert time** — Only ~5 hours total available. Must be pre-prepared and efficient.
5. **AI text too generic** — KB quality + few-shot examples in prompt are the fix.

---

## CONSTRAINTS

- **Timeline:** 2-4 weeks
- **Team:** 1 developer (using Claude Code + GSD), 1 domain expert (limited availability ~5h)
- **Budget:** Minimal — use free/cheap infrastructure
- **Test group:** ~20-50 existing clients of the expert
- **Language:** Vietnamese only for MVP (bilingual later)

---

## PHASE SUGGESTION (for GSD roadmap)

This is a suggestion — GSD should refine based on research:

1. **Data Pipeline** — Scraper + lá số parser (cohoc.net → structured data)
2. **Scoring Engine** — Port Google Sheet scoring logic to Python, validate with test cases
3. **Knowledge Base** — Write KB skeleton, expert review sessions, approved examples
4. **AI Agent** — Prompt engineering, generation pipeline, streaming, quality iteration
5. **Frontend — Input & Processing** — Landing page, birth data form, processing states
6. **Frontend — Results & Charts** — Result page, chart rendering, dimension detail pages
7. **Integration & Testing** — End-to-end flow, 10+ test cases, expert review of AI outputs
8. **Deploy & Soft Launch** — Production deploy, send to test group, collect feedback

---


## Cấu trúc spec:
/
├── CLAUDE.md                 ← Claude Code đọc đầu tiên, mọi session
├── docs/
│   ├── SPEC.md               ← Product spec (what & why)
│   ├── ARCHITECTURE.md       ← Tech decisions (đã quyết, không debate lại)
│   └── DECISIONS.md          ← Decision log (ADR format)
├── tasks/
│   ├── 01_scraper.md         ← Task cụ thể, có acceptance criteria
│   ├── 02_scoring_engine.md
│   ├── 03_ai_pipeline.md
│   └── 04_frontend.md
└── tests/
    ├── fixtures/             ← Test cases (input → expected output)
    └── EXPECTED_OUTPUTS.md   ← Human-readable expectations


## OPEN QUESTIONS (for GSD to explore)

1. Should the scraper be a separate microservice or inline in the FastAPI app?
2. What's the best way to handle "giờ sinh không rõ" (unknown birth time) — skip time-dependent calculations or use a default?
3. How to structure the overview summary generation — separate AI call or part of the first dimension call?
4. Should we pre-generate all 7 dimension luận giải on submit, or generate on-demand when user clicks?
5. What caching strategy for lá số data (same birth data = same chart, no need to re-scrape)?
6. How to handle the edge case where cohoc.net is down during a user session?