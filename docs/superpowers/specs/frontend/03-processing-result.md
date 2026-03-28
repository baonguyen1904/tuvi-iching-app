# Frontend Spec — Part 3: Processing Screen + Result Overview

> Part of the frontend design spec. Index: ../2026-03-27-frontend-design-spec.md

---

## PART 5: PAGE 3 — PROCESSING SCREEN (`/processing/[id]`)

### 5.1 Component Tree

```
app/processing/[id]/page.tsx (Server Component — renders ProcessingScreen)
└── ProcessingScreen (Client Component — polls API)
    ├── ProcessingAnimation
    ├── StepIndicator
    ├── ProgressText
    └── FunFactRotator
```

### 5.2 Page Layout

```
Background: bg-bg-primary, min-h-screen
Layout: flex flex-col items-center justify-center px-4 py-16

Content card: max-w-[400px] w-full text-center
  No card border/bg — just centered content, no card chrome
```

### 5.3 ProcessingAnimation

```
Pulsing dot animation:
  3 dots, each 10px × 10px, bg-accent, rounded-full
  Animated with CSS keyframes: scale 0.8→1.2→0.8, opacity 0.4→1→0.4
  Each dot delayed: 0ms, 160ms, 320ms
  Gap: 8px between dots
  Container: flex gap-2 justify-center mb-10

CSS keyframes (in globals.css or Tailwind plugin):
  @keyframes pulse-dot {
    0%, 100% { transform: scale(0.8); opacity: 0.4; }
    50% { transform: scale(1.2); opacity: 1; }
  }
  animation: pulse-dot 1.2s ease-in-out infinite;
```

### 5.4 StepIndicator

```
4 steps, vertical stack, gap-3, max-width 280px, mx-auto

Each step:
  Layout: flex items-center gap-3

  [Icon/status]
    Size: 24px × 24px, flex-shrink-0
    Completed: CheckCircle2 (Lucide, 20px, color alert-positive) — no circle bg
    In-progress: Loader2 (Lucide, 18px, color accent, animate-spin) inside 24px div
    Pending: circle outline, 16px, border-2 border-border, rounded-full, mx-auto (4px margin within 24px)

  [Step text]
    text-body font-medium text-text-primary (completed + in-progress)
    text-body text-text-tertiary (pending)

Steps:
  1: "Đang lấy lá số..."           → maps to steps: scraping_cohoc, scraping_tuvivn
  2: "Đang tính toán điểm số..."   → maps to step: scoring
  3: "Đang phân tích vận mệnh..."  → maps to step: ai_generating
  4: "Hoàn tất!"                   → maps to step: completed

Step mapping:
  scraping_cohoc  → step 1 = in-progress
  scraping_tuvivn → step 1 = in-progress (still scraping)
  scoring         → step 1 = completed, step 2 = in-progress
  ai_generating   → step 1 = completed, step 2 = completed, step 3 = in-progress
  completed       → all completed

<!-- I12: TWO SCRAPERS, ONE UI STEP — Design decision documented:
  The backend runs 2 scrapers (cohoc.net + tuvi.vn) as required by CLAUDE.md Rule 5.
  The UI collapses both into a single Step 1 "Đang lấy lá số..." for simplicity.
  This is NOT a violation of the rule — CLAUDE.md Rule 5 governs backend implementation,
  not UI presentation. Showing 2 separate scraper steps would confuse users with technical
  internals they don't need to understand. Both API steps (scraping_cohoc, scraping_tuvivn)
  map to the same UI step 1. This is intentional.
-->
```

### 5.5 ProgressText

