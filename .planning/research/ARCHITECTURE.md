# Architecture Research

**Domain:** AI-powered astrology interpretation system (Tu Vi / Vietnamese astrology)
**Researched:** 2026-03-23
**Confidence:** HIGH (patterns verified against official docs and multiple implementation examples)

## Standard Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND LAYER                           │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────────┐ │
│  │  Input Form  │  │ Result Page  │  │  Dimension Detail Page │ │
│  │  (birth data)│  │ (chart + nav)│  │  (streaming luan giai) │ │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬─────────────┘ │
│         │                 │                      │               │
│         │    Next.js App Router + React          │               │
│         └─────────────────┴──────────────────────┘               │
├──────────────────────────────────────────────────────────────────┤
│                        API BOUNDARY                               │
│  REST (chart data, cached la so)    SSE (streaming luan giai)    │
├──────────────────────────────────────────────────────────────────┤
│                         BACKEND LAYER                            │
│  ┌──────────┐  ┌──────────────┐  ┌───────────┐  ┌────────────┐  │
│  │  Scraper │  │  Lunar Conv  │  │  Scoring  │  │  AI Engine │  │
│  │  Module  │  │  Module      │  │  Engine   │  │  (Claude)  │  │
│  └────┬─────┘  └──────┬───────┘  └─────┬─────┘  └─────┬──────┘  │
│       │               │                │              │          │
│       └───────────────┴────────────────┴──────────────┘          │
│                         FastAPI router                            │
├──────────────────────────────────────────────────────────────────┤
│                         DATA LAYER                               │
│  ┌──────────────────┐  ┌──────────────┐  ┌────────────────────┐  │
│  │  Cache (SQLite)  │  │  KB Markdown │  │  External: cohoc.  │  │
│  │  la so results   │  │  files (7    │  │  net scrape target │  │
│  │  by birth hash   │  │  dimensions) │  │                    │  │
│  └──────────────────┘  └──────────────┘  └────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Boundary |
|-----------|----------------|----------|
| Input Form | Collect birth data (date, time, gender), route to backend | Frontend only — no logic |
| Result Page | Display chart visualization, dimension nav, shareable URL | Frontend rendering + state |
| Dimension Detail Page | Trigger on-demand AI generation, consume SSE stream, render text | Frontend + SSE consumer |
| Scraper Module | POST birth data to cohoc.net, parse HTML response to la so struct | Backend only — isolated |
| Lunar Converter | Convert Duong lich → Am lich for Tu Vi calculations | Backend pure function |
| Scoring Engine | Apply lookup tables to la so placements, produce scores + alerts | Backend pure function |
| AI Engine | Build dimension prompt (KB + scores + alerts), call Claude API, stream | Backend orchestrator |
| Cache Layer | Hash birth inputs, store/retrieve la so + scores, skip repeat scrapes | Backend persistence |
| Knowledge Base | 7 markdown files (one per dimension) + core/star reference files | Static files, read at runtime |

## Recommended Project Structure

