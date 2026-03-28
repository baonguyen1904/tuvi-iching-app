# Frontend Spec — Part 5: API, Responsive, Accessibility, Performance, Config

> Part of the frontend design spec. Index: ../2026-03-27-frontend-design-spec.md

---

## PART 9: DATA FLOW & API CLIENT

### 9.1 API Client

**File:** `frontend/lib/api.ts`

```typescript
// M2: Warn loudly if API URL is not configured (prevents silent fallback to localhost in production)
if (!process.env.NEXT_PUBLIC_API_URL) {
  console.warn(
    '[TuViAI] NEXT_PUBLIC_API_URL is not set. Falling back to http://localhost:8000. ' +
    'Set this environment variable in Vercel dashboard for production.'
  );
}
const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

// M8: 30-second AbortController timeout on all API calls
const FETCH_TIMEOUT_MS = 30_000;

async function fetchAPI<T>(path: string, options?: RequestInit): Promise<T> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);

  try {
    const res = await fetch(`${API_BASE}${path}`, {
      ...options,
      signal: controller.signal,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });

    if (!res.ok) {
      const error = await res.json().catch(() => ({}));
      throw new Error(error.detail ?? `HTTP ${res.status}`);
    }

    return res.json();
  } catch (err) {
    if (err instanceof Error && err.name === 'AbortError') {
      throw new Error('Yêu cầu quá thời gian. Vui lòng thử lại.');
    }
    throw err;
  } finally {
    clearTimeout(timeoutId);
  }
}

export const generateProfile = (input: BirthInput) =>
  fetchAPI<{ profileId: string; status: string }>('/api/generate', {
    method: 'POST',
    body: JSON.stringify(input),
  });

export const getProfileStatus = (id: string) =>
  fetchAPI<ProfileStatus>(`/api/profile/${id}/status`);

export const getProfile = (id: string) =>
  fetchAPI<ProfileData>(`/api/profile/${id}`, {
    cache: 'force-cache',   // immutable once generated — server component use
  });

// B10: submitFeedback signature — Feedback type (defined in types.ts) includes profileId.
// POST /api/feedback request body shape:
// {
//   "profileId": "abc123def456",   // required — identifies which profile the feedback is for
//   "helpful": true,               // required — thumbs up/down
//   "comment": "..."               // optional — free text from expanded state
// }
export const submitFeedback = (feedback: Feedback) =>
  fetchAPI<void>('/api/feedback', {
    method: 'POST',
    body: JSON.stringify(feedback),
  });
```

### 9.2 Server vs Client Component Map

| Component | Type | Reason |
|-----------|------|--------|
| `app/page.tsx` (landing) | Server | SSR for SEO |
| `LandingNav` | Client | Scroll event listener |
| `HeroSection` | Server | Static content |
| `HowItWorksSection` | Server | Static content |
| `DimensionsPreviewSection` | Server | Static content |
| `TrustBuildingSection` | Server | Static content |
| `SamplePreviewSection` | Server | Static content |
| `FAQSection` | Client | Accordion interaction |
| `FinalCTASection` | Server | Static content |
| `app/form/page.tsx` | Server | Shell only |
| `BirthInputForm` | Client | Form state, validation, submission |
| `DateField` (Calendar) | Client | Calendar interaction |
| `app/processing/[id]/page.tsx` | Server | Shell only |
| `ProcessingScreen` | Client | Polling, timers, state |
| `app/result/[id]/page.tsx` | Server | Fetches profile data |
| `ResultHeader` | Server | Static (ShareButton is client island) |
| `ShareButton` | Client | Clipboard API |
| `ProfileHeaderCard` | Server | Display only |
| `OverviewRadarChart` | Client | Recharts (needs DOM) |
| `OverviewBarChart` | Client | Recharts |
| `AIOverviewCard` | Server | Display only |
| `DimensionCardsGrid` | Server | Links only |
| `DimensionCard` | Server | Link only (no interaction) |
| `FeedbackWidget` | Client | State machine |
| `app/result/[id]/[dimension]/page.tsx` | Server | Fetches profile data |
| `LifetimeChart` | Client | Recharts |
| `DecadeChart` | Client | Recharts |
| `MonthlyChart` | Client | Recharts |
| `AIInterpretationSection` | Server | react-markdown, static |

