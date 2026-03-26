# Task 04: Frontend — Landing Page + App UI
## Next.js Web Application

**Priority:** Must
**Estimated effort:** 4-5 days
**Dependencies:** Task 01-03 (API endpoints), design direction decided
**Output:** Next.js app in `/frontend`

---

## What to Build

4 main pages + reusable components:
1. Landing page (full marketing)
2. Input form
3. Processing screen
4. Result page (overview + dimension detail)

---

## Design System

### Philosophy
Modern minimalist. Think Notion × Linear × Vercel. Clean, generous whitespace, sharp typography. NO traditional Eastern aesthetic (no dragons, no red/gold, no Chinese calligraphy fonts).

### Typography
- **Headings:** Inter (700, 600 weights) — hoặc system font stack
- **Body:** Inter (400, 500) — clean, readable
- **Vietnamese support:** Inter handles Vietnamese diacritics well
- **Scale:** 14px base, 1.6 line-height for body, 1.2 for headings

### Color Palette

```
--bg-primary:       #FAFAFA    /* Page background */
--bg-surface:       #FFFFFF    /* Cards, panels */
--bg-subtle:        #F3F4F6    /* Hover states, secondary surfaces */

--text-primary:     #111827    /* Headings, important text */
--text-secondary:   #6B7280    /* Body text, descriptions */
--text-tertiary:    #9CA3AF    /* Placeholders, metadata */

--accent:           #2563EB    /* Primary CTA, links */
--accent-hover:     #1D4ED8    /* CTA hover */
--accent-light:     #EFF6FF    /* Accent background */

--alert-positive:   #10B981    /* 🔺 alerts, good scores */
--alert-positive-bg:#ECFDF5
--alert-negative:   #F59E0B    /* 🔻 alerts (amber, NOT red) */
--alert-negative-bg:#FFFBEB

--border:           #E5E7EB
--border-focus:     #2563EB

--chart-duong:      #2563EB    /* Dương line (blue) */
--chart-am:         #F59E0B    /* Âm line (amber) */
--chart-tb:         #9CA3AF    /* TB line (gray) */
```

### Spacing & Layout
- Grid: 8px base unit
- Max content width: 768px (mobile-first, centered)
- Card padding: 24px (desktop), 16px (mobile)
- Section spacing: 64px (desktop), 40px (mobile)
- Border radius: 12px (cards), 8px (buttons), 6px (inputs)
- Shadows: `0 1px 3px rgba(0,0,0,0.08)` (subtle, single level)

### Components Style
- Buttons: Solid fill (primary), outline (secondary), ghost (tertiary)
- Cards: White surface, subtle border, no shadow OR minimal shadow
- Inputs: Border bottom only OR full border, large touch targets (48px height)
- Icons: Lucide icons (consistent, minimal)

---

## Page 1: Landing Page (`/`)

### Sections (top → bottom)

**1. Hero**
```
[Full-width, centered]

Headline (h1):     "Hiểu vận mệnh — Ra quyết định tốt hơn"
                   (or variant — placeholder, will A/B test)

Subheadline (p):   "Luận giải tử vi cá nhân hóa bằng AI, 
                    dựa trên hệ thống Tử Vi Đẩu Số 
                    và kiến thức chuyên gia."

[CTA Button: "Xem luận giải miễn phí →"]

[Subtle mockup/illustration below — abstract, not mê tín]
```

**2. How It Works (3 steps)**
```
[3 cards in a row (desktop) / stack (mobile)]

Step 1: 📝 "Nhập ngày giờ sinh"
        "Chỉ cần ngày sinh dương lịch, giờ sinh và giới tính."

Step 2: 🔍 "AI phân tích lá số"
        "Hệ thống tính toán biểu đồ vận mệnh 
         dựa trên Tử Vi Đẩu Số."

Step 3: 📊 "Nhận luận giải chi tiết"
        "7 lĩnh vực đời sống, mỗi lĩnh vực 
         có biểu đồ + lời khuyên cụ thể."
```

**3. Dimensions Preview**
```
[Grid: 3×2 + 1 (desktop) / 2×3 + 1 (mobile)]

7 cards, mỗi card:
  [Icon]  [Tên dimension]
  [1 dòng mô tả ngắn]

Sự nghiệp — "Xu hướng thăng tiến, thời điểm thuận lợi"
Tiền bạc  — "Biến động tài chính, cơ hội đầu tư"
Hôn nhân  — "Tình duyên, tương thích, thời điểm tốt"
Sức khỏe  — "Giai đoạn cần chú ý, cách phòng tránh"
Đất đai   — "Mua bán bất động sản, thời điểm tốt"
Học tập   — "Phát triển bản thân, học vấn"
Con cái   — "Vận con cái, thời điểm sinh con"
```

**4. Trust Building**
```
[Clean section, subtle bg]

"Tại sao khác biệt?"

• "Dựa trên Tử Vi Đẩu Số — hệ thống có phương pháp, 
   không phải xem bói cảm tính"
• "Knowledge base từ chuyên gia 20+ năm kinh nghiệm"  
• "AI phân tích DỮ LIỆU từ lá số — không bịa đặt"
• "Biểu đồ trực quan, lời khuyên cụ thể"
```

