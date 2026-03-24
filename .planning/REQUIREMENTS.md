# Requirements: Kinh Dịch × Tử Vi — AI Luận Giải MVP

**Defined:** 2026-03-24
**Core Value:** Users receive personalized, expert-quality AI narrative interpretations of their Tử Vi chart across 7 life dimensions, grounded in real scoring data.

## v1 Requirements

### Data Pipeline

- [ ] **DATA-01**: Scrape tuvi.cohoc.net with birth data → parse lá số cả đời + vận 10 năm (12 cung × sao placements)
- [ ] **DATA-02**: Scrape tuvi.vn with birth data → parse lá số 12 tháng (12 cung × sao placements)
- [ ] **DATA-03**: Port existing Selenium scrapers from legacy codebase (`/mnt/d/Working/TBTesu/tuvi/scraper/`) to new project
- [ ] **DATA-04**: Cache lá số results — same birth data returns cached result without re-scraping

### Scoring Engine

- [ ] **SCORE-01**: Port Google Sheet scoring logic (laso_points lookup tables) to Python
- [ ] **SCORE-02**: Calculate per-dimension scores (Dương/Âm/TB) across all time periods (cả đời, 10 năm, 12 tháng)
- [ ] **SCORE-03**: Alert system — detect sao combinations and trigger 🔺 (positive) / 🔻 (negative) alerts with tag text

### Knowledge Base

- [ ] **KB-01**: Create 7 dimension KB markdown files (sự nghiệp, tiền bạc, hôn nhân, sức khỏe, đất đai, học tập, con cái)
- [ ] **KB-02**: Create core rules files (scoring_rules.md, alert_interpretation.md, tone_guidelines.md)

### AI Luận Giải

- [ ] **AI-01**: Per-dimension AI call — Claude Sonnet with structured prompt + KB context + score data → personalized narrative
- [ ] **AI-02**: Tổng quan vận mệnh — AI summary (3-5 câu) across all dimensions, shown on result page

### Chart Visualization

- [ ] **CHART-01**: Lifetime chart per dimension — X=age ranges (10-year blocks), Y=score, lines for Dương/Âm/TB
- [ ] **CHART-02**: Decade chart per dimension — X=individual years, Y=score, lines for Dương/Âm/TB
- [ ] **CHART-03**: Alert markers visible on charts (🔺🔻 at relevant time points)

### Web Interface

- [ ] **WEB-01**: Landing page with CTA "Bắt đầu"
- [ ] **WEB-02**: Input form — ngày sinh (date picker), giờ sinh (dropdown 12 canh hoặc "không rõ"), giới tính (Nam/Nữ), họ tên (optional)
- [ ] **WEB-03**: Processing screen with progress states ("Đang lấy lá số...", "Đang phân tích...", "Đang tạo luận giải...")
- [ ] **WEB-04**: Result page — header (tên, birth info) + tổng quan vận mệnh + 7 dimension buttons
- [ ] **WEB-05**: Dimension detail page — dimension-specific charts + AI luận giải text
- [ ] **WEB-06**: Mobile responsive design

## v2 Requirements

### Enhanced Data Pipeline

- **DATA-05**: Self-hosted tử vi calculation engine (eliminate scraper dependency)
- **DATA-06**: Graceful error handling when scraper sources are down

### Enhanced AI

- **AI-03**: Streaming AI response to frontend for better UX
- **AI-04**: Star reference files (chính tinh + phụ tinh) in KB for richer interpretation
- **AI-05**: Expert-approved few-shot examples in prompts

### Enhanced Web

- **WEB-07**: Shareable URL per result (no login required)
- **WEB-08**: Overview chart — summary visualization across all dimensions

### Social & Accounts

- **SOCL-01**: User accounts / login for saved results
- **SOCL-02**: Chatbot hỏi đáp follow-up

### Export

- **EXPO-01**: PDF/PPTX export of results

## Out of Scope

| Feature | Reason |
|---------|--------|
| Kinh Dịch gieo quẻ | Separate module, not part of Tử Vi MVP |
| Payment / premium tiers | MVP is free for test group (~20-50 people) |
| Push notifications | No user accounts in MVP |
| Multi-dimension comparison charts | Nice-to-have, not core to MVP validation |
| RAG pipeline | KB fits in context window (~5-10K tokens per dimension) |
| Bilingual (English) | Vietnamese only for MVP |
| OAuth / social login | No auth at all in MVP |
| Mobile app (React Native/Flutter) | Web-first for MVP |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| DATA-01 | — | Pending |
| DATA-02 | — | Pending |
| DATA-03 | — | Pending |
| DATA-04 | — | Pending |
| SCORE-01 | — | Pending |
| SCORE-02 | — | Pending |
| SCORE-03 | — | Pending |
| KB-01 | — | Pending |
| KB-02 | — | Pending |
| AI-01 | — | Pending |
| AI-02 | — | Pending |
| CHART-01 | — | Pending |
| CHART-02 | — | Pending |
| CHART-03 | — | Pending |
| WEB-01 | — | Pending |
| WEB-02 | — | Pending |
| WEB-03 | — | Pending |
| WEB-04 | — | Pending |
| WEB-05 | — | Pending |
| WEB-06 | — | Pending |

**Coverage:**
- v1 requirements: 20 total
- Mapped to phases: 0
- Unmapped: 20 ⚠️

---
*Requirements defined: 2026-03-24*
*Last updated: 2026-03-24 after initial definition*
