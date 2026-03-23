# Kinh Dich x Tu Vi — AI Luan Giai MVP

## What This Is

A web application that takes a user's birth data (ngay gio sinh), generates a Vietnamese Tu Vi (astrology) chart with scores across life dimensions, and uses an AI agent (Claude) to produce personalized narrative interpretations ("luan giai") for each dimension. Built as an MVP to test with ~20-50 existing clients of a domain expert partner.

## Core Value

User enters birth data and receives an accurate, personalized, expert-level Tu Vi interpretation that is empowering (not fear-inducing) — powered by AI but grounded in validated scoring logic and expert-curated knowledge.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Data pipeline: scrape cohoc.net to generate structured la so (12 cung x sao placements) from birth data
- [ ] Duong lich to Am lich conversion for Tu Vi calculations
- [ ] Scoring engine: port Google Sheet scoring logic to Python (Duong/Am/TB scores per dimension per time horizon)
- [ ] Alert system: detect sao combinations triggering positive/negative alerts with tags
- [ ] Knowledge base: 7 dimension-specific markdown files + core/star reference files for AI prompt injection
- [ ] AI luan giai engine: per-dimension narrative generation via Claude API with structured output and tone rules
- [ ] Streaming AI responses to frontend for real-time UX
- [ ] Tong quan van menh: cross-dimension overview summary generation
- [ ] Chart visualization: lifetime and decade charts with Duong/Am/TB lines and alert markers
- [ ] User flow: landing page → input form → processing screen → result page → dimension detail pages
- [ ] Shareable result URLs (no login required)
- [ ] Mobile-responsive web interface
- [ ] Caching for la so data (same birth data = same chart)
- [ ] Graceful error handling when cohoc.net is unavailable

### Out of Scope

- Login/accounts — reduce friction, shareable links instead (MVP)
- Payment/monetization — test value first, monetize later
- Chatbot/conversational AI — structured output only for MVP
- Kinh Dich gieo que — separate feature, not in this MVP
- PDF export — not needed for test group
- Push notifications — no accounts = no push
- Multi-dimension comparison view — complexity vs value tradeoff
- Bilingual support — Vietnamese only for MVP
- Mobile native app — web-first approach

## Context

**Domain:** Vietnamese Tu Vi (astrology) is a complex system using lunar calendar, 14 major stars (chinh tinh), minor stars (phu tinh), 12 cung (houses), and scoring across 7 life dimensions (su nghiep, tien bac, hon nhan, suc khoe, dat dai, hoc tap, con cai).

**Expert partner:** A Tu Vi expert with existing client base (~20-50 people) who will review AI outputs for accuracy and curate the knowledge base. Limited availability (~5 hours total across 3 sessions).

**Existing assets:**
- Working scoring engine in Google Sheets (laso_points lookup tables) — validated by expert over many readings
- Scraper target: tuvi.cohoc.net/lap-la-so-tu-vi.html for la so generation
- Research documents: market analysis, MVP scope definition, user research framework (not yet executed)

**Key risk:** Scraper dependency on cohoc.net (could change HTML or block requests). AI hallucination must be constrained to provided data only.

**Test methodology:** The discovery framework and persona hypotheses are NOT yet validated. This MVP exists to generate evidence before full validation.

## Constraints

- **Timeline**: 2-4 weeks
- **Team**: 1 developer (using Claude Code), 1 domain expert (~5h availability)
- **Budget**: Minimal — free/cheap infrastructure (Vercel free tier, Railway starter)
- **Test group**: ~20-50 existing expert clients
- **Language**: Vietnamese only
- **AI model**: Claude Sonnet API (Vietnamese quality, 200K context, structured prompts)
- **Tone (non-negotiable)**: Positive/empowering language, no fear-inducing predictions, every negative alert must include actionable advice

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Next.js frontend | SSR for SEO, React ecosystem | — Pending |
| Python FastAPI backend | Scraper + scoring logic fits Python | — Pending |
| Claude Sonnet API for AI | Vietnamese quality, 200K context | — Pending |
| Structured prompt + inline KB (no RAG) | KB fits in context window (~5-10K tokens per dimension) | — Pending |
| SQLite or Supabase for caching | MVP only needs la so caching | — Pending |
| Chart.js or Recharts for charts | Standard, well-documented | — Pending |
| Vercel (frontend) + Railway (backend) | Fast, cheap deployment | — Pending |
| No auth for MVP | Reduce friction, shareable links | — Pending |
| Scrape cohoc.net for la so | Fastest path to working la so generation | — Pending |
| On-demand dimension generation | Generate luan giai when user clicks dimension, not all upfront | — Pending |

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
*Last updated: 2026-03-23 after initialization*