**5. Sample Preview**
```
[Screenshot mockup of result page — blurred or sample data]
"Đây là những gì bạn sẽ nhận được"
```

**6. FAQ (Accordion)**
```
Q: "Khác gì xem bói online?"
Q: "Có chính xác không?"
Q: "Thông tin của tôi có được bảo mật?"
Q: "Tại sao cần biết giờ sinh?"
Q: "Miễn phí thật không?"
```

**7. Final CTA**
```
"Bắt đầu ngay. Miễn phí. Không cần đăng ký."
[CTA Button: "Xem luận giải →"]
```

**8. Footer**
```
"© 2026 [App Name]"
"Disclaimer: Luận giải mang tính tham khảo..."
```

### Landing Page Behavior
- SSR (server-side rendered) for SEO
- Smooth scroll for CTA → form section (or navigate to /form)
- Mobile-responsive: all sections stack vertically
- No JS-heavy animations — keep it fast

---

## Page 2: Input Form (`/form`)

```
[Card centered on page, max-width 480px]

"Nhập thông tin ngày sinh"

Họ tên (optional)
[Text input — placeholder: "Nguyễn Văn A"]

Ngày sinh *
[Date picker — dương lịch — default empty]

Giờ sinh *
[Dropdown — 12 options]
  Giờ Tý (23:00 - 01:00)
  Giờ Sửu (01:00 - 03:00)
  Giờ Dần (03:00 - 05:00)
  Giờ Mão (05:00 - 07:00)
  Giờ Thìn (07:00 - 09:00)
  Giờ Tỵ (09:00 - 11:00)
  Giờ Ngọ (11:00 - 13:00)
  Giờ Mùi (13:00 - 15:00)
  Giờ Thân (15:00 - 17:00)
  Giờ Dậu (17:00 - 19:00)
  Giờ Tuất (19:00 - 21:00)
  Giờ Hợi (21:00 - 23:00)

[Info icon + tooltip]: 
"Giờ sinh ảnh hưởng đến Cung Mệnh — yếu tố 
 quan trọng nhất trong Tử Vi Đẩu Số. Nếu không 
 biết chính xác, hãy hỏi cha mẹ hoặc xem sổ khai sinh."

Giới tính *
[Radio buttons: ○ Nam  ○ Nữ]

[Submit button: "Xem luận giải →"]
  Loading state: button disabled, spinner, "Đang xử lý..."

[Small text below]: 
"Thông tin của bạn không được lưu trữ cho mục đích nào khác."
```

### Form Validation
- Date: required, range 1920-2010
- Hour: required, must select one
- Gender: required
- Name: optional, max 100 chars
- Show inline errors (red text below field)
- Disable submit until all required fields valid

### On Submit
- POST to `/api/generate`
- On success → navigate to `/processing/[profileId]`
- On error → show error message, keep form filled

---

## Page 3: Processing Screen (`/processing/[id]`)

```
[Full-screen centered, minimal]

[Subtle animation — spinner or pulsing dots]

Step indicator:
  ✅ Đã lấy lá số
  ⏳ Đang tính toán điểm số...
  ○  Đang phân tích vận mệnh
  ○  Hoàn tất

[Progress: 2/8 dimensions analyzed]

[Optional: fun fact about Tử Vi rotating every 5 seconds]
  "Hệ thống Tử Vi Đẩu Số có 14 chính tinh và hơn 100 phụ tinh..."
  "Lá số tử vi của bạn là duy nhất — chỉ ai sinh cùng ngày, 
   giờ và giới tính mới có lá số giống hệt..."
```

### Behavior
- Poll `GET /api/profile/{id}/status` every 2 seconds
- Update step indicator based on `step` + `progress` fields
- When `status === "completed"` → redirect to `/result/[id]`
- When `status === "failed"` → show error + "Thử lại" button
- If user refreshes → resume polling (profileId in URL)
- Timeout: if no completion after 120 seconds → show error

---

## Page 4: Result Page (`/result/[id]`)

### Layout (responsive)

```
[Header bar]
  [App logo/name]                    [Share button 📤]

[Profile header — card]
  Chánh Ngã Đồ — {name or "Bạn"}
  Sinh: {birth_date} ({lunar_info}), Giờ {birth_hour}, {gender}
  Cung Mệnh: {cung_menh} — {ngu_hanh}

[Overview chart — card]
  [Radar chart or bar chart showing 7 dimension scores]

[AI Overview — card]
  "Tổng quan vận mệnh"
  {3-5 sentence AI generated summary}

[Dimension cards grid — 2 columns (desktop), 1 column (mobile)]
  7 cards, each:
    [Icon] {Dimension name}
    [Mini score indicator: bar or number]
    [Alert badges if any: 🔺×2 🔻×1]
    [Click → expand or navigate to detail]

[Footer]
  Disclaimer + "Chia sẻ kết quả" link
```

