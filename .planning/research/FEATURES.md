# Feature Research

**Domain:** Vietnamese Tu Vi (astrology) AI interpretation web application
**Researched:** 2026-03-23
**Confidence:** MEDIUM — Western astrology app features are well-documented (HIGH); Vietnamese Tu Vi-specific web app features rely on fewer sources and direct product analysis (MEDIUM); AI interpretation UX patterns are actively evolving (MEDIUM)

---

## Feature Landscape

### Table Stakes (Users Expect These)

Features users assume exist. Missing these = product feels incomplete.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Birth data input form | Entry point to all value; can't exist without it | LOW | Fields: name (optional), birth date, birth time, gender; must support both solar (duong lich) and lunar (am lich) calendars |
| Lunar/solar calendar conversion | Tu Vi charts require am lich (lunar) date; users may only know duong lich | MEDIUM | Requires correct conversion library or algorithm; a wrong conversion produces a completely wrong chart |
| La so (birth chart) generation | Users come for their Tu Vi chart; this IS the product | HIGH | Depends on scraping cohoc.net or reimplementing la so logic; the 12-cung grid with sao placements is the expected visual |
| Chart visualization: 12-cung grid | Standard Tu Vi display format; any Tu Vi user recognizes this layout | MEDIUM | Square grid of 12 palaces with star names inside each; must be legible on mobile |
| Dimension-level interpretation (luan giai) | Users want to know what the chart MEANS for their life areas; raw charts are not self-interpretable | HIGH | Must cover the 7 dimensions: su nghiep, tien bac, hon nhan, suc khoe, dat dai, hoc tap, con cai |
| Vietnamese-language UI and output | Target users are Vietnamese; English output is unusable for this audience | LOW | All text, labels, interpretations must be in Vietnamese |
| Mobile-responsive layout | Vietnamese users access web on mobile; non-responsive = abandoned | MEDIUM | Chart grid is the hardest element to make responsive |
| Results page (reading result) | Users need a stable destination to read their interpretation | LOW | The landing page after chart generation |
| Graceful error handling | cohoc.net dependency can fail; user must not see a broken page | MEDIUM | Friendly Vietnamese error message + retry option |
| Processing/loading feedback | Chart + AI generation takes seconds; silent wait = user thinks app is broken | LOW | Loading indicator or animated processing screen between input and results |

### Differentiators (Competitive Advantage)

Features that set the product apart. Not required, but valued.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| AI-generated narrative luan giai (per dimension) | Existing Tu Vi sites show raw chart or brief formulaic text; full expert-quality narrative per dimension is rare and high-value | HIGH | Core differentiator; requires Claude API + expert-curated knowledge base + prompt engineering per dimension |
| Tong quan van menh (cross-dimension overview) | Users want a "so what" summary before diving into 7 dimensions; no competitor currently offers an AI-synthesized overview | HIGH | Requires reading across all 7 dimension scores + alert flags; generated last after all dimensions scored |
| Empowering tone (non-fear-inducing) | Most Vietnamese Tu Vi apps use fate-heavy, anxiety-inducing language; positive/actionable framing is a differentiator that creates word-of-mouth | MEDIUM | Tone is enforced at prompt layer; every negative alert must include actionable advice; this is a non-negotiable product principle |
| Scoring visualization: lifetime + decade charts | Luck/fortune score trajectories over time (Duong/Am/TB lines) are rare outside desktop software; web-based charting creates "aha" moments | MEDIUM | Chart.js or Recharts line charts; Duong (positive), Am (negative), TB (baseline) lines per dimension per time period |
| Alert markers on charts | Flagging sao combinations that trigger specific positive/negative life events (with tags) overlaid on timeline is unique | MEDIUM | Requires alert detection logic in scoring engine; displayed as markers on chart at relevant time periods |
| On-demand dimension generation | Generating all 7 dimensions at once would be slow and wasteful; click-to-generate per dimension creates perceived speed and focused reading | MEDIUM | Streaming AI responses per dimension; user sees text appear as it generates; reduces initial load time |
| Streaming AI responses | Real-time text streaming makes long AI interpretations feel alive and fast vs. a spinner then dump | MEDIUM | Server-Sent Events or WebSocket from FastAPI to Next.js frontend; standard Claude API streaming |
| Shareable result URLs (no login required) | Users share readings with family and friends; social spread is free marketing; no-login removes all friction | MEDIUM | URL must encode or reference the birth data / cached result; shareable without account creation |
| Caching: same birth data = same result | Expert clients will re-read their chart; repeated scraping wastes time and risks blocking; deterministic results build trust | MEDIUM | Cache keyed on birth datetime + gender; SQLite or Supabase KV; la so data + dimension scores cached |
| Two-level explanation depth | "Thai Am - Tu Vi 2026" (competitor) validated this: basic version for newcomers, in-depth for researchers | HIGH | Significant extra complexity; defer to post-MVP unless expert partner can supply both knowledge base levels |

