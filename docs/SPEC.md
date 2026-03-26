# SPEC.md — Product Specification
## Tử Vi AI Luận Giải — MVP Phase

**Version:** 1.0
**Date:** 26/03/2026
**Status:** Ready for implementation

---

## 1. PRODUCT OVERVIEW

### What
Web app luận giải tử vi cá nhân hóa bằng AI. User nhập ngày giờ sinh → hệ thống tự động tính lá số, scoring, và sinh luận giải chi tiết cho 7 lĩnh vực đời sống.

### Why (MVP purpose)
- Test chất lượng AI luận giải với khách cũ của expert (~20-50 người)
- Thu thập feedback trước khi build full product
- Validate: AI + KB có thể thay thế/hỗ trợ expert trong luận giải cơ bản không?
- Đồng thời: Landing page full marketing để test positioning & collect leads cho public launch

### Who
- **Primary:** Khách cũ của expert partner (đã tin tưởng, có baseline so sánh)
- **Secondary:** Visitors từ landing page marketing (collect waitlist/leads)

---

## 2. USER FLOW

### Flow A: Direct User (test group)
```
[Nhận link từ expert] → [Landing page] → [CTA "Xem luận giải"] 
→ [Input form] → [Processing 15-30s] → [Result page] 
→ [Click dimension] → [Dimension detail + AI luận giải]
→ [Share link / Feedback survey]
```

### Flow B: Marketing Visitor
```
[Tìm thấy landing page] → [Đọc value proposition] 
→ [CTA "Xem luận giải miễn phí"] → [Input form] → ... same as Flow A
```

### 2.1 Landing Page

**Mục đích:** Bán concept, build trust, drive CTA mạnh. Đây là full marketing page, không chỉ form đơn giản.

**Content blocks (top → bottom):**

1. **Hero Section**
   - Headline: Value proposition chính (placeholder, cần A/B test sau)
     - Option A: "Hiểu vận mệnh — Quản lý rủi ro cuộc sống"
     - Option B: "Luận giải tử vi cá nhân hóa bằng AI"
   - Subheadline: 1 câu mô tả ngắn
   - CTA button: "Xem luận giải miễn phí" → scroll to form hoặc navigate to /form
   - Visual: Abstract/modern illustration (KHÔNG hình mê tín)

2. **How It Works (3 bước)**
   - Bước 1: Nhập ngày giờ sinh
   - Bước 2: AI phân tích lá số & tính điểm
   - Bước 3: Nhận luận giải chi tiết 7 lĩnh vực
   - Visual: Icons hoặc simple illustrations cho mỗi bước

3. **7 Dimensions Preview**
   - Grid/cards hiển thị 7 lĩnh vực: Sự nghiệp, Tiền bạc, Hôn nhân, Sức khỏe, Đất đai, Học tập, Con cái
   - Mỗi card: icon + tên + 1 dòng mô tả ngắn
   - Message: "Mỗi lĩnh vực được phân tích riêng biệt với biểu đồ + lời khuyên cụ thể"

4. **Trust Building**
   - "Dựa trên hệ thống Tử Vi Đẩu Số — không phải xem bói generic"
   - "Knowledge base từ chuyên gia thực chiến 20+ năm kinh nghiệm"
   - "AI phân tích DỮ LIỆU từ lá số của bạn — không bịa đặt"
   - Optional: Expert intro (tên, credentials, ảnh — nếu expert đồng ý)

5. **Sample Output Preview**
   - Screenshot/mockup của result page (blurred hoặc sample data)
   - "Đây là những gì bạn sẽ nhận được"

6. **FAQ Section**
   - "Khác gì xem bói online?"
   - "Có chính xác không?"
   - "Thông tin của tôi có được bảo mật?"
   - "Tại sao cần biết giờ sinh?"
   - "Miễn phí thật không?"

7. **Final CTA**
   - Repeat CTA button
   - "Miễn phí. Không cần đăng ký. Chỉ cần ngày giờ sinh."

**Design direction:** Modern minimalist (Notion/Linear style). Clean typography, generous whitespace, subtle animations on scroll. Tông màu: neutral (white/gray) + 1 accent color. KHÔNG có: hình rồng phượng, font chữ Hán cổ, màu đỏ vàng truyền thống.