```
tuvi-app/
├── frontend/                    # Next.js application
│   ├── app/
│   │   ├── page.tsx             # Landing + input form
│   │   ├── result/[id]/
│   │   │   ├── page.tsx         # Chart + dimension overview
│   │   │   └── [dimension]/
│   │   │       └── page.tsx     # Dimension detail + streaming
│   │   └── layout.tsx
│   ├── components/
│   │   ├── chart/               # Chart.js/Recharts wrappers
│   │   ├── stream/              # SSE consumer, streaming text renderer
│   │   └── ui/                  # Shared UI primitives
│   └── lib/
│       └── api.ts               # Backend API client
│
└── backend/                     # FastAPI application
    ├── main.py                  # App entry, router registration
    ├── routers/
    │   ├── chart.py             # POST /chart — scrape + score + cache
    │   └── luangiai.py          # GET /luangiai/{id}/{dimension} — SSE stream
    ├── services/
    │   ├── scraper.py           # cohoc.net scraper (isolated, replaceable)
    │   ├── lunar.py             # Duong/Am lich conversion
    │   ├── scoring.py           # Scoring engine (port from Google Sheets)
    │   ├── alerts.py            # Alert detection (sao combination rules)
    │   └── ai_engine.py        # Prompt construction + Claude API streaming
    ├── knowledge_base/
    │   ├── su_nghiep.md
    │   ├── tien_bac.md
    │   ├── hon_nhan.md
    │   ├── suc_khoe.md
    │   ├── dat_dai.md
    │   ├── hoc_tap.md
    │   ├── con_cai.md
    │   └── core_stars.md        # Shared star reference for all dimensions
    ├── models/
    │   ├── laso.py              # Pydantic: la so structure
    │   ├── scores.py            # Pydantic: scoring output
    │   └── chart.py             # Pydantic: full chart response
    ├── db/
    │   └── cache.py             # SQLite cache (hash → stored result)
    └── config.py                # Env vars, API keys
```

### Structure Rationale

- **services/ vs routers/:** Routers handle HTTP concerns only. Services contain all domain logic. This makes scraper, scoring, and AI engine independently testable and swappable.
- **knowledge_base/ in backend:** KB files are read by the AI engine at generation time — they live close to the service that uses them, not in a separate shared directory.
- **frontend/app/result/[id]/:** The `id` is a hash of birth data (e.g., MD5 of normalized inputs). This enables shareable URLs with no auth, and direct cache lookup on the backend.
- **stream/ component group:** SSE consumption is complex enough to warrant its own component group — handles connection, reconnect, accumulation, and skeleton-to-text transition.

## Architectural Patterns

### Pattern 1: Request-Response Split (Chart vs. Luan Giai)

**What:** Two distinct backend calls with different latency profiles. Chart generation (scrape + score) is a single blocking request returning a JSON payload. Luan giai (AI generation) is a streaming long-poll per dimension, triggered on demand.

**When to use:** Any time latency profiles differ significantly between data types. Chart: ~2-5s, predictable. Luan giai: ~5-20s per dimension, unbounded.

**Trade-offs:** More endpoints, more frontend state management. But allows result page to load and show the chart before any AI generation begins.

**Example:**
```
POST /api/chart          → Returns full la so + scores + alerts as JSON
GET  /api/luangiai/{id}/{dimension}  → Returns SSE stream of narrative text
```

### Pattern 2: Inline Knowledge Base Injection (No RAG)

**What:** For each dimension request, load the full dimension-specific markdown file + core/star reference into the system prompt. KB fits in Claude's context window (~5-10K tokens per dimension file, well within 200K limit).

**When to use:** When KB is small, well-curated, and domain-specific. RAG adds latency, infrastructure complexity, and embedding maintenance cost. For MVP with 7 known files, inline injection is correct.

**Trade-offs:** Full KB is injected every request (marginal cost). In exchange: no vector DB, no embedding pipeline, no retrieval failures, no chunking edge cases.

**Example:**
```python
# In ai_engine.py
def build_prompt(dimension: str, scores: dict, alerts: list, laso: dict) -> str:
    kb_content = load_kb_file(dimension)     # read markdown file
    core_content = load_kb_file("core_stars")
    return SYSTEM_PROMPT_TEMPLATE.format(
        kb=kb_content,
        core=core_content,
        scores=scores,
        alerts=alerts,
        laso=laso
    )
```

### Pattern 3: Birth Data Hash as Cache Key + Shareable ID

**What:** Normalize birth inputs (date, time, gender), hash with MD5/SHA256, use hash as both the SQLite cache key and the URL segment (`/result/{hash}`). Identical birth data = cache hit = instant result.

**When to use:** Any stateless system where inputs are deterministic and outputs are expensive to recompute. Avoids auth entirely for MVP.

**Trade-offs:** Hash collisions are astronomically unlikely for this input space. No user identity, no session — if someone loses the URL, they re-enter data. Acceptable for MVP test group.