```
Placement: mt-6 text-center

When ai_generating:
  "{aiProgress}/8 lĩnh vực đã được phân tích"
  text-body-sm text-text-secondary

  Progress bar below:
    Width: 200px, height 4px, bg-bg-subtle, rounded-full
    Inner: width={(aiProgress/8)*100}%, bg-accent, rounded-full
    Transition: width 0.3s ease-in-out

When other steps:
  Show the step message from API: "{status.message}"
  text-body-sm text-text-secondary

Error state:
  Icon: AlertTriangle (Lucide, 24px, color amber-500) mb-3
  Text: "Có lỗi xảy ra trong quá trình xử lý."
        text-body text-text-primary font-medium
  Sub-text: "{error.message}" text-body-sm text-text-secondary mt-1
  Retry button: "Thử lại" — primary button, mt-4, w-auto, px-6

  M4 — Retry re-POSTs same data (stored in sessionStorage):
  When BirthInputForm submits successfully and navigates to /processing/[id], store the original
  form data in sessionStorage:
    sessionStorage.setItem('tuvi_last_input', JSON.stringify(birthInputData))

  On the processing error "Thử lại" button click:
    const lastInput = sessionStorage.getItem('tuvi_last_input');
    if (lastInput) {
      // Re-POST with same data, get new profileId, navigate to new processing page
      const result = await generateProfile(JSON.parse(lastInput));
      router.push(`/processing/${result.profileId}`);
    } else {
      router.push('/form');  // fallback: go to form if no stored data
    }

  If no sessionStorage data: navigate to /form (standard fallback).
```

### 5.6 FunFactRotator

```
Placement: mt-12 max-w-[320px] mx-auto text-center

Container: bg-bg-subtle rounded-[12px] px-5 py-4

Prefix: "Bạn có biết?" — text-caption text-text-tertiary font-medium mb-1

Fact text: text-body-sm text-text-secondary

Rotate every 5000ms — fade out (opacity 0, 300ms) → change text → fade in (opacity 1, 300ms)

Facts array (define in constants):
  "Hệ thống Tử Vi Đẩu Số có 14 chính tinh và hơn 100 phụ tinh, tạo ra vô số tổ hợp độc đáo."
  "Lá số của bạn là duy nhất — chỉ ai sinh cùng ngày, giờ và giới tính mới có lá số giống hệt."
  "Tử Vi Đẩu Số có nguồn gốc hơn 1000 năm, được hoàn thiện trong triều đại Tống ở Trung Hoa."
  "Hệ thống chia cuộc đời thành các chu kỳ 10 năm (Đại Vận) — mỗi chu kỳ có năng lượng riêng."
  "AI đang phân tích hàng trăm điểm dữ liệu từ lá số của bạn để tạo luận giải cá nhân hóa."
```

### 5.7 Polling Logic

```typescript
// ProcessingScreen.tsx (Client Component)
'use client';

const POLL_INTERVAL = 2000;  // 2 seconds
const TIMEOUT_MS = 120000;   // 120 seconds

useEffect(() => {
  const startTime = Date.now();

  const poll = async () => {
    if (Date.now() - startTime > TIMEOUT_MS) {
      setError('Quá thời gian chờ. Vui lòng thử lại.');
      return;
    }

    try {
      const status = await getProfileStatus(profileId);
      setCurrentStatus(status);

      if (status.status === 'completed') {
        router.push(`/result/${profileId}`);
        return;
      }

      if (status.status === 'failed') {
        setError(status.message || 'Có lỗi xảy ra.');
        return;
      }

      // Continue polling
      timeoutRef.current = setTimeout(poll, POLL_INTERVAL);
    } catch (err) {
      // Network error — retry up to 3 times
      retryCount.current++;
      if (retryCount.current >= 3) {
        setError('Mất kết nối. Vui lòng thử lại.');
      } else {
        timeoutRef.current = setTimeout(poll, POLL_INTERVAL);
      }
    }
  };

  poll();

  return () => {
    if (timeoutRef.current) clearTimeout(timeoutRef.current);
  };
}, [profileId]);
```

---

## PART 6: PAGE 4 — RESULT OVERVIEW (`/result/[id]`)

### 6.1 Component Tree

```
app/result/[id]/page.tsx (Server Component — fetches profile data)
└── ResultLayout
    ├── ResultHeader (logo + share button)
    ├── ProfileHeaderCard (name, birth info, menh/nguhanh)
    ├── OverviewChartCard
    │   └── OverviewChart (Client — Recharts)
    ├── AIOverviewCard
    ├── DimensionCardsGrid
    │   └── DimensionCard × 8 (includes van_menh)
    ├── FeedbackWidget (Client Component)
    └── ResultFooter
```