---

### 2.2 Input Form

**Route:** `/form` (hoặc inline trên landing page)

**Fields:**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Họ tên | Text input | Optional | Dùng trong luận giải ("Với [Tên], giai đoạn...") |
| Ngày sinh | Date picker (dương lịch) | **Required** | Validate: 1920-2010 (không quá trẻ, không quá già) |
| Giờ sinh | Dropdown (12 canh giờ) | **Required** | Tý (23-1h), Sửu (1-3h), Dần (3-5h), Mão (5-7h), Thìn (7-9h), Tỵ (9-11h), Ngọ (11-13h), Mùi (13-15h), Thân (15-17h), Dậu (17-19h), Tuất (19-21h), Hợi (21-23h) |
| Giới tính | Radio: Nam / Nữ | **Required** | Ảnh hưởng tính toán tử vi |

**"Không biết giờ sinh" handling:**
- Hiển thị tooltip/note nhỏ: "Giờ sinh rất quan trọng trong Tử Vi Đẩu Số vì ảnh hưởng đến cung Mệnh và vị trí các sao. Nếu không biết chính xác, hãy hỏi cha mẹ hoặc xem sổ khai sinh."
- KHÔNG có option "không rõ" — bắt buộc chọn giờ
- Nếu thực sự không biết → không thể xem. Hiển thị message giải thích tại sao

**Validation:**
- Ngày sinh: phải là ngày hợp lệ, trong khoảng 1920-2010
- Giờ sinh: phải chọn 1 trong 12 canh
- Giới tính: phải chọn

**Submit behavior:**
- Disable button, show loading state
- Navigate to processing page `/processing/[profileId]`

---

### 2.3 Processing Screen

**Route:** `/processing/[profileId]`

**UX:** Full-screen processing animation với progress steps:

```
Step 1: "Đang lấy lá số..."              (scrape + parse)     ~3-5s
Step 2: "Đang tính toán điểm số..."       (scoring)            ~1-2s  
Step 3: "Đang phân tích vận mệnh..."      (AI generate all 7)  ~15-25s
Step 4: "Hoàn tất!"                       (redirect)           ~1s
```

**Total wait:** ~20-30 giây (chủ yếu là AI generation cho 7 dimensions)

**Design:** Minimalist animation (spinner hoặc progress bar), mỗi step hiện text thay đổi. Có thể thêm fun facts về Tử Vi trong lúc chờ.

**Backend flow:** 
- POST /api/generate → trả về profileId ngay
- Frontend poll GET /api/profile/{id}/status mỗi 2 giây
- Khi status = "completed" → redirect to result page

**Error handling:**
- Nếu scraper fail → retry 1 lần, nếu vẫn fail → hiện error "Hệ thống đang bận, vui lòng thử lại sau 5 phút"
- Nếu AI fail → hiện charts + scores nhưng note "Luận giải đang được xử lý, vui lòng quay lại sau"

---

### 2.4 Result Page

**Route:** `/result/[profileId]`

**Layout:**

```
┌─────────────────────────────────────────┐
│ Header                                   │
│ ─────────────────────────────────────── │
│ Chánh Ngã Đồ — [Tên hoặc "Bạn"]        │
│ Sinh: 20/04/1968 (Mậu Thân), 17h, Nữ   │
│ Cung Mệnh: [X] — Mệnh [Ngũ Hành]       │
├─────────────────────────────────────────┤
│                                          │
│ Biểu đồ tổng quan                       │
│ [Overview chart — all dimensions]        │
│                                          │
├─────────────────────────────────────────┤
│                                          │
│ Tổng quan vận mệnh                      │
│ [AI generated overview — 3-5 câu]       │
│                                          │
├─────────────────────────────────────────┤
│                                          │
│ Chọn lĩnh vực xem chi tiết:             │
│                                          │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│ │ 💼        │ │ 💰        │ │ 💑        │ │
│ │ Sự nghiệp │ │ Tiền bạc  │ │ Hôn nhân │ │
│ │ Score: 72 │ │ Score: 58 │ │ Score: 85│ │
│ └──────────┘ └──────────┘ └──────────┘ │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│ │ 🏥        │ │ 🏠        │ │ 📚        │ │
│ │ Sức khỏe  │ │ Đất đai   │ │ Học tập  │ │
│ │ Score: 64 │ │ Score: 71 │ │ Score: 69│ │
│ └──────────┘ └──────────┘            │ │
│ ┌──────────┐                          │ │
│ │ 👶        │                          │ │
│ │ Con cái   │                          │ │
│ │ Score: 77 │                          │ │
│ └──────────┘                          │ │
│                                          │
├─────────────────────────────────────────┤
│ Footer: Disclaimer + Share button        │
└─────────────────────────────────────────┘
```