**Example:**
```python
import hashlib
def birth_hash(date: str, time: str, gender: str) -> str:
    normalized = f"{date}|{time}|{gender}".lower().strip()
    return hashlib.sha256(normalized.encode()).hexdigest()[:16]
```

### Pattern 4: On-Demand Dimension Generation (Lazy Trigger)

**What:** The result page loads chart data immediately. Each dimension section starts as a locked/preview state. When user clicks a dimension tab, a frontend request triggers SSE stream for that dimension only. Generation does not start until user interaction.

**When to use:** When AI generation is expensive (latency + cost) and users may not read all 7 dimensions. Progressive disclosure: show chart first, generate narrative only when requested.

**Trade-offs:** First dimension feels slow (5-20s wait). Mitigation: show skeleton loader with streaming text appearing in real-time. Pre-fetching the first dimension (su nghiep) on result page load is a valid enhancement.

### Pattern 5: Scraper Isolation + Circuit Breaker

**What:** The cohoc.net scraper is isolated behind a single service interface. A circuit breaker pattern wraps outbound calls: after N consecutive failures, the breaker opens and returns a cached result or a clear error state rather than hanging.

**When to use:** Any external dependency you do not control. cohoc.net is the highest single-point-of-failure risk in this system.

**Trade-offs:** Adds state tracking logic. Necessary given cohoc.net has no SLA.

```python
# services/scraper.py — simplified structure
MAX_RETRIES = 3
TIMEOUT_SECONDS = 10

async def fetch_laso(birth_data: BirthData) -> LasoResult:
    for attempt in range(MAX_RETRIES):
        try:
            response = await httpx.post(COHOC_URL, data=..., timeout=TIMEOUT_SECONDS)
            return parse_laso_html(response.text)
        except (httpx.TimeoutException, ParseError) as e:
            if attempt == MAX_RETRIES - 1:
                raise ScraperUnavailableError(str(e))
            await asyncio.sleep(2 ** attempt)  # exponential backoff
```

## Data Flow

### Primary Flow: First Visit (No Cache Hit)

```
User enters birth data (frontend)
    ↓ POST /api/chart {date, time, gender}
FastAPI router → birth_hash()
    ↓ cache miss
Scraper → cohoc.net → HTML response → parse_laso()
    ↓
Lunar Converter → am_lich from duong_lich
    ↓
Scoring Engine → scores[7 dimensions] + alerts[]
    ↓
SQLite cache.write(hash, laso, scores, alerts)
    ↓ JSON response
Next.js result page renders chart (Chart.js)
    ↓ shareable URL: /result/{hash}

[User clicks "Su Nghiep" dimension tab]
    ↓ GET /api/luangiai/{hash}/su_nghiep
AI Engine → load KB file → build_prompt() → Claude API stream
    ↓ SSE events: text_delta chunks
Frontend SSE consumer → accumulate text → render in real-time
```

### Secondary Flow: Cache Hit (Repeat Visitor)

```
User enters birth data
    ↓ POST /api/chart
birth_hash() → cache.read(hash) → HIT
    ↓ JSON response (sub-100ms)
Result page renders immediately
[AI generation still on-demand per dimension]
```

### SSE Streaming Detail

```
FastAPI StreamingResponse (text/event-stream)
    ↓ async generator
    → "data: {text chunk}\n\n"  (per token or small batch)
    → "data: [DONE]\n\n"        (signal completion)

Frontend EventSource or fetch + ReadableStream
    → accumulate chunks into state
    → React re-render on each chunk (streaming text effect)
    → on [DONE]: mark dimension complete, enable share
```

### Key Data Flows

1. **Birth data → La so:** Scraper is the only path. No fallback computation exists — if cohoc.net is down and no cache exists, return error. This is the primary fragility point.

2. **La so → Scores:** Pure deterministic function (ported from Google Sheets). No external calls. Always succeeds if la so is valid.