### 6.2 Data Fetching

```typescript
// app/result/[id]/page.tsx
import { getProfile } from '@/lib/api';
import { notFound } from 'next/navigation';

export default async function ResultPage({ params }: { params: { id: string } }) {
  let profile: ProfileData;

  try {
    profile = await getProfile(params.id);
  } catch {
    notFound();
  }

  if (!profile) notFound();

  return <ResultLayout profile={profile} />;
}
```

**Caching:** `fetch` with `cache: 'force-cache'` — result pages are immutable once generated. No revalidation needed for MVP.

### 6.3 ResultHeader

```
Position: sticky top-0, z-40
Height: 56px, bg-bg-surface border-b border-border
Layout: max-w-3xl mx-auto px-4 flex items-center justify-between

Left: "TuVi AI" logo, text-sm font-semibold text-text-primary, href="/"
Right: ShareButton component

ShareButton (Client Component):
  Button: ghost style, flex items-center gap-2
  Icon: Share2 (Lucide, 16px) + text "Chia sẻ"
  onClick: copy current URL to clipboard with fallback (I1):
    ```typescript
    async function handleShare() {
      const url = window.location.href;
      try {
        await navigator.clipboard.writeText(url);
        toast.success('Đã copy link!', { duration: 3000 });
      } catch {
        // I1: Fallback for browsers without Clipboard API (e.g. HTTP context, older Safari)
        try {
          const textarea = document.createElement('textarea');
          textarea.value = url;
          textarea.style.position = 'fixed';
          textarea.style.opacity = '0';
          document.body.appendChild(textarea);
          textarea.select();
          document.execCommand('copy');
          document.body.removeChild(textarea);
          toast.success('Đã copy link!', { duration: 3000 });
        } catch {
          toast.error('Không thể copy. Hãy copy link thủ công.', { duration: 5000 });
        }
      }
    }
    ```
  Uses Sonner toast (import { toast } from 'sonner')
```

### 6.4 ProfileHeaderCard

```
Placement: mt-[56px] (accounts for sticky header), mx-4 (or part of max-w-3xl container)

Card: bg-bg-surface border border-border rounded-[12px] p-6 / p-4 mobile
      flex flex-col gap-1

Title: "Chánh Ngã Đồ"
  text-caption font-medium text-text-tertiary uppercase tracking-wide mb-1

Name line: profile.name ? profile.name : "Kết quả luận giải của bạn"
  text-heading-md font-bold text-text-primary

Birth info line:
  "Sinh {birthDate} ({profile.metadata.nam}), {profile.birthHour}, {profile.gender}"
  text-body text-text-secondary mt-1

Menh line:
  "Cung Mệnh: {profile.metadata.cungMenh} — Mệnh {profile.metadata.menh}"
  text-body text-text-secondary

Ngu hanh tags (flex wrap gap-2 mt-3):
  3 pill badges: nam, cuc, amDuong
  Style: text-caption bg-bg-subtle border border-border text-text-secondary px-2 py-1 rounded-full
```

### 6.5 OverviewChartCard

```
Card: standard card style, mt-4

Header: "Tổng quan 8 lĩnh vực"
  text-heading-sm font-semibold text-text-primary mb-4

Chart container:
  Desktop (≥640px): RadarOverviewChart
  Mobile (<640px): BarOverviewChart (horizontal bar, more readable on narrow screens)

  Use CSS show/hide — both components are rendered in the DOM:
  <div class="hidden sm:block"><RadarChart /></div>
  <div class="block sm:hidden"><BarChart /></div>

  <!-- I2: INTENTIONAL DUAL RENDER — Tradeoff documented:
    REASON: Using window.innerWidth or a media query hook in a Client Component would cause
    a hydration mismatch (server renders one, client renders other). CSS show/hide avoids this.
    COST: Both RadarChart and BarChart Recharts bundles are loaded for ALL users (~100KB each gzipped).
    ACCEPTABLE FOR MVP: Result pages are visited after the heavy JS is already cached from the
    detail page. If bundle size becomes a concern post-MVP, switch to a useMediaQuery hook with
    a stable SSR fallback (e.g. always render Radar server-side, swap client-side after hydration).
  -->

Chart height:
  Radar: 300px container
  Bar: auto (8 bars × ~36px + padding = ~340px)

Legend (below chart):
  Flex row, gap-4, justify-center, mt-2
  Each: flex items-center gap-1.5, text-body-sm text-text-secondary
  3 legend items with colored 12px × 3px line indicators (NOT circles):
    Dương: bg-chart-duong
    Âm: bg-chart-am
    TB (Tổng): bg-chart-tb
```