### Anti-Features (Commonly Requested, Often Problematic)

Features that seem good but create problems.

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| User login / accounts | "Save my chart for later" | Adds auth complexity, friction, GDPR/privacy concerns, database user management; the MVP test group doesn't need this; login kills conversion | Shareable URL solves the "save" need; anonymous session IDs for temporary state |
| Chatbot / conversational follow-up | "Let me ask questions about my chart" | Changes the product from a structured reading tool into an open-ended AI chat, which requires prompt safety rails, abuse prevention, session management, and much higher API costs; also dilutes the expert-curated reading quality | Structure the luan giai so thoroughly that users don't need to ask follow-ups; add FAQ-style clarification notes to each dimension |
| Push notifications | "Remind me of important time periods" | Requires accounts, PWA/native infrastructure, and a notification calendar system; no accounts = no push | Daily/weekly dimension pages as returnable URLs; email digests (post-MVP) |
| PDF export / print | "I want to save this as a file" | Low actual usage in test group; adds rendering complexity (html-to-pdf) and layout bugs; mobile users won't print | Shareable URL is the "save" mechanism; browser's native print function works for power users |
| Real-time astrology (daily horoscopes, planetary transits) | "Show me today's fortune" | Tu Vi is a birth-chart system (static for life); daily horoscope is a different product category (zodiac-based) that would confuse the domain and fragment engineering focus | Time-horizon decade charts already show when favorable/unfavorable periods occur; that covers the "what's coming" need |
| Social comparison / compatibility | "Compare my chart with my partner" | Requires rendering two charts, defining comparison logic, and significant UI work; the Tu Vi compatibility analysis is a deep domain in itself | Keep focus on individual reading; compatibility can be a v2+ product if test users explicitly request it |
| Multi-language support (English) | "Some users may want English" | Requires full translation of all 7 knowledge base files, UI strings, and AI prompt outputs; doubles maintenance burden; the test group is Vietnamese | Vietnamese-only for MVP; internalization architecture can be added post-validation |
| Mobile native app (iOS/Android) | "An app feels more professional" | Native app stores require review cycles, update delays, and platform split effort; web-first with responsive design achieves 95% of the value at 10% of the cost | Progressive Web App (PWA) after web is validated; PWA gives install prompt without app store |
| Fear-based predictions / fate language | Some traditional Tu Vi texts use heavy fate language ("you will suffer...") | Research shows fear-based astrology content induces anxiety, creates self-fulfilling negative behavior, and causes users to abandon the product; expert partner has also flagged this | All negative alerts must pair with actionable advice (e.g., "This period requires caution in financial decisions — consider X strategy"); framing as guidance not fate |
| Kinh Dich gieo que (I Ching divination) | Adjacent domain expertise; users may request it | Separate domain, separate knowledge base, separate UX; building it alongside Tu Vi dilutes both | Separate product/feature; validate Tu Vi MVP first |

---

## Feature Dependencies

```
[Birth data input form]
    └──requires──> [Lunar/solar calendar conversion]
                       └──requires──> [La so generation (scraper)]
                                          └──requires──> [Chart visualization: 12-cung grid]
                                          └──requires──> [Scoring engine (dimension scores)]
                                                             └──requires──> [Alert detection]
                                                             └──requires──> [AI luan giai (per dimension)]
                                                                                └──requires──> [Knowledge base (7 dimension MD files)]
                                                             └──requires──> [Scoring visualization: charts]
                                                             └──requires──> [Tong quan van menh]

[Caching (la so)]
    └──enhances──> [La so generation] (avoids re-scraping for same birth data)
    └──enables──> [Shareable result URLs]

[Streaming AI responses]
    └──enhances──> [AI luan giai per dimension] (real-time UX)

[On-demand dimension generation]
    └──enhances──> [AI luan giai per dimension] (reduces initial load, lazy generation)

[Shareable result URLs]
    └──requires──> [Caching] (URL must point to a stable, retrievable result)
```

### Dependency Notes