---

## PART 10: RESPONSIVE BEHAVIOR

### 10.1 Breakpoints

```
Mobile-first. Single main breakpoint: 640px (Tailwind `sm`).
Content never exceeds 768px (max-w-3xl).

Mobile: 0 – 639px
Desktop: 640px+
```

### 10.2 Per-Component Responsive Rules

| Component | Mobile (< 640px) | Desktop (≥ 640px) |
|-----------|-----------------|-------------------|
| HeroSection | text-[28px] h1, vertical stack | text-[36px] h1 |
| HowItWorksSection | flex-col cards, flex-row layout inside card | grid-cols-3 |
| DimensionsPreviewSection | grid-cols-2 | grid-cols-4 |
| Card padding | p-4 (16px) | p-6 (24px) |
| Section spacing | py-10 (40px) | py-16 (64px) |
| DimensionCardsGrid | grid-cols-1 | grid-cols-2 |
| OverviewChart | BarChart (horizontal) | RadarChart |
| Chart height | 200px | 240-280px |
| Chart X-axis | every other label | every label |
| DimensionNavigation | stacked if needed | single row |
| ProfileHeaderCard | compact, smaller text | full |

### 10.3 Touch Targets

All interactive elements must have minimum 44px × 44px touch target:
- Buttons: `min-h-[44px]` or explicitly `h-[48px]`
- Radio buttons: label must be tappable, not just the circle
- Accordion trigger: `py-4` gives 48px+ effective height
- Dimension cards: no min-height constraint — full card is tappable
- DimensionNavigation links: `py-4` padding

### 10.4 Charts on Mobile

- Minimum chart height: 200px (never less — lines become unreadable)
- On 375px width, 12-point X-axis (LifetimeChart): use `interval={isMobile ? 1 : 0}` — shows every
  other label on mobile, all labels on desktop. This is the single consistent approach across all
  charts (§8.2 LifetimeChart, §8.3 DecadeChart). Do NOT use `interval="preserveStartEnd"` or
  custom interval functions — they produce inconsistent results across chart types.
- Radar chart: hidden below 640px, replaced by BarChart (CSS `hidden sm:block`)
- All charts: `ResponsiveContainer width="100%"` — fills card width

---

## PART 11: INTERACTION PATTERNS

### 11.1 Hover States

```
Cards (clickable):
  Default: border-border shadow-md
  Hover: border-accent-border shadow-lg scale(1.005) — subtle lift
  Transition: all 150ms ease

Buttons:
  Primary: bg-accent → bg-accent-hover (150ms)
  Ghost/Link: text-text-secondary → text-text-primary (100ms)
  All: no scale on buttons (only on cards)

Links:
  text-accent, no underline by default
  hover: underline
```

### 11.2 Focus States

All interactive elements:
```css
focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-offset-2
```

- Never remove focus ring without replacement
- Tab order: logical DOM order (no tabindex manipulation)
- Skip link: first focusable element on each page → "Bỏ qua điều hướng" → jumps to `#main-content`

### 11.3 Loading States

**Charts loading skeleton:**
```
While chart data loads:
  Skeleton rect: full width, height=240px, bg-bg-subtle rounded-[12px] animate-pulse
```

**AI text loading skeleton:**
```
4 skeleton lines: h-4 bg-bg-subtle rounded animate-pulse
Widths: 100%, 90%, 100%, 60%
Gap: 8px
```

**Page transitions:**
- Next.js App Router handles route transitions
- No custom page transition animation (keep it simple/fast)
- Loading.tsx files for Suspense boundaries:
  - `app/result/[id]/loading.tsx`: skeleton matching result page layout
  - `app/result/[id]/[dimension]/loading.tsx`: skeleton matching detail layout
  - `app/processing/[id]/loading.tsx`: pulsing dots skeleton (I8) — see spec below

