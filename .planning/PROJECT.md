# Kinh Dịch × Tử Vi — AI Luận Giải MVP

## What This Is

A web app that takes a user's birth data (ngày giờ sinh), generates a Vietnamese Tử Vi (astrology) chart with scores across life dimensions, and uses Claude AI to produce personalized narrative interpretations ("luận giải") for each dimension. This is an MVP for testing with ~20-50 existing clients of our expert partner — not a full product launch.

## Core Value

Users receive personalized, expert-quality AI narrative interpretations of their Tử Vi chart across 7 life dimensions, grounded in real scoring data — empowering, not fear-inducing.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] User nhập ngày sinh (dương lịch), giờ sinh (12 canh hoặc "không rõ"), giới tính, tên (optional) → hệ thống tạo lá số
- [ ] Scrape cohoc.net để lấy lá số (12 cung × sao placements), cache kết quả
- [ ] Dương lịch → Âm lịch conversion
- [ ] Port Google Sheet scoring logic (laso_points) sang Python — tính scores per dimension per time period
- [ ] Alert system: Phát hiện tổ hợp sao → trigger 🔺 (positive) và 🔻 (negative) alerts với tag text
- [ ] Khi "không rõ giờ sinh" → bỏ qua yếu tố phụ thuộc giờ sinh
- [ ] Knowledge Base: Markdown files per dimension + core rules, expert-reviewed
- [ ] AI luận giải per dimension: Claude Sonnet API call với structured prompt + KB context + score data
- [ ] Output structure: Tổng quan → Phân tích giai đoạn → Mốc cần chú ý → Lời khuyên → Disclaimer
- [ ] Tone rules: Tích cực, empowering, mỗi 🔻 kèm lời khuyên, "cần thận trọng" thay "sẽ gặp họa", disclaimer cuối
- [ ] Tổng quan vận mệnh: AI summary 3-5 câu across all dimensions, hiện trên result page
- [ ] Streaming: AI response streamed to frontend
- [ ] Charts: Cả đời (lifetime) + 10 năm (decade) per dimension, lines Dương/Âm/TB, alert markers
- [ ] Overview chart trên result page
- [ ] Landing page → Input form → Processing screen → Result page → Dimension detail page
- [ ] Shareable URL per result (no login required)
- [ ] Mobile responsive

### Out of Scope

- Chatbot hỏi đáp — Phase 2+, not MVP
- Kinh Dịch gieo quẻ — Separate module, deferred
- User accounts / login — Reduce friction for MVP
- Payment / premium — MVP is free for test group
- PDF/PPTX export — Web view thay thế
- Push notifications — No accounts means no push
- Multi-dimension comparison charts — Nice-to-have, not core
- RAG pipeline — KB fits in context window (~5-10K tokens), no need
- OAuth / social login — Email/password not needed either, no auth at all
- Bilingual (English) — Vietnamese only for MVP

## Context

- **Expert partner**: Domain expert in Tử Vi with existing client base (~20-50 people). Limited availability (~5h total for KB review sessions).
- **Existing scoring engine**: Google Sheet with lookup tables (laso_points) — validated by expert over many readings. Ready to port.
- **Scraper tested**: cohoc.net scraping approach verified, HTML structure known.
- **Knowledge Base approach**: Markdown files injected into AI prompt as context. ~5-10K tokens per dimension call. No RAG needed for MVP.
- **Expert sessions planned**: Session 1 (2h) demo luận giải, Session 2 (2h) review KBs, Session 3 (1h) review AI output.
- **Personas (hypotheses, not validated)**: "Người tìm hướng" (25-40, urban), Business owners (30-50), Việt Kiều, Gen Z spiritual — MVP tests with existing clients only.
- **Positioning**: "Risk intelligence" not "fortune telling" — empowering, not superstitious.

## Constraints

- **Timeline**: 2-4 weeks
- **Team**: 1 developer (using Claude Code), 1 domain expert (~5h availability)
- **Budget**: Minimal — free/cheap infrastructure (Vercel + Railway)
- **Language**: Vietnamese only for MVP
- **Test group**: ~20-50 existing clients of expert
- **Scraper dependency**: cohoc.net could change/block — need caching + error handling
- **Expert time**: Only ~5h total — must be pre-prepared and efficient
- **AI model**: Claude Sonnet API — 200K context window sufficient for structured prompt + inline KB
- **Tech stack**: Next.js (frontend) + Python FastAPI (backend) + SQLite/Supabase (cache) + Chart.js/Recharts (charts)

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Structured prompt + inline KB (no RAG) | KB fits in ~5-10K tokens per dimension, Claude 200K context is plenty | — Pending |
| Scrape cohoc.net for lá số | Already tested and working, fastest path to MVP | — Pending |
| Per-dimension AI calls (not all at once) | Manageable prompt size, streaming UX, on-demand generation | — Pending |
| No authentication | Reduce friction, shareable links, MVP test group only | — Pending |
| Claude Sonnet (not GPT) | Vietnamese quality tốt, large context window | — Pending |
| Web view instead of PPTX | Faster iteration, mobile-friendly, streaming support | — Pending |
| Next.js + Python FastAPI | SSR for SEO (Next.js), scraper + scoring logic natural in Python | — Pending |
| "Không rõ giờ sinh" → skip time-dependent calculations | Simpler than guessing, more honest to user | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd:transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd:complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-03-24 after initialization*
