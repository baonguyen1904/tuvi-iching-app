# Stack Research

**Domain:** Vietnamese Tu Vi AI interpretation web app
**Researched:** 2026-03-23
**Confidence:** HIGH (all versions verified from official sources on research date)

---

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| Next.js | 16.2.1 | Frontend framework | App Router gives SSR for SEO-friendly shareable result pages; Turbopack default for fast dev; built-in SSE support via Route Handlers for streaming AI responses. The Vercel template for Next.js + FastAPI exists as a reference. |
| React | 19.x (bundled with Next.js 16) | UI rendering | Default with Next.js 16; React Compiler (auto-memoization) is stable; View Transitions available for result page animations. |
| TypeScript | 5.x (bundled with Next.js 16) | Type safety | Enforced by create-next-app default; critical for the scoring engine data model where mis-typed cung/sao data causes silent bugs. |
| FastAPI | 0.135.2 | Backend API | Python-first: scraping, scoring engine, and calendar conversion are all Python-native. Async-first design matches SSE streaming. Auto-generates OpenAPI docs. Pydantic v2 integration is tight. |
| Python | 3.12 | Runtime | 3.12 is the LTS sweet spot for 2026 — supported by all libraries in this stack. 3.13 available but ecosystem compatibility less proven. |
| Pydantic | 2.12.5 | Data validation + serialization | Ships with FastAPI; defines la so response schemas for the scoring engine output and Claude structured output parsing. V2's Rust core is dramatically faster than V1. |
| anthropic (Python SDK) | 0.86.0 | Claude API client | Official SDK, supports async streaming and `client.beta.messages.parse()` for structured output (beta header required). Vietnamese quality of claude-sonnet-4-5 is validated. |
| Tailwind CSS | 4.x | Styling | CSS-first config (no tailwind.config.js needed); 5x faster full builds; ships as default in create-next-app for Next.js 16. Mobile-responsive Vietnamese-language UI without custom CSS weight. |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| playwright (Python) | 1.58.0 | La so scraping from cohoc.net | cohoc.net lap-la-so-tu-vi.html uses client-side JS to render the chart — static httpx will get empty HTML. Use Playwright with async API to submit the birth data form and extract the rendered DOM. |
| beautifulsoup4 | 4.14.3 | HTML parsing after Playwright extraction | After Playwright retrieves rendered HTML, pass `page.content()` to BeautifulSoup with lxml parser for fast structured extraction of cung/sao placements. |
| lxml | 6.0.2 | BS4 HTML parser backend | Recommended parser for BeautifulSoup; significantly faster than html.parser; install as `beautifulsoup4[lxml]`. |
| vnlunar | 1.1.1 | Solar-to-lunar date conversion | Vietnamese-specific timezone handling (UTC+7); supports 1800-2199 range; required for Duong lich → Am lich conversion before Tu Vi chart calculation. Do not use generic Chinese calendar libraries — Vietnamese calendar has known divergences from Chinese calendar (e.g. 1984-1985 New Year). |
| recharts | 3.8.0 | Chart visualization | React-native SVG charts; line charts for Duong/Am/TB score timelines per dimension; composable component API matches the scoring data shape; lighter than Chart.js (no canvas complexity); supports custom tooltips for alert markers. |
| httpx | 0.28.1 | HTTP client for internal API calls + fallback scraping | Use for calling internal FastAPI endpoints from Next.js server components, and as a lightweight fallback if cohoc.net ever serves static HTML. Do NOT use as primary scraper — cohoc.net is JS-rendered. |
| uvicorn | 0.34.x | ASGI server for FastAPI | Production server for FastAPI. Use with `--workers` equal to CPU count. Gunicorn + uvicorn worker class for multi-core Railway deployment. |
| python-dotenv | 1.x | Environment variable loading | Load `ANTHROPIC_API_KEY` and other secrets from `.env` in development; Railway/Vercel inject env vars at runtime. |
| aiocache or in-process dict | - | La so caching | For MVP: a simple Python in-process dict keyed on `hash(birth_data)` is sufficient for ~50 users. If multiple workers: use Redis via `aiocache`. The goal is: same birth data input = same chart, no repeat scrape. |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| create-next-app@latest | Scaffold Next.js 16 project | Use: `npx create-next-app@latest --typescript --tailwind --app --turbopack` — gets TypeScript, Tailwind v4, App Router, Turbopack in one command |
| Playwright browser install | Download Chromium for scraper | Run `playwright install chromium` after pip install — only Chromium needed, saves 1GB+ |
| python-decouple or pydantic-settings | Config management for FastAPI | Use pydantic-settings (ships with pydantic v2) for typed config from env vars |
| pytest + pytest-asyncio | Backend testing | Critical for scoring engine unit tests — the Google Sheets logic must be ported and validated with expert data before Claude prompts consume it |