- **La so generation requires lunar/solar conversion:** Tu Vi charts are calculated on am lich (lunar calendar) dates; without correct conversion the chart is invalid.
- **AI luan giai requires knowledge base:** The AI must be constrained to expert-curated content only; hallucination without a grounding knowledge base is a product-quality failure.
- **Alert detection requires scoring engine:** Alerts are triggered by sao combinations identified during the scoring pass; alert detection is not an independent step.
- **Tong quan van menh requires all 7 dimension scores:** The overview cannot be generated until all dimension scores are available; it is always the last AI generation step.
- **Shareable URL requires caching:** Without caching, a shared URL would re-generate the chart and AI text on every load, which is slow, expensive (API cost), and potentially inconsistent.
- **On-demand generation and streaming are complementary enhancements** to the core AI luan giai feature; they improve UX but are not required for the feature to function.

---

## MVP Definition

### Launch With (v1)

Minimum viable product — what's needed to validate the concept with 20-50 expert clients.

- [ ] Birth data input form (name optional, date, time, gender, solar/lunar toggle) — gateway to all value
- [ ] Duong lich to am lich conversion — required for valid la so
- [ ] La so generation via cohoc.net scraper — fastest path to correct chart
- [ ] Scoring engine: port Google Sheets scoring logic to Python (Duong/Am/TB per dimension per time horizon) — required for AI input
- [ ] Alert detection: sao combination flags with tags — required for accurate luan giai
- [ ] Knowledge base: 7 dimension-specific markdown files + star reference files — required for AI grounding
- [ ] AI luan giai per dimension (on-demand, streaming) — the core value proposition
- [ ] Tong quan van menh overview — makes the result feel complete and summarized
- [ ] Results page with chart visualization (12-cung grid) — base display
- [ ] Scoring visualization: Duong/Am/TB line charts per dimension — "aha" visual for users
- [ ] Alert markers on timeline charts — adds insight beyond raw scores
- [ ] Shareable result URLs (no login) — enables test group to share with expert for feedback
- [ ] Caching for la so data — prevents re-scraping, enables shareable URLs
- [ ] Processing/loading screen — essential UX between input and results
- [ ] Mobile-responsive layout — test group uses mobile
- [ ] Graceful error handling (cohoc.net fallback) — cohoc.net is a single point of failure
- [ ] Vietnamese-only UI — all output in Vietnamese, empowering tone enforced at prompt level

### Add After Validation (v1.x)

Features to add once core is working and test group feedback is collected.

- [ ] Two-level explanation depth (basic vs. in-depth) — add when knowledge base has enough depth to support both levels; trigger: expert partner has time to curate second level
- [ ] Email/link sharing improvements — add if test group reports friction sharing results
- [ ] Fallback la so calculation (if cohoc.net scraper breaks) — add if scraper breaks more than twice during test period
- [ ] Result page improvements from user feedback — add based on what test group finds confusing

### Future Consideration (v2+)

Features to defer until product-market fit is established.

- [ ] User accounts / saved readings — defer until test group explicitly requests persistence beyond shareable URLs
- [ ] Chatbot / conversational follow-up — defer until structured luan giai is proven insufficient; high complexity and cost
- [ ] Compatibility / partner chart comparison — separate domain; validate individual reading first
- [ ] Kinh Dich gieo que — separate product; defer entirely
- [ ] Mobile native app / PWA — defer until web version is validated and retained usage is proven
- [ ] Payment / monetization — test value first; do not introduce payment friction during validation phase
- [ ] Bilingual support (English) — defer until non-Vietnamese user demand is demonstrated
- [ ] Push notifications — requires accounts; defer with accounts
- [ ] PDF export — low value for test group; defer

---

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| Birth data input form | HIGH | LOW | P1 |
| Lunar/solar calendar conversion | HIGH | MEDIUM | P1 |
| La so generation (scraper) | HIGH | HIGH | P1 |
| Chart visualization: 12-cung grid | HIGH | MEDIUM | P1 |
| Scoring engine (dimensions) | HIGH | HIGH | P1 |
| AI luan giai per dimension | HIGH | HIGH | P1 |
| Knowledge base (7 dimension files) | HIGH | MEDIUM | P1 |
| Tong quan van menh overview | HIGH | MEDIUM | P1 |
| Mobile-responsive layout | HIGH | MEDIUM | P1 |
| Empowering tone (prompt enforcement) | HIGH | LOW | P1 |
| Shareable result URLs | HIGH | MEDIUM | P1 |
| Caching (la so + results) | MEDIUM | MEDIUM | P1 |
| Processing/loading screen | MEDIUM | LOW | P1 |
| Graceful error handling | MEDIUM | LOW | P1 |
| Streaming AI responses | MEDIUM | MEDIUM | P2 |
| On-demand dimension generation | MEDIUM | MEDIUM | P2 |
| Scoring visualization (line charts) | HIGH | MEDIUM | P2 |
| Alert detection + markers on charts | MEDIUM | MEDIUM | P2 |
| Two-level explanation depth | MEDIUM | HIGH | P3 |
| Compatibility / partner chart | MEDIUM | HIGH | P3 |
| User accounts / login | LOW | HIGH | P3 |
| Chatbot follow-up | MEDIUM | HIGH | P3 |
| PDF export | LOW | MEDIUM | P3 |
| Mobile native app | LOW | HIGH | P3 |

