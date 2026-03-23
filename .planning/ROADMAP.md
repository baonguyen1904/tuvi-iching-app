# Roadmap: Kinh Dich x Tu Vi — AI Luan Giai MVP

**Milestone:** M1 — MVP
**Granularity:** Coarse
**Coverage:** 36/36 requirements mapped
**Created:** 2026-03-23

---

## Phases

- [ ] **Phase 1: Foundation and Data Pipeline** — Project skeleton, input form, scraper, calendar conversion, caching, and error handling
- [ ] **Phase 2: Scoring Engine and Knowledge Base** — Port scoring logic from Google Sheets, alert detection, and author all AI grounding KB files with expert
- [ ] **Phase 3: AI Engine, Charts, and Full UI** — AI luan giai generation with streaming, score visualization charts, and complete user-facing result flow

---

## Phase Details

### Phase 1: Foundation and Data Pipeline
**Goal**: Users can submit birth data and the system produces a validated la so — the foundation everything else is built on
**Depends on**: Nothing (first phase)
**Requirements**: DINP-01, DINP-02, DINP-03, DINP-04, DINP-05, PIPE-01, PIPE-02, PIPE-03, PIPE-04, PIPE-05
**Success Criteria** (what must be TRUE):
  1. User can fill in the birth data form (date, time, gender, name) and submit it
  2. System correctly converts solar calendar input to lunar calendar, including intercalary months
  3. System produces a complete la so with all 14 chinh tinh and phu tinh placed across 12 cung
  4. Submitting the same birth data twice does not re-scrape — result is returned from cache
  5. When cohoc.net is unavailable, user sees a Vietnamese error message with a retry option
**Plans**: TBD
**UI hint**: yes

### Phase 2: Scoring Engine and Knowledge Base
**Goal**: The system can calculate authoritative Duong/Am/TB scores and detect alert combinations per dimension, and the AI grounding knowledge base is ready
**Depends on**: Phase 1
**Requirements**: SCOR-01, SCOR-02, SCOR-03, SCOR-04, KBAS-01, KBAS-02, KBAS-03, KBAS-04
**Success Criteria** (what must be TRUE):
  1. Scoring engine produces Duong, Am, and TB scores for all 7 dimensions across all 3 time horizons (ca doi, 10 nam, 12 thang)
  2. Alert detection identifies positive and negative sao combinations and tags them correctly
  3. Scoring output matches the expert's validated Google Sheets for 20+ known la so test cases
  4. All 7 dimension KB files, core reference files, and star reference files exist, are expert-reviewed, and fit within the ~5-10K token inline injection limit
**Plans**: TBD

### Phase 3: AI Engine, Charts, and Full UI
**Goal**: Users receive a complete, personalized Tu Vi reading — streaming AI narrative per dimension, score charts with alert markers, and shareable result pages
**Depends on**: Phase 2
**Requirements**: AILG-01, AILG-02, AILG-03, AILG-04, AILG-05, AILG-06, CHRT-01, CHRT-02, CHRT-03, CHRT-04, CHRT-05, UIUX-01, UIUX-02, UIUX-03, UIUX-04, UIUX-05, UIUX-06, UIUX-07
**Success Criteria** (what must be TRUE):
  1. After submitting birth data, user sees a processing screen with progress steps and then arrives at a result page showing a tong quan van menh overview summary
  2. User can click any of the 7 dimension buttons and receive a streaming, personalized AI luan giai narrative — generated on-demand, not all at once
  3. AI narrative only references stars actually present in the user's chart and uses empowering, non-fear-inducing language with actionable advice on every negative alert
  4. Result page displays Duong/Am/TB score line charts per dimension for ca doi and 10 nam horizons, with alert markers visible at relevant time points
  5. User can share their result URL with someone else who can open it and view the full reading — no login required
  6. All pages render correctly on mobile and the entire interface is in Vietnamese
**Plans**: TBD
**UI hint**: yes

---

## Progress Table

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation and Data Pipeline | 0/0 | Not started | - |
| 2. Scoring Engine and Knowledge Base | 0/0 | Not started | - |
| 3. AI Engine, Charts, and Full UI | 0/0 | Not started | - |

---

## Coverage Map

| Requirement | Phase | Status |
|-------------|-------|--------|
| DINP-01 | Phase 1 | Pending |
| DINP-02 | Phase 1 | Pending |
| DINP-03 | Phase 1 | Pending |
| DINP-04 | Phase 1 | Pending |
| DINP-05 | Phase 1 | Pending |
| PIPE-01 | Phase 1 | Pending |
| PIPE-02 | Phase 1 | Pending |
| PIPE-03 | Phase 1 | Pending |
| PIPE-04 | Phase 1 | Pending |
| PIPE-05 | Phase 1 | Pending |
| SCOR-01 | Phase 2 | Pending |
| SCOR-02 | Phase 2 | Pending |
| SCOR-03 | Phase 2 | Pending |
| SCOR-04 | Phase 2 | Pending |
| KBAS-01 | Phase 2 | Pending |
| KBAS-02 | Phase 2 | Pending |
| KBAS-03 | Phase 2 | Pending |
| KBAS-04 | Phase 2 | Pending |
| AILG-01 | Phase 3 | Pending |
| AILG-02 | Phase 3 | Pending |
| AILG-03 | Phase 3 | Pending |
| AILG-04 | Phase 3 | Pending |
| AILG-05 | Phase 3 | Pending |
| AILG-06 | Phase 3 | Pending |
| CHRT-01 | Phase 3 | Pending |
| CHRT-02 | Phase 3 | Pending |
| CHRT-03 | Phase 3 | Pending |
| CHRT-04 | Phase 3 | Pending |
| CHRT-05 | Phase 3 | Pending |
| UIUX-01 | Phase 3 | Pending |
| UIUX-02 | Phase 3 | Pending |
| UIUX-03 | Phase 3 | Pending |
| UIUX-04 | Phase 3 | Pending |
| UIUX-05 | Phase 3 | Pending |
| UIUX-06 | Phase 3 | Pending |
| UIUX-07 | Phase 3 | Pending |

---

*Created: 2026-03-23*
*Last updated: 2026-03-23 after initial roadmap creation*
