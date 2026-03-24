# Roadmap: Kinh Dịch × Tử Vi — AI Luận Giải MVP

## Overview

Three phases that mirror the app's data flow: first build the pipeline that extracts and scores lá số data from scraping sources; then build the intelligence layer that converts raw scores into expert-quality AI narratives; then deliver the full web experience that surfaces everything to users. Each phase can be verified independently before the next begins.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Data Pipeline & Scoring Engine** - Backend foundation: scrape lá số, port scoring logic, cache results
- [ ] **Phase 2: Knowledge Base & AI Luận Giải** - Intelligence layer: KB markdown files + Claude narrative generation per dimension
- [ ] **Phase 3: Charts & Web Interface** - User-facing product: visualization charts, all web pages, mobile responsive

## Phase Details

### Phase 1: Data Pipeline & Scoring Engine
**Goal**: Given any birth data input, the system can produce scored Tử Vi data across all dimensions and time periods
**Depends on**: Nothing (first phase)
**Requirements**: DATA-01, DATA-02, DATA-03, DATA-04, SCORE-01, SCORE-02, SCORE-03
**Success Criteria** (what must be TRUE):
  1. Providing valid birth data returns a parsed lá số with 12 cung × sao placements from cohoc.net
  2. Providing valid birth data also returns monthly sao placements from tuvi.vn
  3. The same birth data requested a second time returns a cached result without re-scraping
  4. Per-dimension scores (Dương/Âm/TB) are computed across all time periods (cả đời, 10 năm, 12 tháng)
  5. Sao combination alerts (🔺 positive / 🔻 negative) are detected and returned with tag text
**Plans**: 5 plans

Plans:
- [ ] 01-01-PLAN.md — Scaffold backend project, port schemas/constants/soup_utils (Wave 1)
- [ ] 01-02-PLAN.md — Export laso_points.xlsx to JSON + implement scoring engine (Wave 2)
- [ ] 01-03-PLAN.md — Port cohoc.net Selenium scraper + HTML parsing tests (Wave 2)
- [ ] 01-04-PLAN.md — Port tuvi.vn Selenium scraper + HTML parsing tests (Wave 2)
- [ ] 01-05-PLAN.md — Supabase cache module + FastAPI /api/la-so endpoint (Wave 3)

### Phase 2: Knowledge Base & AI Luận Giải
**Goal**: Given scored lá số data, the system generates expert-quality Vietnamese narrative interpretations for each of the 7 life dimensions
**Depends on**: Phase 1
**Requirements**: KB-01, KB-02, AI-01, AI-02
**Success Criteria** (what must be TRUE):
  1. All 7 dimension KB markdown files exist (sự nghiệp, tiền bạc, hôn nhân, sức khỏe, đất đai, học tập, con cái) with expert-reviewed content
  2. Core rules files exist (scoring_rules.md, alert_interpretation.md, tone_guidelines.md)
  3. A per-dimension AI call returns a structured narrative (Tổng quan → Phân tích giai đoạn → Mốc cần chú ý → Lời khuyên → Disclaimer)
  4. AI output uses empowering tone: every 🔻 alert is accompanied by advice, no fear-inducing language
  5. A 3-5 sentence Tổng quan vận mệnh summary across all 7 dimensions is generated
**Plans**: TBD

### Phase 3: Charts & Web Interface
**Goal**: Users can access the full Tử Vi experience through a web app — entering birth data, seeing charts, and reading AI narratives — on any device
**Depends on**: Phase 2
**Requirements**: CHART-01, CHART-02, CHART-03, WEB-01, WEB-02, WEB-03, WEB-04, WEB-05, WEB-06
**Success Criteria** (what must be TRUE):
  1. A user can open the landing page, fill the input form (ngày sinh, giờ sinh, giới tính, tên), and reach a result page
  2. The result page shows a Tổng quan vận mệnh summary and 7 clickable dimension buttons
  3. Each dimension detail page shows both a lifetime chart and a decade chart with Dương/Âm/TB lines and alert markers
  4. The processing screen shows meaningful progress states ("Đang lấy lá số...", "Đang phân tích...", "Đang tạo luận giải...")
  5. The entire experience is usable on a mobile device without horizontal scrolling
**Plans**: TBD
**UI hint**: yes

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Data Pipeline & Scoring Engine | 0/5 | Not started | - |
| 2. Knowledge Base & AI Luận Giải | 0/? | Not started | - |
| 3. Charts & Web Interface | 0/? | Not started | - |