### Dimension Detail (expand or separate route)

**Option A: Accordion expand** (recommended for mobile UX)
- Click dimension card → expands inline with charts + AI text
- Other cards collapse

**Option B: Separate route** (`/result/[id]/[dimension]`)
- Click → navigate to dedicated page
- Back button → return to overview

**Recommend Option A for MVP** — less navigation, feels more seamless.

### Detail Content (when expanded / on detail page)

```
[Dimension title: "Luận giải Sự Nghiệp"]

[Chart: Cả đời]
  X: age ranges (10-20, 20-30, ...)
  Y: score
  3 lines: Dương (blue), Âm (amber), TB (gray)
  Alert markers: 🔺🔻 at relevant points

[Chart: 10 năm ({decade_range})]
  X: years (2023, 2024, ...)
  Y: score
  3 lines: same
  Alert markers: same

[AI Luận Giải text — rendered markdown]
  ## Tổng quan sự nghiệp
  ...
  ## Giai đoạn hiện tại
  ...
  ## Các mốc cần chú ý
  🔺 2025: ...
  🔻 2027: ...
  ## Lời khuyên
  ...
  ---
  *Disclaimer*

[Navigation: ← Prev dimension | Next dimension →]
```

---

## Charts (Recharts)

### Lifetime Chart Component

```tsx
interface LifetimeChartProps {
  data: Array<{
    period: string;   // "10-20", "20-30", etc.
    duong: number;
    am: number;
    tb: number;
  }>;
  alerts: Array<{
    type: 'positive' | 'negative';
    period: string;   // maps to x-axis
    tag: string;
  }>;
}
```

- Line chart with 3 series
- X-axis: period labels
- Y-axis: score (auto-scale)
- Alert markers: custom dots at alert periods (green ▲ / amber ▼)
- Tooltip: show score values + alert tag on hover
- Responsive: min-height 250px, full-width

### Decade Chart Component
- Same structure, different data granularity (individual years)

### Overview Chart Component
- **Radar chart** (spider chart) with 7 axes = 7 dimensions
- Each axis: summary score for that dimension
- Single fill area showing relative strengths
- Labels: dimension names in Vietnamese

---

## Shared Components

### DimensionCard
```tsx
interface DimensionCardProps {
  dimension: string;        // key
  label: string;           // Vietnamese name
  icon: string;            // Lucide icon name
  summaryScore: number;
  alertCount: { positive: number; negative: number };
  isExpanded: boolean;
  onClick: () => void;
}
```

### AlertBadge
```tsx
// Positive: green bg, ▲ icon
// Negative: amber bg, ▼ icon
```

### ShareButton
```tsx
// Click → copy URL to clipboard
// Show "Đã copy link!" toast for 3 seconds
```

### FeedbackWidget
```tsx
// Bottom of result page
// "Luận giải này có ích cho bạn không?"
// [👍 Có] [👎 Không] + Optional textarea
// Submit → POST /api/feedback
```

---

## API Client (`lib/api.ts`)

```typescript
const API_BASE = process.env.NEXT_PUBLIC_API_URL;

export async function generateProfile(input: BirthInput): Promise<{ profileId: string }> {
  const res = await fetch(`${API_BASE}/api/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(input)
  });
  return res.json();
}

export async function getProfileStatus(id: string): Promise<ProfileStatus> { ... }
export async function getProfile(id: string): Promise<ProfileData> { ... }
export async function submitFeedback(id: string, feedback: Feedback): Promise<void> { ... }
```

---

## Acceptance Criteria

- [ ] Landing page: all 7 sections render, CTA navigates to form
- [ ] Landing page: scores 90+ on Lighthouse (Performance, SEO)
- [ ] Input form: validates all fields, shows inline errors
- [ ] Input form: disables submit during loading
- [ ] Input form: handles API errors gracefully
- [ ] Processing: polls every 2s, updates step indicator
- [ ] Processing: redirects to result on completion
- [ ] Processing: shows error + retry on failure
- [ ] Result: overview chart renders with 7 dimensions
- [ ] Result: AI overview text displays
- [ ] Result: 7 dimension cards with scores + alert badges
- [ ] Result: dimension detail expands with 2 charts + AI text
- [ ] Result: charts render correctly with 3 lines + alert markers
- [ ] Result: share button copies URL to clipboard
- [ ] Result: feedback widget submits
- [ ] Mobile: all pages responsive at 375px width
- [ ] Mobile: touch targets ≥ 44px
- [ ] Mobile: charts readable (not too compressed)
- [ ] No console errors in production build
- [ ] Page load < 3 seconds on 3G connection (landing page)

---

## Implementation Order

1. **Day 1:** Project setup (Next.js + Tailwind + Recharts) + design system tokens
2. **Day 1-2:** Landing page (all sections, responsive)
3. **Day 2-3:** Input form + API client + processing screen
4. **Day 3-4:** Result page (overview + dimension cards + accordion)
5. **Day 4-5:** Charts (Lifetime + Decade + Overview radar) + polish
6. **Day 5:** Feedback widget + share button + mobile testing