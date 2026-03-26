# EXPECTED_OUTPUTS.md — Test Expectations

---

## 1. Scraper Output Expectations

### Given valid birth data:
- Returns `LasoData` with exactly 12 cung
- Each cung has a `name` (one of the standard 12 cung names)
- Each cung has ≥ 1 star (most cungs have 2-5 stars)
- `cung_menh` is one of the 12 cung names
- `ngu_hanh` is one of: Kim, Mộc, Thủy, Hỏa, Thổ
- `lunar_info` contains year name (e.g., "Mậu Thân")
- All star names are valid Vietnamese Tử Vi star names

### Given same input twice:
- Returns identical `LasoData` (deterministic)

### Given invalid input:
- Network timeout → raises `ScraperError` within 30s
- Invalid date → raises `ValidationError` before scraping

### Standard 12 Cung Names (expected):
Mệnh, Phụ Mẫu, Phúc Đức, Điền Trạch, Quan Lộc, Nô Bộc (Giao Hữu), Thiên Di, Tật Ách, Tài Bạch, Tử Tức, Phu Thê, Huynh Đệ

---

## 2. Scoring Engine Output Expectations

### Given valid LasoData:
- Returns `ScoringResult` with exactly 7 dimensions
- Each dimension has lifetime scores (≥ 6 data points, roughly ages 10-80)
- Each dimension has decade scores (10 data points, 10 years)
- Each dimension has monthly scores (12 data points)
- Each score point has `duong`, `am`, `tb` values (numbers, can be negative)
- `summary_score` is a single number per dimension

### Alerts:
- Each alert has `type` ("positive" or "negative"), `period`, `tag`
- Tag is a Vietnamese string describing the alert
- Not all dimensions will have alerts — some may have 0

### Validation against Google Sheet:
- For 5 test profiles, scoring output MUST match Sheet output
- Tolerance: ±1 for rounding differences
- Alert triggers must match exactly (same alerts, same periods)

---

## 3. AI Luận Giải Output Expectations

### Per dimension output:
- Language: Vietnamese
- Length: 500-1500 words (approximately 1-2 pages)
- Structure: Contains 4 sections:
  1. "Tổng quan [dimension]" — 3-5 sentences
  2. "Giai đoạn hiện tại" — 2-4 paragraphs
  3. "Các mốc cần chú ý" — 1 entry per alert, each with explanation + advice
  4. "Lời khuyên" — 2-3 bullet points
- Ends with disclaimer text
- Format: Markdown (## headings, paragraphs)

### Tone compliance:
- ✅ Uses "cần thận trọng", "nên lưu ý", "cần cẩn thận"
- ❌ Does NOT use "sẽ gặp họa", "đại nạn", "tai ương", "kiếp nạn"
- ✅ Every 🔻 alert has accompanying advice (what to do / avoid)
- ✅ Empowering tone — user has agency, not fatalistic
- ❌ Does NOT claim certainty ("chắc chắn sẽ xảy ra")
- ✅ Uses hedging ("có xu hướng", "khả năng", "nên phòng tránh")

### Data grounding:
- ✅ References specific time periods from score data
- ✅ References score patterns (high Dương, low Âm, crossover)
- ❌ Does NOT mention stars/cung not present in user's lá số
- ❌ Does NOT invent events, dates, or specifics not in input data

### Overview output:
- Language: Vietnamese
- Length: 3-5 sentences
- Summarizes across all 7 dimensions
- Mentions strongest dimension and most cautious dimension
- Invites reader to explore details

---

## 4. API Response Expectations

### POST /api/generate
- Status 200 with `{ profileId, status: "processing" }`
- profileId is a 12-character alphanumeric string
- Same input → same profileId (cache key)
- Status 400 for invalid input (missing fields, invalid date range)

### GET /api/profile/{id}/status
- While processing: `{ status: "processing", step: "...", progress: N, totalSteps: 8 }`
- When done: `{ status: "completed" }`
- When failed: `{ status: "failed", error: "...", message: "..." }`
- Unknown profileId: Status 404

### GET /api/profile/{id}
- Status 200 with full profile JSON (see ARCHITECTURE.md for schema)
- All 7 dimensions present with scores + interpretation text
- Overview summary present
- Charts data present (lifetime + decade per dimension)
- Status 404 for unknown profileId
- Status 202 if still processing

---

## 5. Frontend Behavior Expectations

### Landing page:
- Renders all 7 sections
- CTA scrolls to form or navigates to /form
- Mobile: all sections stack, no horizontal overflow
- Load time < 3s on simulated 3G

### Form:
- Cannot submit with empty required fields
- Date picker restricts to 1920-2010
- Shows inline validation errors in Vietnamese
- After submit: button shows loading state, form fields disabled
- On API error: shows error message, form re-enables

### Processing:
- Shows current step text
- Updates progress as backend reports
- Redirects to result when complete
- Shows error + retry button on failure
- Handles page refresh (resumes polling)

### Result:
- Displays profile header with birth info
- Overview chart (radar) renders with 7 axes
- AI overview text is readable
- 7 dimension cards visible (2-column grid desktop, 1-column mobile)
- Click dimension → expands with charts + AI text
- Charts have 3 colored lines + alert markers
- Share button copies current URL
- All text is Vietnamese, no English leakage

### Charts:
- Lifetime chart: X = age ranges, Y = scores, 3 lines visible
- Decade chart: X = years, Y = scores, 3 lines visible
- Alert markers visible at correct time points
- Tooltip shows values on hover (desktop) / tap (mobile)
- Responsive: readable at 375px width minimum

---

## 6. End-to-End Flow Expectation

```
User opens landing page
  → Sees hero, how it works, dimensions preview, trust section, FAQ
  → Clicks CTA

User fills form
  → Enters: name, date, hour, gender
  → Clicks submit
  → Sees button loading state

Processing screen
  → Shows step 1: "Đang lấy lá số..."
  → Updates to step 2: "Đang tính toán..."
  → Updates to step 3: "Đang phân tích..." with progress (1/8, 2/8, ...)
  → After ~20-30 seconds: redirects to result

Result page
  → Shows profile header with correct birth info
  → Shows radar chart with 7 dimension scores
  → Shows AI overview (3-5 sentences)
  → Shows 7 clickable dimension cards
  → Click "Sự nghiệp" → expands with:
    - Lifetime chart (score trends across age)
    - Decade chart (10-year detail)
    - AI luận giải text (~500-1000 words)
    - Alert explanations with advice
    - Disclaimer at bottom
  → Click share → URL copied to clipboard
  → Open URL in new browser → same result page loads (cached)
```

---

## 7. Test Fixtures (to be created)

Create JSON fixture files in `/tests/fixtures/`:

| File | Contains | Source |
|------|----------|--------|
| `test_case_1_input.json` | BirthInput for test case 1 | Manual |
| `test_case_1_laso.json` | Expected LasoData from scraper | Scraped + verified manually |
| `test_case_1_scores.json` | Expected ScoringResult | From Google Sheet |
| `test_case_2_input.json` | ... | ... |
| `test_case_2_laso.json` | ... | ... |
| `test_case_2_scores.json` | ... | ... |
| ... (5 test cases total) | | |

**Process to create fixtures:**
1. Go to cohoc.net manually with test birth data
2. Screenshot + record the full lá số
3. Enter same data in Google Sheet → record all scores + alerts
4. Save as structured JSON
5. Use these as ground truth for automated testing