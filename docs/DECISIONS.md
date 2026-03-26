# DECISIONS.md — Architecture Decision Log
## ADR Format: Decision → Context → Rationale → Consequences

---

### ADR-001: Playwright over Selenium for scraping

**Decision:** Use Playwright instead of Selenium for scraping cohoc.net

**Context:** Existing scraper uses Selenium. Need async scraping that works well with FastAPI.

**Rationale:**
- Playwright is async-native (works with asyncio / FastAPI)
- Faster execution, better headless defaults
- Auto-waits for elements (less flaky than Selenium)
- Single browser install command (`playwright install chromium`)
- Better documentation for Claude Code to work with

**Consequences:**
- Need to rewrite existing Selenium scraper
- Playwright binary (~200MB) must be included in Docker image
- Slight learning curve if unfamiliar (mitigated by Claude Code)

---

### ADR-002: Structured prompts over RAG

**Decision:** Use structured prompt engineering with inline KB context. No RAG (vector DB + retrieval).

**Context:** Need to feed expert knowledge to Claude for luận giải generation.

**Rationale:**
- Total KB per dimension call: ~5-10K tokens — fits easily in 200K context window
- RAG adds complexity: vector DB setup, embedding pipeline, retrieval quality tuning
- Structured prompts are deterministic and easier to debug
- MVP timeline (2-4 weeks) doesn't allow RAG infrastructure

**Consequences:**
- KB size limited to ~100K tokens total (sufficient for MVP)
- Must restructure KB when moving to Phase 2 (Kinh Dịch, chatbot) → migrate to RAG then
- All KB loaded as markdown files → simple to edit and version control

**Revisit when:** KB grows beyond 100K tokens, or chatbot feature requires dynamic retrieval.

---

### ADR-003: Pre-generate all 7 dimensions on submit

**Decision:** When user submits form, generate all 7 dimension luận giải + 1 overview = 8 AI calls immediately.

**Context:** Could generate on-demand (when user clicks a dimension) or pre-generate.

**Rationale:**
- User waits once (20-30s), then all content is instant
- Simpler caching: entire profile is either complete or not
- Avoids "loading..." state every time user clicks a new dimension
- 8 concurrent Claude API calls is manageable (~15-25s total)
- Better UX despite longer initial wait

**Consequences:**
- Higher initial API cost per user (pay for 7 dims even if user only reads 2)
- Longer processing time (20-30s vs 5-10s for single dimension)
- Need robust background job + polling mechanism
- Need progress indicator UX

---

### ADR-004: SQLite for MVP caching

**Decision:** Use SQLite as the only database.

**Context:** Need to cache profiles (lá số + scores + AI text) to avoid re-computation.

**Rationale:**
- Zero configuration, file-based
- Sufficient for 50-500 profiles
- JSON column support for structured data
- No external service dependency
- Easy to migrate to PostgreSQL later if needed

**Consequences:**
- Single-writer limitation (fine for MVP traffic)
- Must persist SQLite file in Railway volume
- No concurrent write safety (not needed for MVP)

**Revisit when:** Traffic exceeds ~100 concurrent users or need multi-server deployment.

---

### ADR-005: Next.js with App Router

**Decision:** Use Next.js 15+ with App Router for frontend.

**Context:** Need a web app with SEO-friendly landing page + dynamic result pages.

**Rationale:**
- SSR for landing page (SEO, social sharing)
- Dynamic routes for result pages (`/result/[id]`)
- React ecosystem (Recharts, Tailwind)
- Vercel deployment is trivial
- Claude Code works well with Next.js

**Consequences:**
- App Router has some complexity (server vs client components)
- Must be careful about client-side charting (Recharts = client component)
- Heavier than plain HTML but worth the DX

---

### ADR-006: Birth time is mandatory

**Decision:** User MUST provide giờ sinh (1 of 12 canh). No "unknown" option.

**Context:** Some users don't know their exact birth time.

**Rationale:**
- Giờ sinh determines Cung Mệnh — the most critical element in Tử Vi
- Without it, the entire chart is unreliable
- Expert practice: refuses to read without birth time
- Providing inaccurate readings would damage trust
- Better to turn away users than give wrong results

**Consequences:**
- Some users will be unable to use the app
- Need clear UX messaging explaining WHY (not just "required field")
- Suggest: "Hỏi cha mẹ hoặc xem sổ khai sinh"
- May lose 10-20% of potential users

---

### ADR-007: Landing page as full marketing page

**Decision:** Build a comprehensive marketing landing page, not just a simple form.

**Context:** MVP could have a minimal form-only page. But we want to test positioning and collect leads.

**Rationale:**
- Test marketing messaging before full launch
- Build trust with new visitors (not just test group)
- Collect conversion data (landing → form submit rate)
- Serves dual purpose: test tool quality + test market response
- Content can be reused for public launch

**Consequences:**
- More frontend work (additional sections, copy, design)
- Need to write marketing copy (can iterate)
- Must not delay MVP — landing page can be "good enough" first, polish later

---

### ADR-008: Modern minimalist design over traditional Eastern aesthetic

**Decision:** Design follows Notion/Linear style — clean, minimal, modern typography.

**Context:** Vietnamese tử vi apps typically use traditional aesthetics (red/gold, Chinese characters, dragons).

**Rationale:**
- Differentiate from "mê tín" apps
- Appeal to younger, urban, tech-savvy demographic
- "Risk management" positioning requires professional look
- Easier to build and maintain with Tailwind
- Builds trust through modern design language

**Consequences:**
- May feel "less authentic" to traditional tử vi users
- Need other trust signals (expert credentials, methodology explanation)
- Risk: some users expect traditional look and feel confused

---

### ADR-009: Monorepo with separate frontend/backend directories

**Decision:** Single repo with `/frontend` and `/backend` directories.

**Context:** Could use separate repos or monorepo.

**Rationale:**
- Simpler for solo developer
- Shared documentation in `/docs`
- Claude Code can access full context
- Easy to coordinate changes

**Consequences:**
- Vercel and Railway both deploy from same repo (configure root directory)
- Slightly more complex CI/CD configuration

---

### ADR-010: Vietnamese only for MVP

**Decision:** All UI, content, and AI output in Vietnamese only.

**Context:** Could build bilingual (Vietnamese + English) from the start for Việt Kiều market.

**Rationale:**
- MVP test group is Vietnamese-speaking
- Reduces scope significantly
- AI prompt quality is better when single-language
- Can add English in Phase 2

**Consequences:**
- Exclude potential Việt Kiều users for now
- Must plan i18n-friendly code structure for later
- All strings should be extracted (not hardcoded) to ease future translation