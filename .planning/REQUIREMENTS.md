# Requirements: Kinh Dich x Tu Vi — AI Luan Giai MVP

**Defined:** 2026-03-23
**Core Value:** User enters birth data and receives an accurate, personalized, expert-level Tu Vi interpretation that is empowering — powered by AI but grounded in validated scoring logic and expert-curated knowledge.

## v1 Requirements

Requirements for initial release (test with ~20-50 expert clients).

### Data Input

- [ ] **DINP-01**: User can enter birth date via date picker (duong lich / solar calendar)
- [ ] **DINP-02**: User can select birth time from dropdown of 12 canh gio, or "khong ro" (unknown)
- [ ] **DINP-03**: User can select gender (Nam/Nu)
- [ ] **DINP-04**: User can optionally enter their name (ho ten)
- [ ] **DINP-05**: System converts duong lich to am lich (lunar calendar) correctly, including intercalary months

### Data Pipeline

- [ ] **PIPE-01**: System scrapes cohoc.net to generate a complete la so (12 cung x sao placements) from birth data
- [ ] **PIPE-02**: System extracts all chinh tinh (14 major stars) and phu tinh (minor stars) positions from scraped data
- [ ] **PIPE-03**: System determines Cung Menh from la so data
- [ ] **PIPE-04**: System caches la so results so identical birth data does not re-scrape
- [ ] **PIPE-05**: System handles cohoc.net unavailability gracefully with Vietnamese error message and retry option

### Scoring Engine

- [ ] **SCOR-01**: System calculates Duong (positive), Am (negative), and TB (neutral) scores per dimension from sao placements
- [ ] **SCOR-02**: System calculates scores for 3 time horizons: ca doi (lifetime, moc 10 nam), 10 nam (decade, moc tung nam), 12 thang (monthly)
- [ ] **SCOR-03**: System detects alert-triggering sao combinations and generates positive (triangle up) and negative (triangle down) alerts with tag text
- [ ] **SCOR-04**: Scoring logic matches validated Google Sheets output for 20+ test cases

### Knowledge Base

- [ ] **KBAS-01**: 7 dimension-specific markdown KB files exist (su nghiep, tien bac, hon nhan, suc khoe, dat dai, hoc tap, con cai)
- [ ] **KBAS-02**: Core reference files exist (scoring_rules.md, alert_interpretation.md, tone_guidelines.md)
- [ ] **KBAS-03**: Star reference files exist for chinh tinh (14 major stars) and phu tinh
- [ ] **KBAS-04**: Each KB file fits within ~5-10K tokens for inline prompt injection (no RAG needed)

### AI Luan Giai

- [ ] **AILG-01**: System generates personalized narrative luan giai per dimension via Claude API with structured output (tong quan, phan tich giai doan, moc chu y, loi khuyen, disclaimer)
- [ ] **AILG-02**: AI responses stream to frontend in real-time (SSE)
- [ ] **AILG-03**: AI tone is empowering and positive — no fear-inducing predictions; every negative alert includes actionable advice
- [ ] **AILG-04**: AI only references stars and data present in the user's actual la so (no hallucinated sao)
- [ ] **AILG-05**: System generates a tong quan van menh (cross-dimension overview summary, 3-5 sentences) shown on result page before dimension selection
- [ ] **AILG-06**: Dimension luan giai is generated on-demand when user clicks a dimension (not all upfront)

### Charts & Visualization

- [ ] **CHRT-01**: Result page displays scoring line charts per dimension: ca doi (X=age ranges, Y=score, lines for Duong/Am/TB)
- [ ] **CHRT-02**: Result page displays decade charts per dimension: 10 nam (X=individual years, Y=score, lines for Duong/Am/TB)
- [ ] **CHRT-03**: Alert markers (triangle up/triangle down) are visible on charts at relevant time points
- [ ] **CHRT-04**: Charts are rendered client-side from score data JSON
- [ ] **CHRT-05**: Charts are mobile-responsive

### User Flow & Web Interface

- [ ] **UIUX-01**: Landing page with CTA "Bat dau" leads to input form
- [ ] **UIUX-02**: Processing screen shows multi-step progress ("Dang lay la so..." → "Dang phan tich..." → "Dang tao luan giai...")
- [ ] **UIUX-03**: Result page shows header (name, birth info) + overview chart + AI summary + 7 dimension buttons
- [ ] **UIUX-04**: Dimension detail page shows dimension-specific charts + streamed AI luan giai text
- [ ] **UIUX-05**: Each result has a shareable URL (no login required)
- [ ] **UIUX-06**: Entire interface is in Vietnamese
- [ ] **UIUX-07**: All pages are mobile-responsive

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Enhanced Interpretations

- **EITP-01**: Two-level explanation depth (basic overview vs. in-depth analysis per dimension)
- **EITP-02**: Age-appropriate interpretation guidance (20-30, 30-45, 45-60, 60+)

### Social & Sharing

- **SOCL-01**: Email/link sharing improvements based on test group feedback
- **SOCL-02**: Compatibility / partner chart comparison

### Infrastructure

- **INFR-01**: Fallback la so calculation engine (if cohoc.net scraper breaks permanently)
- **INFR-02**: User accounts and saved readings
- **INFR-03**: PWA install prompt for mobile users

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| User login / accounts | Adds friction; shareable URLs solve "save" need for MVP test group |
| Payment / monetization | Test value first; do not introduce payment friction during validation |
| Chatbot / conversational AI | Changes product from structured reading to open-ended chat; high complexity and cost |
| Kinh Dich gieo que | Separate domain and knowledge base; validate Tu Vi MVP first |
| PDF export | Low value for test group; browser print works for power users |
| Push notifications | Requires accounts; no accounts in MVP |
| Multi-dimension comparison view | Complexity vs value tradeoff; individual readings first |
| Bilingual support (English) | Vietnamese-only for MVP; internationalization later |
| Mobile native app | Web-first; responsive design covers 95% of value at 10% cost |
| Fear-based predictions / fate language | Ethical and product-quality anti-feature; explicitly prohibited |
| Daily horoscopes / planetary transits | Tu Vi is birth-chart based (static); daily horoscope is a different product category |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| (populated by roadmapper) | | |

**Coverage:**
- v1 requirements: 33 total
- Mapped to phases: 0
- Unmapped: 33

---
*Requirements defined: 2026-03-23*
*Last updated: 2026-03-23 after initial definition*