**I8 — `app/processing/[id]/loading.tsx` spec:**
```typescript
// Shown by Next.js during navigation to /processing/[id] (before ProcessingScreen mounts)
// Use the same pulsing dot animation as ProcessingAnimation (§5.3)
export default function ProcessingLoading() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4">
      <div className="flex gap-2 justify-center mb-6">
        {/* 3 pulsing dots matching §5.3 ProcessingAnimation spec */}
        <div className="w-2.5 h-2.5 rounded-full bg-accent animate-[pulse-dot_1.2s_ease-in-out_infinite]" />
        <div className="w-2.5 h-2.5 rounded-full bg-accent animate-[pulse-dot_1.2s_ease-in-out_160ms_infinite]" />
        <div className="w-2.5 h-2.5 rounded-full bg-accent animate-[pulse-dot_1.2s_ease-in-out_320ms_infinite]" />
      </div>
      <p className="text-body-sm text-text-tertiary">Đang chuẩn bị...</p>
    </div>
  );
}
// Note: pulse-dot keyframe is defined in globals.css (see §5.3)
```

### 11.4 Error States

**Form field error:**
```
Field border: border-red-400
Error message: text-red-500 text-body-sm mt-1.5
               AlertCircle icon 14px inline before text
Trigger: onBlur validation + on failed submit
```

**API error (form submit):**
```
Alert banner inside card, below submit button:
  bg-red-50 border border-red-200 rounded-[8px] px-4 py-3 mt-4
  AlertTriangle icon (16px, text-red-500) + text-body-sm text-red-700
  "Có lỗi xảy ra. Vui lòng thử lại."
```

**Processing error:**
```
Replace animation area:
  AlertTriangle icon (32px, amber-500)
  Error title: text-heading-sm
  Error detail: text-body-sm text-text-secondary
  Retry button: primary → /form
```

**Result not found (notFound()):**
- Next.js routes `notFound()` calls to the nearest `not-found.tsx` in the tree; use the global
  `app/not-found.tsx` (M3) — do NOT create a separate `app/result/not-found.tsx`.
- The global not-found page already handles all `notFound()` calls from any route.

**Global not-found.tsx (M3):**

```typescript
// app/not-found.tsx — Global 404 page (also used by notFound() calls)
// Server Component (no 'use client' needed)
import Link from 'next/link';

export default function NotFound() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4 text-center gap-4">
      <h1 className="text-heading-md font-bold text-text-primary">404</h1>
      <p className="text-body text-text-secondary max-w-[360px]">
        Trang này không tồn tại hoặc đã bị xóa.
      </p>
      <Link href="/" className="primary-button mt-2">
        Về trang chủ
      </Link>
    </div>
  );
}
```

**error.tsx boundaries (B6):**

Next.js requires `error.tsx` files to be Client Components. Define the following four error boundaries:

```typescript
// app/error.tsx — Global fallback
'use client';
export default function GlobalError({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4 text-center gap-4">
      <h1 className="text-heading-sm font-semibold text-text-primary">Đã xảy ra lỗi</h1>
      <p className="text-body text-text-secondary max-w-[360px]">
        Có lỗi không mong đợi. Vui lòng thử lại hoặc quay về trang chủ.
      </p>
      <div className="flex gap-3">
        <button onClick={reset} className="primary-button">Thử lại</button>
        <a href="/" className="secondary-button">Về trang chủ</a>
      </div>
    </div>
  );
}

// app/result/[id]/error.tsx — Result page error
'use client';
export default function ResultError({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4 text-center gap-4">
      <h1 className="text-heading-sm font-semibold text-text-primary">Không thể tải kết quả</h1>
      <p className="text-body text-text-secondary max-w-[360px]">
        Có lỗi khi tải trang kết quả. Vui lòng thử lại.
      </p>
      <div className="flex gap-3">
        <button onClick={reset} className="primary-button">Thử lại</button>
        <a href="/" className="secondary-button">Về trang chủ</a>
      </div>
    </div>
  );
}

// app/result/[id]/[dimension]/error.tsx — Dimension detail error
'use client';
export default function DimensionError({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4 text-center gap-4">
      <h1 className="text-heading-sm font-semibold text-text-primary">Không thể tải lĩnh vực này</h1>
      <p className="text-body text-text-secondary max-w-[360px]">
        Có lỗi khi tải trang chi tiết. Vui lòng thử lại hoặc quay về tổng quan.
      </p>
      <div className="flex gap-3">
        <button onClick={reset} className="primary-button">Thử lại</button>
        <a href=".." className="secondary-button">Về tổng quan</a>
      </div>
    </div>
  );
}

// app/processing/[id]/error.tsx — Processing page error
'use client';
export default function ProcessingError({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4 text-center gap-4">
      <h1 className="text-heading-sm font-semibold text-text-primary">Lỗi trong quá trình xử lý</h1>
      <p className="text-body text-text-secondary max-w-[360px]">
        Có lỗi khi xử lý dữ liệu. Vui lòng thử lại từ đầu.
      </p>
      <div className="flex gap-3">
        <button onClick={reset} className="primary-button">Thử lại</button>
        <a href="/form" className="secondary-button">Nhập lại thông tin</a>
      </div>
    </div>
  );
}
```