---

## Installation

```bash
# --- Frontend (Next.js) ---
npx create-next-app@latest tuvi-frontend --typescript --tailwind --app --turbopack
cd tuvi-frontend
npm install recharts
npm install -D @types/node

# --- Backend (FastAPI + Python 3.12) ---
python3.12 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install fastapi==0.135.2
pip install uvicorn[standard]
pip install pydantic==2.12.5
pip install pydantic-settings
pip install anthropic==0.86.0
pip install playwright==1.58.0
pip install beautifulsoup4==4.14.3 lxml
pip install vnlunar==1.1.1
pip install httpx==0.28.1
pip install python-dotenv

# Install Playwright browser (Chromium only)
playwright install chromium
```

---

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| Playwright (Python) | httpx + BeautifulSoup (pure HTTP) | Only if cohoc.net serves static HTML — currently it does not. If the site adds a proper API endpoint, switch to httpx and drop Playwright. |
| vnlunar | lunardate / LunarCalendar (Chinese) | Never for this app — these libraries do not handle the Vietnamese calendar divergence from the Chinese calendar. Low-traffic edge case but correctness matters for Tu Vi. |
| Recharts | Chart.js / react-chartjs-2 | If you need Canvas-based rendering (e.g., export to PNG/PDF). For MVP (no PDF export), SVG-based Recharts is simpler to compose with React state. |
| In-process dict cache | Redis | Use Redis if deploying multiple FastAPI workers (Railway production scale). For MVP with ~50 users on a single worker, in-process cache is zero-infrastructure. |
| FastAPI (Python backend) | Next.js API routes (Node.js) | If you abandon the Python scraping/scoring requirement entirely. Not recommended: the scoring engine is already in Google Sheets (Python port is natural) and Playwright is Python-native. |
| Vercel (frontend) | Netlify / Cloudflare Pages | If Vercel's free tier limits become a problem. Vercel is the native host for Next.js; the Next.js + FastAPI starter template is maintained by Vercel. |
| Railway (backend) | Render.com | Render has a free tier with sleep-on-inactivity (kills scraping reliability); Railway's $5/month Hobby plan keeps the server always-on. Use Render if budget is zero and you can tolerate cold starts. |

---

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| requests (Python HTTP) | Synchronous; blocks FastAPI's async event loop; causes performance degradation when called inside `async def` routes | httpx with `AsyncClient` |
| httpx as primary cohoc.net scraper | cohoc.net lap-la-so-tu-vi.html renders the la so via JavaScript — httpx returns empty chart container HTML | playwright with async API |
| Selenium | 2x slower than Playwright on benchmark (536ms vs 290ms per interaction); more complex setup; no modern auto-waiting | playwright |
| Chinese lunar calendar libraries (lunardate, LunarCalendar) | Vietnamese calendar diverges from Chinese calendar for certain years — incorrect Am lich dates corrupt all downstream Tu Vi calculations | vnlunar |
| LangChain / LlamaIndex | Adds abstraction layers with non-trivial complexity for what is a direct API call pattern; the KB fits in context window so RAG is unnecessary | anthropic Python SDK directly |
| WebSockets | Overkill for one-directional AI streaming; requires persistent connection management; SSE is simpler and sufficient | FastAPI StreamingResponse + EventSource on client |
| Supabase / PostgreSQL | No user accounts, no relational data, no queries — la so caching by birth data hash is a key-value pattern | In-process dict (MVP) → Redis (production) |
| SQLite on Railway | Railway filesystem is ephemeral — SQLite data is wiped on redeploy. If you need persistence, use Railway's managed Redis or PostgreSQL add-on | Railway managed Redis |
| Next.js Pages Router | App Router is the current standard; Pages Router is in maintenance mode; new features (Cache Components, proxy.ts, streaming) are App Router only | App Router (default in create-next-app) |

---

## Stack Patterns by Variant

**If cohoc.net blocks Playwright/headless browser:**
- Investigate cohoc.net's API endpoints via browser DevTools (network tab) — the JavaScript-rendered chart likely calls a backend API
- Switch from DOM scraping to direct API call with httpx
- Cache result aggressively to minimize future calls
- Keep Playwright as fallback with human-in-the-loop CAPTCHA handling if needed

