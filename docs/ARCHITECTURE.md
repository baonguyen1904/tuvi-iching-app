# ARCHITECTURE.md — Technical Architecture
## Updated based on existing codebase analysis

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
│  ┌───────────┐   ┌───────────┐                           │
│  │ Scraper A  │   │ Scraper B  │                          │
│  │ cohoc.net  │   │ tuvi.vn    │                          │
│  │ Playwright │   │ Playwright │                          │
│  │ (lifetime  │   │ (monthly)  │                          │
│  │  + 10yr)   │   │            │                          │
│  └─────┬──────┘   └─────┬──────┘                         │
│        └───────┬─────────┘                                │
│                ▼                                          │
│         ┌──────────┐                                      │
│         │ Scoring   │← laso_points.xlsx                   │
│         │ Engine    │  (222 stars, 8 dimensions)           │
│         └────┬─────┘                                      │
│              ▼                                            │
│         ┌──────────┐                                      │
│         │ AI Engine │← KB markdown files                  │
│         │ Claude    │                                     │
│         └────┬─────┘                                      │
│              ▼                                            │
│         ┌──────────┐                                      │
│         │  Cache    │                                     │
│         │  SQLite   │                                     │
│         └──────────┘                                      │
└──────────────────────────────────────────────────────────┘
```

---

## 2. TECH STACK

| Layer | Choice | Why |
|-------|--------|-----|
| Frontend | Next.js 15+ (App Router, TypeScript) | SSR for SEO landing page |
| Styling | Tailwind CSS | Rapid UI, consistent design |
| Charts | Recharts | React-native charts, responsive |
| Backend | Python FastAPI | Async, existing Python scoring logic |
| Scraper | Playwright (async, headless) | Migration from Selenium, async-native |
| AI | Claude Sonnet API | Vietnamese quality, 200K context |
| AI approach | Structured prompt + inline KB | No RAG needed for MVP |
| Star matching | python-slugify | Same as existing codebase |
| Database | SQLite | MVP caching only |
| Deploy FE | Vercel | Next.js native |
| Deploy BE | Railway | Python + Playwright hosting |

---

## 3. DATA FLOW — Complete Pipeline

```
[User submits form]
  birth_date, birth_hour, gender, name
     │
     ▼
[Check Cache] ── hit ──→ Return cached result immediately
     │ miss
     ▼
[Scraper A: cohoc.net]                [Scraper B: tuvi.vn]
  POST birth data                       POST birth data + nam_xem
  Wait (up to 90s for cache)            Parse result
  Parse HTML                            Filter d-none stars
  Extract:                              Extract:
    - metadata (menh, cuc, am_duong)      - 12 monthly cungs
    - 12 cung (lifetime)                  - sorted by month
    - 12 cung_10yrs (Đại Vận)
  Star names: parse (Đ)/(H)/(M)
  Slugify all star names
     │                                      │
     └──────────────┬───────────────────────┘
                    ▼
              [LasoData]
              (combined from both sources)
                    │
                    ▼
         [Scoring Engine]
           1. Build cung_point dicts (3 timeframes)
           2. For each of 8 dimensions:
              a. Raw score: Σ(point × weight) per cung
              b. Anchor: weighted sum from key cungs (LIFETIME data)
              c. Final: (raw + anchor) / 2
              d. Alerts: pct_change between periods ≥ 30%/50%
           3. Output: 8 × {lifetime[12] + decade[10] + monthly[13]} scores + alerts
                    │
                    ▼
            [AI Engine]
              8 parallel Claude API calls:
                1 overview + 7 dimension luận giải
              (van_menh may be included or excluded from user-facing content)
              Input per call: system prompt + KB + user data + scores + alerts
                    │
                    ▼
              [Save to SQLite]
              [Mark status: completed]
                    │
                    ▼
              [Frontend polls, gets result]
              [Render charts + AI text]
