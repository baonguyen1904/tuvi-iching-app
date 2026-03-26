# ARCHITECTURE.md — Technical Architecture
## Decisions made. Don't debate — build.

---

## 1. SYSTEM OVERVIEW

```
┌──────────────────────────────────────────────────────────┐
│                      FRONTEND                             │
│                   Next.js (Vercel)                         │
│                                                           │
│  Landing ─→ Form ─→ Processing ─→ Result ─→ Detail       │
│   page       page    (polling)     page      page         │
└────────────────────────┬─────────────────────────────────┘
                         │ REST API
                         ▼
┌──────────────────────────────────────────────────────────┐
│                      BACKEND                              │
│                  Python FastAPI (Railway)                  │
│                                                           │
│  ┌─────────┐  ┌─────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Scraper  │→│ Scoring  │→│ AI Engine │→│  Cache   │  │
│  │Playwright│  │ Engine   │  │ Claude    │  │ SQLite   │  │
│  └─────────┘  └─────────┘  └──────────┘  └──────────┘  │
│                                 ↑                         │
│                          ┌──────────┐                     │
│                          │   KB     │                     │
│                          │ Markdown │                     │
│                          │  files   │                     │
│                          └──────────┘                     │
└──────────────────────────────────────────────────────────┘
```

---

## 2. TECH STACK

| Layer | Choice | Version | Why |
|-------|--------|---------|-----|
| Frontend framework | Next.js (App Router) | 15.x | SSR for SEO landing page, React ecosystem |
| Frontend language | TypeScript | 5.x | Type safety, better DX with Claude Code |
| Styling | Tailwind CSS | 4.x | Rapid UI, consistent design system |
| Charts | Recharts | 2.x | React-native charts, responsive, well-documented |
| Backend framework | FastAPI | 0.110+ | Async, fast, auto-docs, Python ecosystem |
| Backend language | Python | 3.11+ | Existing scraper/scoring logic, async support |
| Scraper | Playwright | latest | Async, headless, better than Selenium |
| AI model | Claude Sonnet | claude-sonnet-4-20250514 | Vietnamese quality, 200K context window |
| AI approach | Structured prompt + inline KB | — | No RAG needed, KB < 100K tokens |
| Database | SQLite | 3 | MVP caching only, zero config |
| Deploy frontend | Vercel | — | Next.js native, free tier |
| Deploy backend | Railway | — | Python hosting, easy deploy, free/cheap |

---

## 3. API CONTRACT

### 3.1 POST `/api/generate`

Start the full pipeline: scrape → score → AI generate all dimensions.

**Request:**
```json
{
  "birthDate": "1968-04-20",
  "birthHour": "ty",
  "gender": "female",
  "name": "Nguyễn Thị A"
}
```

`birthHour` enum: `ty`, `suu`, `dan`, `mao`, `thin`, `ty_`, `ngo`, `mui`, `than`, `dau`, `tuat`, `hoi`

**Response (immediate):**
```json
{
  "profileId": "abc123def",
  "status": "processing"
}
```

**Backend flow:**
1. Check cache → if hit, return immediately with status "completed"
2. If miss → start async background task:
   a. Scrape cohoc.net → parse lá số
   b. Run scoring engine → scores + alerts
   c. Call Claude API × 8 (1 overview + 7 dimensions)
   d. Save all to SQLite
   e. Mark status "completed"

---

### 3.2 GET `/api/profile/{profileId}/status`

Poll for completion status.

**Response (processing):**
```json
{
  "profileId": "abc123def",
  "status": "processing",
  "step": "ai_generating",
  "progress": 4,
  "totalSteps": 8,
  "message": "Đang phân tích sự nghiệp..."
}
```

**Response (completed):**
```json
{
  "profileId": "abc123def",
  "status": "completed"
}
```

**Response (failed):**
```json
{
  "profileId": "abc123def",
  "status": "failed",
  "error": "scraper_timeout",
  "message": "Hệ thống đang bận, vui lòng thử lại sau 5 phút"
}
```

---

### 3.3 GET `/api/profile/{profileId}`

Get full profile data (after completed).