**Dimension cards:**
- Icon + tên dimension
- Summary score (aggregate lifetime score hoặc current period score)
- Click → navigate to dimension detail (same page scroll hoặc `/result/[id]/[dimension]`)
- Visual indicator nếu có alert 🔺🔻 trong current period

**Share:**
- "Chia sẻ kết quả" button → copy link to clipboard
- Link format: `[domain]/result/[profileId]` (publicly accessible, no login)

---

### 2.5 Dimension Detail Page

**Route:** `/result/[profileId]/[dimension]` (hoặc anchor section trong result page)

**Layout:**

```
┌─────────────────────────────────────────┐
│ ← Quay lại tổng quan                    │
│                                          │
│ Luận giải Sự Nghiệp — [Tên]            │
├─────────────────────────────────────────┤
│                                          │
│ Biểu đồ cả đời                          │
│ [Lifetime chart — Dương/Âm/TB lines]    │
│ [Alert markers 🔺🔻 on chart]           │
│                                          │
│ Biểu đồ 10 năm gần nhất                │
│ [Decade chart — Dương/Âm/TB lines]      │
│ [Alert markers]                          │
│                                          │
├─────────────────────────────────────────┤
│                                          │
│ ── AI Luận Giải ──                       │
│                                          │
│ ## Tổng quan sự nghiệp                  │
│ [AI text — 3-5 câu overview]            │
│                                          │
│ ## Giai đoạn hiện tại (2023-2032)       │
│ [AI text — decade analysis]              │
│                                          │
│ ## Các mốc cần chú ý                    │
│ 🔺 2025: [alert title]                  │
│    [AI expanded explanation + advice]    │
│                                          │
│ 🔻 2027: [alert title]                  │
│    [AI expanded explanation + advice]    │
│                                          │
│ ## Lời khuyên                            │
│ [2-3 actionable recommendations]         │
│                                          │
│ ── Disclaimer ──                         │
│ "Đây là luận giải tham khảo dựa trên   │
│  Tử Vi Đẩu Số. Mọi quyết định cuối    │
│  cùng là của bạn."                       │
│                                          │
├─────────────────────────────────────────┤
│ [← Prev dimension]  [Next dimension →]  │
└─────────────────────────────────────────┘
```

---

## 3. BUSINESS RULES

### 3.1 Lá Số Generation

- Dương lịch → Âm lịch conversion: handled by cohoc.net (scraper)
- Input validation: ngày 1920-2010, giờ bắt buộc, giới tính bắt buộc
- Lá số = 12 cung × list of sao (chính tinh + phụ tinh) per cung
- Cùng birth data (ngày + giờ + giới tính) → LUÔN cho cùng lá số → cache

### 3.2 Scoring Engine

- 7 dimensions: sự nghiệp, tiền bạc, hôn nhân, sức khỏe, đất đai, học tập, con cái
- 3 score types per data point: Dương (positive), Âm (negative), TB (neutral)
- Time horizons:
  - Cả đời: mốc 10 năm (e.g., 10-20, 20-30, ..., 70-80)
  - 10 năm: mốc từng năm (e.g., 2023, 2024, ..., 2032)
  - 12 tháng: mốc từng tháng (current year)
- Alert system:
  - 🔺 = Positive (opportunity): score vượt threshold + sao tốt alignment
  - 🔻 = Negative (risk): score dưới threshold + sao xấu alignment
  - Mỗi alert có tag text mô tả (e.g., "có bước thăng tiến", "cẩn thận kiện cáo")
- Scoring lookup table: `laso_points` (export từ Google Sheet)

### 3.3 AI Luận Giải