```

---

## 4. API CONTRACT

### 4.1 POST `/api/generate`

**Request:**
```json
{
  "birthDate": "1994-07-19",
  "birthHour": "dan",
  "gender": "male",
  "name": "Nguyễn Văn A",
  "namXem": 2026
}
```

`birthHour` enum: `ty, suu, dan, mao, thin, ty_, ngo, mui, than, dau, tuat, hoi`

**Response (immediate):**
```json
{
  "profileId": "abc123def456",
  "status": "processing"
}
```

### 4.2 GET `/api/profile/{profileId}/status`

**Response (processing):**
```json
{
  "profileId": "abc123def456",
  "status": "processing",
  "step": "scraping_cohoc",
  "message": "Đang lấy lá số..."
}
```

Steps: `scraping_cohoc` → `scraping_tuvivn` → `scoring` → `ai_generating` (progress 1-8) → `completed`

### 4.3 GET `/api/profile/{profileId}`

**Response:** Full profile data with all dimensions.

```json
{
  "profileId": "abc123def456",
  "name": "Nguyễn Văn A",
  "birthDate": "1994-07-19",
  "birthHour": "Giờ Dần (03:00-05:00)",
  "gender": "Nam",
  "metadata": {
    "nam": "Giáp Tuất",
    "menh": "Mộc",
    "cuc": "Thủy Nhị Cục",
    "amDuong": "Dương Nam",
    "cungMenh": "...",
    "nguHanh": "..."
  },
  "overview": {
    "summary": "AI generated overview..."
  },
  "dimensions": {
    "van_menh": {
      "label": "Vận mệnh",
      "summaryScore": 12.5,
      "lifetime": {
        "labels": [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110],
        "duong": [15.2, 18.4, ...],
        "am": [-8.3, -5.1, ...],
        "tb": [6.9, 13.3, ...]
      },
      "decade": {
        "labels": [2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034, 2035],
        "duong": [...],
        "am": [...],
        "tb": [...]
      },
      "monthly": {
        "labels": ["Th.1/2026", "Th.1/2026", "Th.2/2026", ..., "Th.12/2026"],
        "duong": [...],
        "am": [...],
        "tb": [...]
      },
      "alerts": [],
      "interpretation": null
    },
    "su_nghiep": {
      "label": "Sự nghiệp",
      "summaryScore": 8.7,
      "lifetime": { ... },
      "decade": { ... },
      "monthly": { ... },
      "alerts": [
        {
          "type": "positive",
          "period": "2028",
          "tag": "có bước thăng tiến hoặc đạt được sự công nhận",
          "level": 30,
          "starName": "hoa-cai"
        }
      ],
      "interpretation": "## Tổng quan sự nghiệp\n..."
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

## 5. SCORING ENGINE — Summary of Formulas

### Score Calculation
```
raw_pos(cung, dim) = Σ { point × weight }  for stars with point > 0
raw_neg(cung, dim) = Σ { point × weight }  for stars with point ≤ 0
  where weight = laso_points[dimension_column], default 1 if empty

anchor_pos(dim) = Σ { raw_pos(key_cung) × cung_weight }  from LIFETIME data only
anchor_neg(dim) = Σ { raw_neg(key_cung) × cung_weight }  from LIFETIME data only

Dương = final_pos = (raw_pos + anchor_pos) / 2
Âm    = final_neg = (raw_neg + anchor_neg) / 2
TB    = final_sum = final_pos + final_neg
```

### Alert Detection
```
pct_change = (value[i] - value[i-1]) / |value[i-1]| × 100
For neg column: pct_change *= -1

Level 50: |pct_change| ≥ 50%  (priority)
Level 30: |pct_change| ≥ 30% AND not level 50

Match direction (pos/neg change) with star's pct_fvg_XX value
Lookup tag text from {dimension}_tag_XX column
```

### Data Points per Chart
| Chart | Points | X-axis | Source |
|-------|--------|--------|--------|
| Lifetime | 12 | Ages: 0, 10, 20, ..., 110 | cohoc.net `cung` |
| 10-year | 10 | Years: 2026, 2027, ..., 2035 | cohoc.net `cung_10yrs[:-2]` |
| Monthly | 13 | Th.1, Th.1, Th.2, ..., Th.12 | tuvi.vn `cung_12months` (first prepended) |

---

## 6. DATABASE SCHEMA (SQLite)

```sql
CREATE TABLE profiles (
  id TEXT PRIMARY KEY,
  name TEXT,
  birth_date TEXT NOT NULL,
  birth_hour TEXT NOT NULL,
  gender TEXT NOT NULL,
  nam_xem INTEGER NOT NULL DEFAULT 2026,
  
  -- Scraped data (JSON)
  metadata JSON,               -- nam, menh, cuc, am_duong, etc.
  cung_lifetime JSON,          -- 12 cungs × stars
  cung_10yrs JSON,             -- 12 cungs × stars (Đại Vận)
  cung_12months JSON,          -- 12 monthly cungs × stars
  
  -- Scoring output (JSON)
  scores JSON,                 -- 8 dimensions × 3 timeframes
  alerts JSON,                 -- all triggered alerts
  
  -- AI output
  overview_summary TEXT,
  interpretations JSON,        -- {dimension: markdown_text}
  
  -- Status
  status TEXT DEFAULT 'processing',
  current_step TEXT,
  ai_progress INTEGER DEFAULT 0,
  error_message TEXT,
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  completed_at TIMESTAMP
);

CREATE INDEX idx_profiles_cache ON profiles(birth_date, birth_hour, gender);
```

**Cache key:** `SHA256(birth_date + birth_hour + gender + nam_xem)[:12]`

---

## 7. KNOWLEDGE BASE STRUCTURE

```
backend/knowledge_base/
├── core/
│   ├── scoring_rules.md          # How Dương/Âm/TB work
│   ├── alert_interpretation.md   # How to read 🔺🔻
│   └── tone_guidelines.md        # Language rules + ethics
├── dimensions/
│   ├── van_menh.md               # Added: overall fortune
│   ├── su_nghiep.md
│   ├── tien_bac.md
│   ├── hon_nhan.md
│   ├── suc_khoe.md
│   ├── dat_dai.md
│   ├── hoc_tap.md
│   └── con_cai.md
├── stars/
│   ├── chinh_tinh.md
│   └── phu_tinh.md
└── examples/
    └── approved_outputs/
```

---

## 8. FRONTEND ARCHITECTURE

```
frontend/
├── app/
│   ├── layout.tsx
│   ├── page.tsx                  # Landing page
│   ├── form/page.tsx             # Input form
│   ├── processing/[id]/page.tsx  # Polling + progress
│   └── result/[id]/
│       ├── page.tsx              # Overview + dimension cards
│       └── [dimension]/page.tsx  # Detail (charts + AI text)
├── components/
│   ├── ui/                       # Button, Card, Input, etc.
│   ├── landing/                  # Hero, HowItWorks, FAQ, etc.
│   ├── charts/
│   │   ├── LifetimeChart.tsx     # 12 points, 3 lines + alert markers
│   │   ├── DecadeChart.tsx       # 10 points
│   │   ├── MonthlyChart.tsx      # 13 points (wrapping)
│   │   └── OverviewChart.tsx     # Radar chart, 7-8 dimensions
│   └── ...
├── lib/
│   ├── api.ts
│   ├── types.ts
│   └── constants.ts
```

### Design System
- Modern minimalist (Notion/Linear style)
- Colors: neutral bg, blue accent, green positive alerts, amber negative alerts
- Typography: Inter, 14px base
- Mobile-first, max-width 768px

---

## 9. DEPLOYMENT

### Backend (Railway)
- Docker image with Playwright + Chromium
- Environment: `ANTHROPIC_API_KEY`, `ALLOWED_ORIGINS`
- SQLite on persistent volume
- **Both scrapers need Chromium** — single browser instance shared

### Frontend (Vercel)
- `NEXT_PUBLIC_API_URL` → Railway backend URL

### Cost (MVP)
- Vercel: Free tier
- Railway: ~$5/month
- Claude API: ~$0.05-0.10 per profile (8 calls)
- 50 test users ≈ $5
- **Total: ~$10-15**

---

## 10. KEY DEPENDENCIES (Python)

```
fastapi, uvicorn           # API framework
playwright                 # Browser automation (replacing Selenium)
beautifulsoup4, lxml       # HTML parsing
python-slugify             # Star name matching (CRITICAL: same as existing)
pandas                     # laso_points loading + scoring DataFrames
anthropic                  # Claude API client
python-multipart           # FastAPI form handling
aiosqlite                  # Async SQLite
```

**Note on python-slugify:** This is the EXACT matching mechanism used in the existing codebase. Both sides (laso_points index + scraped star names) must use `slugify(name.lower())` to produce identical slugs.