### 6.6 AIOverviewCard

```
Card: standard card style, mt-4

Header row: flex items-center gap-2
  Sparkles icon (Lucide, 18px, color accent)
  Text: "Tổng quan vận mệnh"  text-heading-sm font-semibold text-text-primary

Content:
  mt-3, text-body text-text-secondary leading-relaxed
  Render: {profile.overview.summary} as plain text (no markdown here — it's 3-5 sentences)

Loading skeleton (if summary is null/empty):
  3 skeleton lines: bg-bg-subtle rounded animate-pulse
  Heights: 16px, 16px, 10px (last one shorter)
  Gap: 8px
```

### 6.7 DimensionCardsGrid

```
Section header: "Xem chi tiết từng lĩnh vực"
  text-heading-sm font-semibold text-text-primary mt-8 mb-4

Grid:
  Desktop (≥640px): grid grid-cols-2 gap-4
  Mobile (<640px): grid grid-cols-1 gap-3

Order: su_nghiep, tien_bac, hon_nhan, suc_khoe, dat_dai, hoc_tap, con_cai, van_menh
van_menh is last card.

B9 — Defensive guard when mapping dimension cards:
```typescript
{DIMENSION_ORDER.map((key) => {
  const data = profile.dimensions[key];
  // Guard: skip if dimension data is missing (should not happen, but protects against partial API response)
  if (!data) return null;
  return <DimensionCard key={key} dimensionKey={key} data={data} profileId={profile.profileId} />;
})}
```
```

### 6.8 DimensionCard Component

**File:** `frontend/components/result/DimensionCard.tsx`

```typescript
interface DimensionCardProps {
  dimensionKey: DimensionKey;
  data: DimensionData;
  profileId: string;
}
```

**Visual spec:**

```
Card: bg-bg-surface border border-border rounded-[12px] p-4
      hover:border-accent-border hover:shadow-lg transition-all duration-150 cursor-pointer
      Link wraps entire card → href={`/result/${profileId}/${dimensionKey}`}

Layout: flex flex-col gap-3

[Top row: icon + name + arrow]
  flex items-center justify-between

  Left: flex items-center gap-3
    Icon container: w-9 h-9 rounded-[8px] bg-accent-light flex items-center justify-center
                    Icon: 18px Lucide, color accent
    Name: text-label font-semibold text-text-primary

  Right: ChevronRight (Lucide, 16px, text-text-tertiary)

[Score bar]
  Layout: flex items-center gap-2 mt-1

  Score label: text-mono text-body-sm text-text-tertiary "TB:"
  Score value: text-mono font-medium text-text-primary "{summaryScore.toFixed(1)}"

  Bar track: flex-1 h-1.5 bg-bg-subtle rounded-full overflow-hidden
  Bar fill: width calculated, bg-accent rounded-full

  Score normalization: summaryScore ranges ~-20 to +20. Map to 0-100% for display:
    barWidth = Math.max(0, Math.min(100, ((summaryScore + 20) / 40) * 100))

[Alert badges row] (hidden for van_menh)
  flex flex-wrap gap-1.5

  Positive alerts:
    AlertBadge type="positive" count={positiveAlertCount}
    Only show if count > 0

  Negative alerts:
    AlertBadge type="negative" count={negativeAlertCount}
    Only show if count > 0

  If no alerts: show nothing (empty space, card is shorter — that's fine)

  For van_menh: render nothing here at all

[Interpretation preview — first 80 chars of AI text] (optional, show if available)
  text-body-sm text-text-tertiary leading-snug
  truncated with ellipsis: line-clamp-2
  Hidden on mobile if card is too tall — remove if needed
```