3. **Scores + KB → Narrative:** Claude API call. Dependent on Anthropic uptime. Fail independently from chart data — chart always loads, narrative may fail per dimension.

4. **State sharing:** No server-side session. All shareable state lives in the URL hash. Frontend may cache dimension narratives in sessionStorage to avoid re-fetching on tab switch.

## Scaling Considerations

| Scale | Architecture Adjustments |
|-------|--------------------------|
| 0-50 users (MVP test group) | SQLite cache is sufficient. Single Railway instance. No queue needed. |
| 50-1K users | SQLite can handle concurrent reads. Add connection pooling. Monitor cohoc.net rate limits. |
| 1K-10K users | Migrate cache to Postgres. Add Redis for in-flight deduplication (same birth data submitted simultaneously). Rate-limit AI calls per IP. |
| 10K+ users | Introduce job queue (Celery/RQ) for AI generation. SSE becomes WebSocket with horizontal scaling. Cohoc.net dependency becomes untenable — need own la so computation. |

### Scaling Priorities

1. **First bottleneck: cohoc.net scraper.** At scale, concurrent scrapes will be rate-limited or blocked. Fix: cache aggressively, add user-agent rotation, eventually replace with own la so algorithm.

2. **Second bottleneck: Claude API cost/latency.** Each dimension generation is a separate API call. At scale, implement generation queue with per-user limits and cost controls.

## Anti-Patterns

### Anti-Pattern 1: Generating All 7 Dimensions Upfront

**What people do:** Trigger all 7 AI generation calls on result page load to "pre-load" content.

**Why it's wrong:** 7 concurrent Claude API calls per user. High cost, high latency, high failure surface. Most users will not read all 7 dimensions.

**Do this instead:** Generate on-demand when user clicks a dimension. Optionally pre-fetch the most common first dimension (su nghiep) after chart loads, as a single background call.

### Anti-Pattern 2: Storing Luan Giai in the Database

**What people do:** Cache the AI-generated narrative text alongside the la so in the database.

**Why it's wrong:** Narratives are long (1-3K tokens each × 7 dimensions = significant storage). They also become stale when prompts or KB evolve. The correct cache boundary is la so + scores, not AI output.

**Do this instead:** Cache la so + scores (deterministic, compact). Re-generate narratives on demand each session. If caching narratives is later needed, use a short TTL (24h) with explicit invalidation on KB changes.

### Anti-Pattern 3: Putting Scoring Logic in the Frontend

**What people do:** Move scoring tables to JavaScript to avoid a backend round-trip.

**Why it's wrong:** Scoring logic is the validated domain asset (sourced from expert-reviewed Google Sheets). It must remain in Python, testable, version-controlled, and single-source-of-truth. Frontend exposure also creates IP risk.

**Do this instead:** Scoring is a pure Python function in the backend. Frontend receives only pre-computed scores as numbers.

### Anti-Pattern 4: RAG for the Knowledge Base

**What people do:** Build a vector embedding pipeline, chunk KB files, embed into a vector store, query at generation time.

**Why it's wrong:** Overkill. The entire KB (7 dimension files + core_stars.md) is ~20-40K tokens total — well within Claude's 200K context window. RAG adds embedding latency, infrastructure cost, and retrieval failures for no benefit at this scale.

**Do this instead:** Load the full relevant dimension markdown file + core_stars reference inline in the system prompt. If KB grows beyond ~100K tokens, re-evaluate.

### Anti-Pattern 5: Hardcoding cohoc.net HTML Selectors

**What people do:** Scatter CSS selectors or XPath strings throughout the scraping code.

**Why it's wrong:** cohoc.net can change its HTML at any time. When it does, every hardcoded selector breaks simultaneously.

**Do this instead:** Isolate all selectors in a single configuration dict or class. Add HTML structure validation (assert expected elements exist before parsing). Write integration tests against saved HTML snapshots so breakage is detected immediately, not at user request time.

## Integration Points