**Response:**
```json
{
  "profileId": "abc123def",
  "name": "Nguyễn Thị A",
  "birthDate": "1968-04-20",
  "birthDateLunar": "Mậu Thân, tháng 3 ...",
  "birthHour": "Giờ Tý",
  "gender": "Nữ",
  "cungMenh": "Thiên Đồng",
  "nguHanh": "Thổ",
  
  "overview": {
    "chartData": { ... },
    "summary": "AI generated overview text..."
  },
  
  "dimensions": {
    "su_nghiep": {
      "label": "Sự nghiệp",
      "icon": "briefcase",
      "summaryScore": 72,
      "lifetimeChart": {
        "labels": ["10-20", "20-30", "30-40", ...],
        "duong": [5, 12, 18, ...],
        "am": [-3, -5, -8, ...],
        "tb": [3, 8, 10, ...]
      },
      "decadeChart": {
        "labels": ["2023", "2024", "2025", ...],
        "duong": [15, 12, 20, ...],
        "am": [-5, -8, -3, ...],
        "tb": [10, 8, 14, ...]
      },
      "alerts": [
        {
          "type": "positive",
          "year": "2025",
          "tag": "có bước thăng tiến hoặc đạt được sự công nhận"
        },
        {
          "type": "negative",
          "year": "2027",
          "tag": "cẩn thận tiểu nhân, thị phi trong công việc"
        }
      ],
      "interpretation": "AI generated full luận giải text (markdown format)..."
    },
    "tien_bac": { ... },
    "hon_nhan": { ... },
    "suc_khoe": { ... },
    "dat_dai": { ... },
    "hoc_tap": { ... },
    "con_cai": { ... }
  },
  
  "createdAt": "2026-03-26T10:30:00Z"
}
```

---

## 4. DATA FLOW DETAIL

### 4.1 Scraper Pipeline

```
Input: birthDate, birthHour, gender
  ↓
Playwright (headless Chromium)
  → Navigate to tuvi.cohoc.net/lap-la-so-tu-vi.html
  → Fill form: ngày, tháng, năm, giờ, giới tính
  → Submit
  → Wait for result page
  → Extract HTML
  ↓
HTML Parser (BeautifulSoup / lxml)
  → Parse 12 cung elements
  → For each cung: extract sao names
  → Extract metadata: cung mệnh, ngũ hành, âm lịch info
  ↓
Output: LasoData {
  cungMenh: str,
  nguHanh: str,
  lunarInfo: str,
  cungs: [
    { name: "Mệnh", stars: ["Thiên Đồng", "Tả Phù", ...] },
    { name: "Phụ Mẫu", stars: [...] },
    ...12 cungs
  ]
}
```

### 4.2 Scoring Pipeline

```
Input: LasoData
  ↓
Load lookup table: laso_points.csv
  → Each row: star_name | dimension | duong_points | am_points | tb_points | alert_tag
  ↓
For each dimension (7):
  For each time_horizon (lifetime, decade, monthly):
    For each time_period:
      → Sum duong/am/tb points from stars in relevant cungs
      → Check alert triggers
  ↓
Output: ScoringResult {
  dimensions: {
    su_nghiep: {
      lifetime: [{period: "10-20", duong: 5, am: -3, tb: 3}, ...],
      decade: [{period: "2023", duong: 15, am: -5, tb: 10}, ...],
      monthly: [{period: "2026-01", duong: 8, am: -2, tb: 6}, ...],
      alerts: [{type: "positive", period: "2025", tag: "..."}, ...]
    },
    ...7 dimensions
  }
}
```

### 4.3 AI Generation Pipeline

```
For each dimension + overview (8 total):
  ↓
Build prompt:
  1. System prompt (role + rules + output format)
  2. KB content (load /knowledge_base/dimensions/{dim}.md)
  3. KB core (load /knowledge_base/core/scoring_rules.md)
  4. User data (name, birth info, cung menh, relevant sao)
  5. Score data (lifetime + decade + monthly for this dimension)
  6. Alerts (for this dimension)
  ↓
Call Claude Sonnet API
  model: claude-sonnet-4-20250514
  max_tokens: 2000
  temperature: 0.7
  ↓
Parse response → structured text (markdown)
  ↓
Save to SQLite
```

**Parallelization:** Generate all 8 calls concurrently (asyncio.gather). Estimated total time: ~15-25 seconds.

---

## 5. DATABASE SCHEMA (SQLite)

```sql
CREATE TABLE profiles (
  id TEXT PRIMARY KEY,              -- hash(birthDate+birthHour+gender)
  name TEXT,
  birth_date TEXT NOT NULL,
  birth_hour TEXT NOT NULL,
  gender TEXT NOT NULL,
  lunar_info TEXT,
  cung_menh TEXT,
  ngu_hanh TEXT,
  laso_data JSON NOT NULL,          -- full 12 cung × sao
  scores JSON NOT NULL,             -- all dimensions × all time horizons
  overview_summary TEXT,            -- AI generated overview
  interpretations JSON NOT NULL,    -- {dimension: markdown_text}
  status TEXT DEFAULT 'processing', -- processing | completed | failed
  current_step TEXT,                -- scraping | scoring | ai_generating
  ai_progress INTEGER DEFAULT 0,   -- 0-8 (how many AI calls done)
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  completed_at TIMESTAMP
);
```