### 6.9 AlertBadge Component

**File:** `frontend/components/result/AlertBadge.tsx`

```typescript
interface AlertBadgeProps {
  type: 'positive' | 'negative';
  count: number;
  label?: string;   // optional custom label
}
```

```
Positive:
  bg-alert-positive-bg border border-alert-positive-bdr text-emerald-700
  px-2 py-0.5 rounded-full text-caption font-medium
  "▲ {count} cơ hội"  (if count > 1) or "▲ Cơ hội" (if count = 1)
  — text-emerald-700 = #047857 gives 4.5:1 contrast on emerald-50 bg ✓

Negative:
  bg-alert-negative-bg border border-alert-negative-bdr text-amber-700
  px-2 py-0.5 rounded-full text-caption font-medium
  "▼ {count} cần chú ý"
  — text-amber-700 = #B45309 gives 4.5:1 contrast on amber-50 bg ✓
  — Do NOT use text-alert-negative (amber-500, only 2.3:1 contrast — fails WCAG AA)
```

### 6.10 FeedbackWidget

**File:** `frontend/components/result/FeedbackWidget.tsx`
Client Component.

```typescript
// B10: FeedbackWidget receives profileId as prop — do NOT read from URL params here
interface FeedbackWidgetProps {
  profileId: string;  // passed from parent ResultLayout/ResultPage
}

type FeedbackState = 'idle' | 'positive' | 'negative' | 'expanded' | 'submitted' | 'error'; // I6: 'error' added
const [state, setState] = useState<FeedbackState>('idle');
const [comment, setComment] = useState('');
```

```
Placement: mt-12 mb-8

Container: text-center

Question: "Luận giải này có ích cho bạn không?"
  text-body text-text-secondary mb-4

Buttons row (idle state): flex justify-center gap-3
  Positive: ThumbsUp icon (16px) + "Có" — secondary button
  Negative: ThumbsDown icon (16px) + "Không" — secondary button

  onClick positive: setState('positive') then setState('expanded')
  onClick negative: setState('negative') then setState('expanded')

Expanded state (comment textarea + submit):
  Question replaced with: "Cảm ơn! Bạn muốn chia sẻ thêm không?" text-body-sm text-text-secondary

  Textarea:
    rows={3}, placeholder="Chia sẻ suy nghĩ (không bắt buộc)..."
    Standard input styling, resize-none

  Submit button: "Gửi phản hồi" — primary, full-width, mt-2
  Skip link: "Bỏ qua" — ghost, text-sm, mt-1 block text-center

  onSubmit:
    // B10: profileId is passed as prop, included in Feedback object
    // I6: Catch API errors and set 'error' state
    try {
      await submitFeedback({ profileId, helpful: state === 'positive', comment })
      setState('submitted')
    } catch {
      setState('error')
    }

Submitted state:
  CheckCircle2 icon (24px, color alert-positive) + "Cảm ơn bạn đã phản hồi!"
  text-body text-text-secondary

Error state (I6):
  AlertTriangle icon (20px, amber-500)
  Text: "Gửi thất bại, vui lòng thử lại."  text-body-sm text-text-secondary
  Retry button: "Thử lại" → secondary button, onClick: setState('expanded')
```

### 6.11 ResultFooter

```
mt-8 pb-8 border-t border-border pt-6

Layout: text-center

Disclaimer:
  text-caption text-text-tertiary max-w-[400px] mx-auto
  "Nội dung luận giải mang tính tham khảo dựa trên hệ thống Tử Vi Đẩu Số.
   Không phải lời khuyên chuyên nghiệp. Mọi quyết định cuối cùng là của bạn."

Below: "© 2026 TuVi AI" text-caption text-text-tertiary mt-2
```

---