### External Services

| Service | Integration Pattern | Notes |
|---------|---------------------|-------|
| cohoc.net | HTTP POST via httpx (async), parse HTML with BeautifulSoup | Retry 3x with exponential backoff. Cache result aggressively. No SLA — circuit breaker recommended. |
| Claude API (Anthropic) | anthropic Python SDK, `client.messages.stream()`, yield SSE chunks | Use `claude-sonnet-*` model. Stream text deltas directly to frontend. Per-dimension prompt, inline KB injection. |
| Vercel (frontend host) | Standard Next.js deployment — no special integration needed | Free tier sufficient for MVP. |
| Railway (backend host) | FastAPI as Python process, PORT env var for binding | Starter plan sufficient. Add ANTHROPIC_API_KEY as env secret. |

### Internal Boundaries

| Boundary | Communication | Notes |
|----------|---------------|-------|
| Frontend ↔ Backend (chart) | REST JSON over HTTPS | POST birth data, receive la so + scores + alerts |
| Frontend ↔ Backend (narrative) | Server-Sent Events (SSE) over HTTPS | GET per dimension, stream text chunks |
| Scraper ↔ Cache | Direct function call within backend | Check cache before any HTTP request to cohoc.net |
| Scoring ↔ Scraper | Direct function call — scraper output is scoring input | No async needed, both synchronous pure functions |
| AI Engine ↔ KB files | File system read at generation time | Files are static — load once per request, no hot-reload needed |
| AI Engine ↔ Claude API | Anthropic Python SDK async stream | Wrap in try/except for API errors, emit error SSE event on failure |

## Build Order Implications

The dependency graph determines implementation sequence:

```
1. Lunar Converter          (no deps, pure function — validate first)
2. Scraper Module           (depends on cohoc.net target being understood)
3. Scoring Engine           (depends on scraper output structure + Google Sheets port)
4. Cache Layer              (depends on scraper + scoring — wrap them)
5. FastAPI chart endpoint   (assembles 2+3+4, returns JSON)
6. Knowledge Base files     (expert session 1: author/curate 7 markdown files)
7. AI Engine                (depends on KB + scoring output structure)
8. FastAPI luangiai endpoint (assembles 5+7, wraps in SSE)
9. Next.js frontend         (depends on both API endpoints being defined)
10. Chart visualization      (depends on scores structure from step 3)
11. SSE consumer component   (depends on step 8 streaming protocol)
```

**Critical path:** Scraper → Scoring → Chart API endpoint → Frontend result page. This is the minimum path to a working demo. AI generation (steps 6-8) can be developed in parallel once the la so data structure is defined.

**Parallel track:** Knowledge Base authoring (step 6) is expert-dependent, not engineering-dependent. Start this in parallel with steps 2-4. Schedule expert session 1 immediately after la so structure is defined (after step 2).

## Sources

- [Streaming APIs with FastAPI and Next.js - Sahan Serasinghe](https://sahansera.dev/streaming-apis-python-nextjs-part1/)
- [Claude API Streaming Documentation](https://platform.claude.com/docs/en/build-with-claude/streaming)
- [Effective Context Engineering for AI Agents - Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [How I built an AI SaaS with Next.js, FastAPI, and Dokploy](https://dev.to/julykk/how-i-built-an-ai-saas-with-nextjs-fastapi-and-dokploy-52eo)
- [Building a streaming LLM with Next.js, FastAPI and Docker](https://jaqpot.org/blog/run-and-deploy-an-llm)
- [Claude Structured Outputs Documentation](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
- [Circuit Breaker Pattern in Python](https://medium.com/@ya.lishinskiy2017/circuit-breaker-pattern-in-python-1602902ef143)
- [Exception Handling for Robust Web Scraping](https://scrapingant.com/blog/python-exception-handling)

---
*Architecture research for: Vietnamese Tu Vi AI interpretation system (Kinh Dich x Tu Vi)*
*Researched: 2026-03-23*