**Cache key strategy:**
- `id` = SHA256(birthDate + birthHour + gender)[:12]
- Name is NOT part of cache key (same chart regardless of name)
- Name is stored separately, used only in AI text generation

---

## 6. KNOWLEDGE BASE FILE STRUCTURE

```
backend/knowledge_base/
├── core/
│   ├── scoring_rules.md          # Cách đọc Dương/Âm/TB scores
│   ├── alert_interpretation.md   # Cách interpret 🔺🔻 alerts
│   └── tone_guidelines.md        # Nguyên tắc ngôn ngữ + ethics
│
├── dimensions/
│   ├── su_nghiep.md
│   ├── tien_bac.md
│   ├── hon_nhan.md
│   ├── suc_khoe.md
│   ├── dat_dai.md
│   ├── hoc_tap.md
│   └── con_cai.md
│
├── stars/
│   ├── chinh_tinh.md             # 14 chính tinh meanings + scoring
│   └── phu_tinh.md               # Phụ tinh meanings
│
└── examples/
    └── approved_outputs/         # Expert-approved example luận giải
        ├── su_nghiep_sample.md
        └── tien_bac_sample.md
```

**Total KB per AI call:** ~5-10K tokens (well within 200K context window)

---

## 7. FRONTEND ARCHITECTURE

### Next.js App Router Structure

```
frontend/
├── app/
│   ├── layout.tsx                # Root layout, fonts, metadata
│   ├── page.tsx                  # Landing page (marketing)
│   ├── form/
│   │   └── page.tsx              # Input form
│   ├── processing/
│   │   └── [id]/
│   │       └── page.tsx          # Processing screen (poll status)
│   └── result/
│       └── [id]/
│           ├── page.tsx          # Result overview
│           └── [dimension]/
│               └── page.tsx      # Dimension detail
│
├── components/
│   ├── ui/                       # Reusable UI primitives
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── Input.tsx
│   │   └── ...
│   ├── landing/                  # Landing page sections
│   │   ├── Hero.tsx
│   │   ├── HowItWorks.tsx
│   │   ├── DimensionsPreview.tsx
│   │   ├── TrustSection.tsx
│   │   └── FAQ.tsx
│   ├── charts/                   # Chart components
│   │   ├── LifetimeChart.tsx
│   │   ├── DecadeChart.tsx
│   │   └── OverviewChart.tsx
│   ├── BirthForm.tsx
│   ├── ProcessingStatus.tsx
│   ├── DimensionCard.tsx
│   └── InterpretationView.tsx
│
├── lib/
│   ├── api.ts                    # API client functions
│   ├── constants.ts              # Dimension names, icons, colors
│   └── types.ts                  # TypeScript interfaces
│
└── public/
    └── images/                   # Landing page assets
```

### Design System (Tailwind)

- **Font:** Inter (body) + optional serif for Vietnamese (Playfair Display or similar)
- **Colors:**
  - Background: `#FAFAFA` (light gray-white)
  - Surface: `#FFFFFF`
  - Text primary: `#1A1A1A`
  - Text secondary: `#6B7280`
  - Accent: `#2563EB` (blue) — modern, trustworthy
  - Positive alert: `#10B981` (green)
  - Negative alert: `#F59E0B` (amber, NOT red — less scary)
  - Border: `#E5E7EB`
- **Spacing:** 8px grid
- **Border radius:** 8px (cards), 6px (buttons), 4px (inputs)
- **Shadows:** subtle, 1 level only (`shadow-sm`)

---

## 8. DEPLOYMENT

### Frontend (Vercel)
- Connect GitHub repo → auto-deploy on push
- Environment: `NEXT_PUBLIC_API_URL` → Railway backend URL
- Domain: TBD (use Vercel subdomain for MVP)

### Backend (Railway)
- Dockerfile-based deploy
- Environment variables:
  - `ANTHROPIC_API_KEY` — Claude API key
  - `ALLOWED_ORIGINS` — Frontend URL for CORS
- Playwright needs Chromium binary → include in Docker image
- SQLite file persisted via Railway volume

### Cost Estimate (MVP)
- Vercel: Free tier (sufficient)
- Railway: ~$5/month (Starter plan)
- Claude API: ~$0.05-0.10 per profile (8 calls × ~5K input tokens + ~1K output tokens)
  - 50 test users = ~$5 total
- **Total MVP cost: ~$10-15**