---

## PART 12: ACCESSIBILITY

### 12.1 Semantic HTML

```
- Page landmark: <main id="main-content"> wraps content, <nav> for navigation
- Headings: strict hierarchy (h1 → h2 → h3). One h1 per page.
- Lists: <ul>/<ol> for FAQ, step lists, dimension lists
- Charts: wrapped in <figure> with <figcaption> describing what the chart shows
- Form: <form> with <fieldset>/<legend> for radio groups
- Buttons vs links: <button> for actions, <a> for navigation
```

### 12.2 ARIA Labels

```typescript
// Chart ARIA
<figure aria-label={`Biểu đồ ${chartTitle}`} role="figure">
  <figcaption className="sr-only">
    {`Biểu đồ đường thể hiện điểm Dương, Âm và TB của ${dimensionLabel} theo ${period}`}
  </figcaption>
  <ResponsiveContainer>...</ResponsiveContainer>
</figure>

// Alert badges
<span aria-label={`${count} cơ hội tích cực được phát hiện`}>▲ {count}</span>

// Share button
<button aria-label="Sao chép link kết quả vào clipboard">
  <Share2 aria-hidden="true" />
  Chia sẻ
</button>

// Loading state
<div role="status" aria-live="polite" aria-label="Đang tải...">
  [spinner]
</div>

// Processing step indicator
<ol role="list" aria-label="Các bước xử lý">
  <li aria-current={isActive ? 'step' : undefined}>...</li>
</ol>

// Dimension nav
<nav aria-label="Điều hướng giữa các lĩnh vực">
  <a aria-label={`Lĩnh vực trước: ${prevLabel}`}>...</a>
  <a aria-label={`Lĩnh vực tiếp theo: ${nextLabel}`}>...</a>
</nav>
```

### 12.3 Keyboard Navigation

```
Tab order on landing: Nav CTA → Hero CTA → (visible sections) → FAQ items → Footer CTA
Tab order on form: Name → Date trigger → Hour select → Gender Nam → Gender Nữ → Submit
Tab order on result: Share → Profile → (non-interactive overview) → Dimension cards → Feedback → Footer
Tab order on detail: Back → Share → (charts — non-focusable) → AI text → Prev nav → Next nav

FAQ Accordion:
  Each AccordionTrigger is focusable
  Enter/Space: toggle open
  shadcn handles this natively

Charts: not keyboard-navigable (visual only). Screen reader gets figcaption instead.

Escape: closes any open Popover (Calendar) or Tooltip — shadcn handles this.
```

### 12.4 Color Contrast