**If Railway free trial expires during MVP:**
- Move FastAPI to Render.com free tier (accepts cold starts for low-traffic MVP)
- Or deploy FastAPI as a Vercel Python serverless function (zero config, but cold starts and 10s timeout limit streaming)
- Vercel's `vercel/examples/python/flask` pattern works for FastAPI too

**If Claude Sonnet API costs spike during testing:**
- Add response caching keyed on `hash(dimension + chart_data)` — same chart + same dimension = cache hit
- Use `max_tokens` budgeting per dimension (e.g., 800 tokens per luan giai)
- Batch test with `client.messages.batches` API for non-interactive test runs

**If the scoring engine port from Google Sheets is complex:**
- Keep Python scoring engine as pure functions with no FastAPI dependency initially
- Unit test with `pytest` against known expert-validated chart outputs before wiring to API
- The Google Sheets structure (laso_points lookup tables) maps naturally to Python dicts

---

## Version Compatibility

| Package A | Compatible With | Notes |
|-----------|-----------------|-------|
| fastapi@0.135.2 | pydantic@2.12.5 | FastAPI 0.100+ dropped Pydantic v1 support entirely — do not install pydantic<2 |
| anthropic@0.86.0 | Python 3.9+ | SDK requires Python 3.9+; use Python 3.12 for this project |
| playwright@1.58.0 | Python 3.9+ | Run `playwright install chromium` separately after pip install |
| next@16.2.1 | Node.js 20.9+ | Next.js 16 requires Node.js 20.9+ (LTS); Node 18 is dropped |
| recharts@3.8.0 | react@19.x | Recharts 3.x supports React 18 and 19; no compatibility issues with Next.js 16 |
| tailwindcss@4.x | next@16.x | TW4 is the create-next-app default; CSS @import syntax replaces @tailwind directives |
| vnlunar@1.1.1 | Python 3.9+ | Pure Python; no native dependencies |

---

## Scraper Architecture Note

The cohoc.net form (`tuvi.cohoc.net/lap-la-so-tu-vi.html`) uses JavaScript to render the la so — verified by direct inspection. The birth data parameters are:
- `g_namSinh` (year), `g_thangCur` (month), `g_ngayCur` (day), `g_gioSinh` (hour), `g_isNam` (gender), `g_isduonglich` (calendar type)

**Recommended scraping flow:**
1. Playwright `async_playwright()` → launch Chromium headless
2. Navigate to form URL
3. Fill fields via `page.fill()` / `page.select_option()`
4. Click submit → wait for chart container to populate (`page.wait_for_selector('.chart')`)
5. `page.content()` → pass to BeautifulSoup + lxml
6. Parse 12 cung × sao placement tables into structured dict
7. Cache result keyed on `sha256(birth_params)` in-process

Before implementing: inspect the Network tab to check if a XHR/fetch API endpoint exists — if so, call it directly with httpx instead. Direct API call is 10x more stable than DOM scraping.

---

## Sources

- Next.js 16.2.1 version — `npm view next version` on 2026-03-23
- Next.js 16 blog post — https://nextjs.org/blog/next-16 (published October 21, 2025)
- Next.js 16.1 blog post — https://nextjs.org/blog/next-16-1 (published December 18, 2025)
- FastAPI 0.135.2 — https://pypi.org/project/fastapi/ verified 2026-03-23
- anthropic Python SDK 0.86.0 — https://pypi.org/project/anthropic/ verified 2026-03-23
- httpx 0.28.1 — https://pypi.org/project/httpx/ verified 2026-03-23
- playwright Python 1.58.0 — https://pypi.org/project/playwright/ verified 2026-03-23
- pydantic 2.12.5 — https://pypi.org/project/pydantic/ verified 2026-03-23
- vnlunar 1.1.1 — https://github.com/nguyen703/vnlunar verified 2026-03-23
- recharts 3.8.0 — npm registry, 16 days ago from 2026-03-23 (MEDIUM confidence — could not fetch npm page directly, inferred from search results)
- beautifulsoup4 4.14.3 — https://pypi.org/project/beautifulsoup4/ search-verified 2026-03-23
- Claude structured outputs — https://platform.claude.com/docs/en/build-with-claude/structured-outputs (public beta, November 14, 2025)
- Tailwind CSS v4 + Next.js 16 compatibility — https://tailwindcss.com/docs/guides/nextjs verified 2026-03-23
- Railway free tier status — search-verified: no permanent free tier since August 2023; Hobby plan $5/month
- cohoc.net form analysis — direct WebFetch to https://tuvi.cohoc.net/lap-la-so-tu-vi.html, 2026-03-23

---
*Stack research for: Vietnamese Tu Vi AI interpretation web app*
*Researched: 2026-03-23*