- **Pre-generate tất cả** khi user submit: 1 overview + 7 dimensions = 8 AI calls
- **Per-dimension call structure:**
  - Input: system prompt + KB (dimension) + user data + scores + alerts
  - Output: structured Vietnamese text (~500-1000 words per dimension)
- **Overview call:** Summarize across all 7 dimensions (3-5 câu)
- **Tone rules (non-negotiable):**
  - Empowering, không gieo sợ hãi
  - Mỗi 🔻 PHẢI kèm advice
  - "Cần thận trọng" NOT "sẽ gặp họa"
  - Chỉ nói về data được cung cấp, không bịa
  - Luôn kết thúc bằng disclaimer
- **Quality baseline:** Expert review 10 outputs, phải đạt ≥ 7/10

### 3.4 Charts

- 2 charts per dimension: Lifetime (cả đời) + Decade (10 năm)
- Each chart: 3 lines (Dương, Âm, TB) trên cùng axes
- Alert markers: 🔺🔻 hiển thị tại time points tương ứng
- Overview chart trên result page: tổng hợp (có thể là radar chart hoặc bar chart cho 7 dimensions)
- Mobile-responsive: charts phải readable trên màn hình 375px width

### 3.5 Caching Strategy

- **Cache key:** hash(ngày_sinh + giờ_sinh + giới_tính)
- **Cache layers:**
  - Lá số raw data: cache vĩnh viễn (same input = same output)
  - Scores: cache vĩnh viễn (derived from lá số, deterministic)
  - AI luận giải: cache vĩnh viễn per profile (same data = same interpretation)
- **Cache storage:** SQLite table
- **Cache hit:** skip scraper + scoring + AI → return cached result immediately

---

## 4. FEATURES — IN SCOPE (MVP)

| # | Feature | Priority | Notes |
|---|---------|----------|-------|
| F1 | Landing page (full marketing) | Must | Bán concept, build trust, CTA |
| F2 | Input form (birth data) | Must | Validation, giờ sinh bắt buộc |
| F3 | Scraper pipeline (cohoc.net → lá số) | Must | Playwright, async |
| F4 | Scoring engine (lá số → scores + alerts) | Must | Port from Google Sheet |
| F5 | AI luận giải (pre-generate 7 dims + overview) | Must | Claude Sonnet, structured prompt |
| F6 | Result page (overview + dimension cards) | Must | Charts + AI text |
| F7 | Dimension detail page | Must | 2 charts + full luận giải |
| F8 | Processing screen | Must | Progress steps, polling |
| F9 | Shareable link | Must | Public URL, no login |
| F10 | Mobile responsive | Must | Mobile-first design |
| F11 | Caching (birth data → result) | Should | SQLite, avoid re-scrape |
| F12 | Error handling (scraper fail, AI fail) | Should | Retry + graceful degradation |
| F13 | Simple feedback widget | Nice | "Có ích không?" Yes/No + optional text |

---

## 5. FEATURES — OUT OF SCOPE (Phase 2+)

- Chatbot / hỏi đáp follow-up
- Kinh Dịch gieo quẻ
- User accounts / login / saved profiles
- Payment / premium tier
- Push notifications
- PDF/PPTX export
- Multi-dimension comparison charts
- Family profiles / compatibility
- Bilingual (English)
- Admin dashboard
- Analytics beyond basic feedback

---

## 6. SUCCESS METRICS

| Metric | How to measure | Target |
|--------|---------------|--------|
| Completion rate | % users submit form → see result | > 80% |
| Dimension engagement | % users click ≥ 1 dimension detail | > 60% |
| Deep engagement | % users click ≥ 3 dimensions | > 30% |
| Time on dimension page | Avg time on detail page | > 2 min |
| Expert accuracy | Expert rates 10 AI outputs (1-10) | ≥ 7/10 |
| User satisfaction | "Có ích không?" survey | > 50% positive |
| Share rate | % users click share | > 10% |
| Landing page conversion | % visitors → submit form | > 15% |

---

## 7. CONSTRAINTS

- **Timeline:** 2-4 weeks
- **Team:** 1 developer (Claude Code), 1 domain expert (~5h total)
- **Budget:** Minimal — free/cheap infra, Claude API cost only significant expense
- **Language:** Vietnamese only
- **No login:** All results publicly accessible via URL
- **Giờ sinh bắt buộc:** No "unknown time" option