Verify minimum 4.5:1 for normal text, 3:1 for large text:
- `#111827` on `#FFFFFF`: 16.1:1 ✓
- `#6B7280` on `#FFFFFF`: 5.9:1 ✓
- `#9CA3AF` on `#FFFFFF`: 3.8:1 — borderline. Use only for non-essential text.
- `#FFFFFF` on `#2563EB`: 4.7:1 ✓
- `#10B981` on `#ECFDF5`: 3.1:1 — large text/icons only (not body text)
- `#F59E0B` on `#FFFBEB`: 2.3:1 — NOT sufficient for text. AlertBadge uses `text-amber-700` (#B45309) and `text-emerald-700` (#047857) instead — see §6.9.

### 12.5 Motion/Animation

```css
/* Respect prefers-reduced-motion */
@media (prefers-reduced-motion: reduce) {
  .animate-pulse { animation: none; }
  .animate-spin { animation: none; }
  * { transition-duration: 0.01ms !important; }
}
```

---

## PART 13: PERFORMANCE STRATEGY

### 13.1 Code Splitting

- All Client Components automatically code-split by Next.js
- Chart components (`LifetimeChart`, `DecadeChart`, etc.) are Client Components — they only ship to the browser when the detail page is visited
- Heavy components wrapped with `dynamic()` if needed:

```typescript
// If Recharts bundle size is a concern (unlikely but possible):
import dynamic from 'next/dynamic';
const LifetimeChart = dynamic(() => import('@/components/charts/LifetimeChart'), {
  ssr: false,
  loading: () => <ChartSkeleton height={240} />,
});
```

### 13.2 Image Optimization

```typescript
// Use Next.js Image component everywhere
import Image from 'next/image';

// Hero SVG: inline SVG (no Image component needed — no network request)

// Sample preview screenshot:
<Image
  src="/images/sample-result-preview.png"
  alt="Ví dụ kết quả luận giải tử vi"
  width={600}
  height={375}
  loading="lazy"
  quality={80}
  className="w-full h-auto"
/>
```

No external image domains needed for MVP — all assets are local.

### 13.3 Font Loading

```typescript
// Use next/font — zero layout shift, no external request at runtime
import { Inter } from 'next/font/google';
const inter = Inter({
  subsets: ['latin', 'vietnamese'],  // Vietnamese subset critical
  display: 'swap',
  preload: true,
  variable: '--font-inter',
  weight: ['400', '500', '600', '700'],  // Only what's used
});
```

### 13.4 Bundle Size Targets

| Bundle | Target |
|--------|--------|
| Landing page JS | < 80KB gzipped |
| Form page JS | < 50KB gzipped |
| Result page JS (no charts) | < 60KB gzipped |
| Recharts (charts) | ~100KB gzipped (acceptable — lazy loaded) |
| Total first load | < 200KB gzipped |

**Lucide imports:** Always import individually, never `import * from 'lucide-react'`.

### 13.5 Fetch Strategy

<!-- I3: RESOLVED — One approach only. Do NOT mix Suspense wrapper pattern with direct async fetch.
  CHOSEN: Direct async fetch in server component (simpler, fewer files, adequate for MVP).
  The Suspense wrapper + ResultContent pattern adds complexity without benefit at this scale.
  Next.js loading.tsx already handles the loading skeleton during navigation (see §11.3).
-->

**Pattern for result pages:**
```typescript
// app/result/[id]/page.tsx — Direct async fetch (NO Suspense wrapper)
export default async function ResultPage({ params }) {
  const profile = await getProfile(params.id);  // throws → caught by error.tsx
  if (!profile) notFound();
  return <ResultLayout profile={profile} />;
}

// app/result/[id]/loading.tsx — Handles navigation skeleton (Next.js built-in)
export default function ResultLoading() {
  return <ResultPageSkeleton />;
}

// ResultPageSkeleton — animate-pulse skeleton matching result page layout:
// - Header card (profile info)
// - Overview chart area
// - Cards grid (8 dimension cards)
function ResultPageSkeleton() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-6 animate-pulse">
      {/* Header card */}
      <div className="h-[88px] bg-bg-subtle rounded-[12px] mb-6" />
      {/* Overview chart */}
      <div className="h-[280px] bg-bg-subtle rounded-[12px] mb-6" />
      {/* AI overview card */}
      <div className="h-[120px] bg-bg-subtle rounded-[12px] mb-6" />
      {/* Dimension cards grid */}
      <div className="grid grid-cols-2 gap-3">
        {Array.from({ length: 8 }).map((_, i) => (
          <div key={i} className="h-[96px] bg-bg-subtle rounded-[12px]" />
        ))}
      </div>
    </div>
  );
}
```

Do NOT add `<Suspense>` around a `<ResultContent>` client component — use `loading.tsx` for skeletons instead.

### 13.6 React-Markdown Bundle

```bash
npm install react-markdown rehype-raw
# react-markdown v9+ is ESM only — no remark plugins needed for MVP
# rehype-raw is REQUIRED: preprocessInterpretation (§7.7) injects raw HTML <span> tags;
# rehype-raw is the plugin that allows react-markdown to render them.
# react-markdown v9 and rehype-raw both work in Server Components (pure ESM, no client required).
# No 'use client' needed for AIInterpretationSection — it is a Server Component.
```

Only import on the dimension detail page — it's not used on landing or overview.

### 13.7 Caching Headers

The result and dimension pages are static once generated. Set cache headers:
```typescript
// In API route or via fetch options
// getProfile uses: cache: 'force-cache'
// Next.js will cache the server-rendered HTML by default
// For ISR if needed later: revalidate: false (never revalidate)
```

---

## PART 14: FILE STRUCTURE

```
frontend/
├── app/
│   ├── layout.tsx                    # Root layout: Inter font, Toaster (Sonner)
│   ├── globals.css                   # CSS variables, base styles, keyframes (pulse-dot, etc.)
│   ├── not-found.tsx                 # Global 404 (M3)
│   ├── error.tsx                     # Global error boundary (B6)
│   ├── page.tsx                      # Landing page (SSR)
│   ├── form/
│   │   └── page.tsx                  # Form page
│   ├── processing/
│   │   └── [id]/
│   │       ├── page.tsx
│   │       ├── loading.tsx           # Pulsing dots skeleton (I8)
│   │       └── error.tsx             # Processing error boundary (B6)
│   └── result/
│       └── [id]/
│           ├── page.tsx              # Result overview
│           ├── loading.tsx           # Navigation skeleton
│           ├── error.tsx             # Result error boundary (B6)
│           └── [dimension]/
│               ├── page.tsx          # Dimension detail
│               ├── loading.tsx
│               └── error.tsx         # Dimension error boundary (B6)
│
├── components/
│   ├── ui/                           # shadcn components (auto-generated)
│   │   ├── accordion.tsx
│   │   ├── calendar.tsx
│   │   ├── popover.tsx
│   │   ├── radio-group.tsx
│   │   ├── select.tsx
│   │   └── tooltip.tsx
│   ├── landing/
│   │   ├── LandingNav.tsx            # Client (scroll)
│   │   ├── HeroSection.tsx           # Server
│   │   ├── HeroIllustration.tsx      # Server (inline SVG)
│   │   ├── HowItWorksSection.tsx     # Server
│   │   ├── DimensionsPreviewSection.tsx  # Server
│   │   ├── TrustBuildingSection.tsx  # Server
│   │   ├── SamplePreviewSection.tsx  # Server
│   │   ├── FAQSection.tsx            # Client (accordion)
│   │   ├── FinalCTASection.tsx       # Server
│   │   └── LandingFooter.tsx         # Server
│   ├── form/
│   │   ├── BirthInputForm.tsx        # Client
│   │   └── DatePickerField.tsx       # Client
│   ├── processing/
│   │   ├── ProcessingScreen.tsx      # Client
│   │   ├── StepIndicator.tsx         # (child, receives state)
│   │   └── FunFactRotator.tsx        # Client
│   ├── result/
│   │   ├── ResultHeader.tsx          # Server (ShareButton island)
│   │   ├── ShareButton.tsx           # Client
│   │   ├── ProfileHeaderCard.tsx     # Server
│   │   ├── OverviewChartCard.tsx     # Server wrapper
│   │   ├── AIOverviewCard.tsx        # Server
│   │   ├── DimensionCardsGrid.tsx    # Server
│   │   ├── DimensionCard.tsx         # Server (Link)
│   │   ├── AlertBadge.tsx            # Server
│   │   ├── FeedbackWidget.tsx        # Client
│   │   └── ResultFooter.tsx          # Server
│   ├── detail/
│   │   ├── DetailHeader.tsx          # Server (ShareButton island)
│   │   ├── DimensionTitleBlock.tsx   # Server
│   │   ├── ChartCard.tsx             # Server wrapper
│   │   ├── AlertsSummarySection.tsx  # Server
│   │   ├── AIInterpretationSection.tsx  # Server (react-markdown)
│   │   └── DimensionNavigation.tsx   # Server (links)
│   └── charts/
│       ├── LifetimeChart.tsx         # Client
│       ├── DecadeChart.tsx           # Client
│       ├── MonthlyChart.tsx          # Client
│       ├── OverviewRadarChart.tsx    # Client
│       ├── OverviewBarChart.tsx      # Client
│       ├── ChartSkeleton.tsx         # Server (static UI)
│       └── chartConfig.ts            # Constants (not a component)
│
├── lib/
│   ├── api.ts                        # API client functions
│   ├── types.ts                      # TypeScript interfaces
│   ├── constants.ts                  # DIMENSION_ICONS, LABELS, BIRTH_HOURS, FUN_FACTS
│   ├── tokens.ts                     # Design tokens (colors) — mirrored in tailwind.config.ts
│   └── utils.ts                      # preprocessInterpretation and other helpers
│
├── public/
│   └── images/
│       └── sample-result-preview.png  # Static screenshot for landing page
│
├── tailwind.config.ts
├── next.config.ts
└── tsconfig.json
```

---

## PART 15: IMPLEMENTATION ORDER

Follow this order to enable parallel backend development:

**Day 1 (Foundation):**
1. Next.js 15 project init: `npx create-next-app@latest frontend --typescript --tailwind --app`
2. shadcn init: `npx shadcn@latest init` (choose default style, slate base)
3. Add shadcn components: accordion, calendar, popover, radio-group, select, tooltip
4. Install: `recharts react-markdown sonner lucide-react date-fns`
5. Set up `globals.css` CSS variables, `tailwind.config.ts` token extension
6. Create `lib/types.ts`, `lib/constants.ts`, `lib/api.ts` (with mock data fallback)

**Day 1-2 (Landing):**
7. Build all landing sections (Server Components — fastest to build)
8. LandingNav (Client — add scroll border after static content works)
9. FAQSection with Accordion
10. Mobile test at 375px

**Day 2-3 (Form + Processing):**
11. BirthInputForm with all fields and validation
12. DatePickerField with shadcn Calendar
13. ProcessingScreen with polling logic (mock API → redirect after 5s for testing)
14. FunFactRotator

**Day 3-4 (Result Page):**
15. ProfileHeaderCard, AIOverviewCard
16. DimensionCardsGrid + DimensionCard
17. AlertBadge, ShareButton, FeedbackWidget
18. OverviewBarChart (simpler, test on mobile first)
19. OverviewRadarChart (desktop)

**Day 4-5 (Dimension Detail + Charts):**
20. DetailHeader, DimensionTitleBlock, AlertsSummarySection
21. AIInterpretationSection with react-markdown
22. DimensionNavigation
23. ChartCard wrapper
24. LifetimeChart (12 points, with alert markers)
25. DecadeChart (10 points)
26. MonthlyChart (13 points)

**Day 5 (Polish + Testing):**
27. Loading skeletons: `loading.tsx` for result, dimension, and processing routes (I8)
28. Error boundaries: `error.tsx` for all routes (B6) + global `not-found.tsx` (M3)
29. Mobile responsive review at 375px and 414px
30. Accessibility audit (tab nav, ARIA labels, focus-first-error I9)
31. Lighthouse run (target: Performance ≥ 90, SEO 100)
32. Verify: no "7 lĩnh vực" copy remaining, all 8 dimensions shown (I11)

---

## PART 16: ENVIRONMENT & CONFIGURATION

```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000

# .env.production (set in Vercel dashboard)
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```

```typescript
// next.config.ts
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  // No external images for MVP — all assets local
  images: {
    formats: ['image/webp'],
  },

  // Strict mode for development
  reactStrictMode: true,
};

export default nextConfig;
```

```typescript
// tsconfig.json (strict mode)
// NOTE (B7): This project does NOT use a src/ directory. All source files live at frontend/ root.
// Use "@/*": ["./*"] — this maps @/components/... → frontend/components/...
// If you init with create-next-app and it generates "@/*": ["./src/*"], change it immediately.
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

---

## QUICK REFERENCE: shadcn Component Usage

```bash
# Install these shadcn components
npx shadcn@latest add accordion
npx shadcn@latest add calendar
npx shadcn@latest add popover
npx shadcn@latest add radio-group
npx shadcn@latest add select
npx shadcn@latest add tooltip

# Install Sonner separately (shadcn's toast recommendation)
npm install sonner

# Add Sonner to root layout:
# <Toaster richColors position="bottom-center" />
```

---

*End of Frontend Design Spec v1.2 — 2026-03-27 (v1.2 fixes: NB1 rehype-raw consistency; NI1 tokens.ts in Part 14; NI2 AIInterpretationSection Server Component note; NI3 remove result/not-found.tsx; NI4 sessionStorage in handleSubmit; NM1 result loading skeleton; NM2 useIsMobile hook; NM3 standardize LifetimeChart mobile interval)*