**Priority key:**
- P1: Must have for launch
- P2: Should have, add when possible
- P3: Nice to have, future consideration

---

## Competitor Feature Analysis

| Feature | cohoc.net (Tu Vi source) | Thai Am - Tu Vi 2026 (app) | Co-Star (Western) | Our Approach |
|---------|--------------------------|---------------------------|-------------------|--------------|
| Birth chart generation | Yes — full 12-cung la so | Yes — lifetime chart | Yes — natal chart | Yes — via cohoc.net scraper |
| Dimension interpretation | Automated brief text | Brief AI interpretations | Daily AI notifications | Expert-curated AI narrative per dimension (deeper) |
| Scoring / luck trajectory | No visual | Yes — daily "Huyen Khi" score | No | Yes — Duong/Am/TB line charts per dimension |
| Alert markers | No | No explicit alerts | No | Yes — sao combination alerts with actionable advice |
| AI tone | Neutral / traditional language | Modern but fate-heavy | Casual / psychological | Empowering, non-fear-inducing — explicit design principle |
| Shareable results | No | No (app-only) | Social profiles (with login) | Yes — no login required |
| Mobile experience | Desktop-first, poor mobile | Native app | Native app | Responsive web (no app store delay) |
| On-demand generation | Not applicable | Pre-computed | Pre-computed | On-demand per dimension with streaming |
| Vietnamese language | Yes | Yes | No (English only) | Yes — Vietnamese only for MVP |
| Multi-profile (family) | No | Yes | No | No for MVP |
| Expert knowledge base | Community articles | Unknown sourcing | Human astrologers + AI | Expert-validated 7-dimension knowledge base |

---

## Sources

- [Co-Star vs The Pattern vs MyNitya comparison](https://mynitya.com/blog/costar-vs-pattern-vs-mynitya-comparison) — MEDIUM confidence (single blog source)
- [Thai Am - Tu Vi 2026 app listing](https://spark.mwm.ai/us/apps/th-i-m-t-vi-2026/1150954869) — MEDIUM confidence
- [AI Tu Vi - Van Han 2026 app listing](https://spark.mwm.ai/us/apps/ai-t-vi-v-n-h-n-2026/6449532445) — MEDIUM confidence
- [cohoc.net la so generation page](https://tuvi.cohoc.net/lap-la-so-tu-vi.html) — HIGH confidence (direct product analysis)
- [10 Best AI-Powered Astrology Apps 2026](https://developerbazaar.com/10-best-ai-powered-astrology-apps/) — LOW confidence (marketing content)
- [How to Develop an Astrology App Like Co-Star 2026](https://www.apptunix.com/blog/how-to-develop-an-astrology-app-like-co-star/) — LOW confidence (dev agency marketing)
- [AI Astrology App Development Features](https://appquipo.com/blog/develop-ai-astrology-app/) — LOW confidence
- [Astrology App Development 2025 - Webelight](https://www.webelight.com/blog/astrology-app-development-in-2025-top-10-horoscope-apps-how-to-build-yours-with-ai-ml-flutter) — LOW confidence
- [Top 5 AI Astrology Predictions Sites - Scrile](https://www.scrile.com/blog/ai-astrology-predictions) — LOW confidence
- [How UX Design Drives Astrology Apps - SeaIsle News](https://seaislenews.com/news/2025/jun/16/how-ux-design-drives-the-success-of-astrology-apps/) — LOW confidence
- [Negative Sides of Astrology (fear-based patterns)](https://medium.com/@dimuthcbandara97/negative-sides-of-astrology-a-critical-examination-41f5749b14fd) — MEDIUM confidence
- [The Pattern vs My Zodiac AI 2026](https://my-zodiac-ai.com/blog/the-pattern-vs-my-zodiac-ai-2026) — LOW confidence (competitor marketing)
- PROJECT.md requirements (validated by domain expert partner) — HIGH confidence

---

*Feature research for: Vietnamese Tu Vi AI interpretation web application (Kinh Dich x Tu Vi MVP)*
*Researched: 2026-03-23*
