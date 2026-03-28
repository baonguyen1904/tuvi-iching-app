# Frontend Plan — Tasks 10-12: Error Boundaries, Accessibility, Polish

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans. Steps use checkbox (`- [ ]`) syntax.

**Spec reference:** `docs/superpowers/specs/frontend/05-api-a11y-perf.md`

**Prerequisites:** Tasks 1-9 completed (all pages and components built)

---

## Task 10: Error Boundaries + Loading States

**Goal:** Every route has a loading skeleton and an error boundary so the app never shows a blank screen or an unhandled crash.

**Files to create (8):**
- `frontend/app/not-found.tsx`
- `frontend/app/error.tsx`
- `frontend/app/result/[id]/error.tsx`
- `frontend/app/result/[id]/[dimension]/error.tsx`
- `frontend/app/processing/[id]/error.tsx`
- `frontend/app/processing/[id]/loading.tsx`
- `frontend/app/result/[id]/loading.tsx`
- `frontend/app/result/[id]/[dimension]/loading.tsx`

---

- [ ] **Step 10.1: Create `frontend/app/not-found.tsx` (Server Component — global 404)**

```tsx
// frontend/app/not-found.tsx
import Link from 'next/link';

export default function NotFound() {
  return (
    <main id="main-content" className="min-h-screen bg-bg-primary flex items-center justify-center px-4">
      <div className="text-center max-w-md">
        <p className="text-6xl font-bold text-accent mb-4">404</p>
        <h1 className="text-2xl font-semibold text-text-primary mb-2">
          Trang không tồn tại
        </h1>
        <p className="text-text-secondary mb-6">
          Trang này không tồn tại hoặc đã bị xóa.
        </p>
        <Link
          href="/"
          className="inline-block bg-accent text-white rounded-md px-5 py-2.5 text-sm font-medium hover:bg-accent-hover transition-colors"
        >
          Về trang chủ
        </Link>
      </div>
    </main>
  );
}
```

---

- [ ] **Step 10.2: Create `frontend/app/error.tsx` (Client Component — global error boundary)**

```tsx
// frontend/app/error.tsx
'use client';

import { useEffect } from 'react';
import Link from 'next/link';

interface ErrorProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function GlobalError({ error, reset }: ErrorProps) {
  useEffect(() => {
    console.error('[GlobalError]', error);
  }, [error]);

  return (
    <main id="main-content" className="min-h-screen bg-bg-primary flex items-center justify-center px-4">
      <div className="text-center max-w-md">
        <p className="text-5xl mb-4">⚠️</p>
        <h1 className="text-2xl font-semibold text-text-primary mb-2">
          Đã xảy ra lỗi
        </h1>
        <p className="text-text-secondary mb-6">
          Đã xảy ra lỗi không mong muốn. Vui lòng thử lại hoặc quay về trang chủ.
        </p>
        <div className="flex gap-3 justify-center">
          <button
            onClick={reset}
            className="bg-accent text-white rounded-md px-5 py-2.5 text-sm font-medium hover:bg-accent-hover transition-colors"
          >
            Thử lại
          </button>
          <Link
            href="/"
            className="bg-transparent border border-border text-text-primary rounded-md px-5 py-2.5 text-sm font-medium hover:bg-bg-subtle transition-colors"
          >
            Về trang chủ
          </Link>
        </div>
      </div>
    </main>
  );
}
```

---

- [ ] **Step 10.3: Create `frontend/app/result/[id]/error.tsx` (Client Component)**

```tsx
// frontend/app/result/[id]/error.tsx
'use client';

import { useEffect } from 'react';
import Link from 'next/link';

interface ErrorProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function ResultError({ error, reset }: ErrorProps) {
  useEffect(() => {
    console.error('[ResultError]', error);
  }, [error]);

  return (
    <main id="main-content" className="min-h-screen bg-bg-primary flex items-center justify-center px-4">
      <div className="text-center max-w-md">
        <p className="text-5xl mb-4">📊</p>
        <h2 className="text-xl font-semibold text-text-primary mb-2">
          Không thể tải kết quả
        </h2>
        <p className="text-text-secondary mb-6">
          Không thể tải kết quả luận giải. Vui lòng thử lại hoặc nhập lại thông tin.
        </p>
        <div className="flex gap-3 justify-center">
          <button
            onClick={reset}
            className="bg-accent text-white rounded-md px-5 py-2.5 text-sm font-medium hover:bg-accent-hover transition-colors"
          >
            Thử lại
          </button>
          <Link
            href="/form"
            className="bg-transparent border border-border text-text-primary rounded-md px-5 py-2.5 text-sm font-medium hover:bg-bg-subtle transition-colors"
          >
            Nhập lại
          </Link>
        </div>
      </div>
    </main>
  );
}
```

---

- [ ] **Step 10.4: Create `frontend/app/result/[id]/[dimension]/error.tsx` (Client Component)**

```tsx
// frontend/app/result/[id]/[dimension]/error.tsx
'use client';

import { useEffect } from 'react';
import Link from 'next/link';

interface ErrorProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function DimensionError({ error, reset }: ErrorProps) {
  useEffect(() => {
    console.error('[DimensionError]', error);
  }, [error]);

  return (
    <main id="main-content" className="min-h-screen bg-bg-primary flex items-center justify-center px-4">
      <div className="text-center max-w-md">
        <p className="text-5xl mb-4">🔍</p>
        <h2 className="text-xl font-semibold text-text-primary mb-2">
          Không thể tải lĩnh vực này
        </h2>
        <p className="text-text-secondary mb-6">
          Không thể tải thông tin lĩnh vực. Vui lòng thử lại hoặc quay về tổng quan.
        </p>
        <div className="flex gap-3 justify-center">
          <button
            onClick={reset}
            className="bg-accent text-white rounded-md px-5 py-2.5 text-sm font-medium hover:bg-accent-hover transition-colors"
          >
            Thử lại
          </button>
          <Link
            href=".."
            className="bg-transparent border border-border text-text-primary rounded-md px-5 py-2.5 text-sm font-medium hover:bg-bg-subtle transition-colors"
          >
            Về tổng quan
          </Link>
        </div>
      </div>
    </main>
  );
}
```

---

- [ ] **Step 10.5: Create `frontend/app/processing/[id]/error.tsx` (Client Component)**

```tsx
// frontend/app/processing/[id]/error.tsx
'use client';

import { useEffect } from 'react';
import Link from 'next/link';

interface ErrorProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function ProcessingError({ error, reset }: ErrorProps) {
  useEffect(() => {
    console.error('[ProcessingError]', error);
  }, [error]);

  return (
    <main id="main-content" className="min-h-screen bg-bg-primary flex items-center justify-center px-4">
      <div className="text-center max-w-md">
        <p className="text-5xl mb-4">⏳</p>
        <h2 className="text-xl font-semibold text-text-primary mb-2">
          Lỗi trong quá trình xử lý
        </h2>
        <p className="text-text-secondary mb-6">
          Đã xảy ra lỗi trong quá trình tính toán và luận giải. Vui lòng thử lại.
        </p>
        <div className="flex gap-3 justify-center">
          <button
            onClick={reset}
            className="bg-accent text-white rounded-md px-5 py-2.5 text-sm font-medium hover:bg-accent-hover transition-colors"
          >
            Thử lại
          </button>
          <Link
            href="/form"
            className="bg-transparent border border-border text-text-primary rounded-md px-5 py-2.5 text-sm font-medium hover:bg-bg-subtle transition-colors"
          >
            Nhập lại thông tin
          </Link>
        </div>
      </div>
    </main>
  );
}
```

---

- [ ] **Step 10.6: Create `frontend/app/processing/[id]/loading.tsx` (3 pulsing dots)**

This mirrors the visual rhythm of `ProcessingAnimation` so the loading state feels continuous with the actual processing page.

```tsx
// frontend/app/processing/[id]/loading.tsx
export default function ProcessingLoading() {
  return (
    <main
      id="main-content"
      className="min-h-screen bg-bg-primary flex items-center justify-center px-4"
      role="status"
      aria-live="polite"
      aria-label="Đang chuẩn bị..."
    >
      <div className="text-center">
        {/* Pulsing dots — matches ProcessingAnimation (I8) */}
        <div className="flex items-center justify-center gap-2 mb-4">
          <span
            className="w-3 h-3 rounded-full bg-accent animate-pulse"
            style={{ animationDelay: '0ms' }}
          />
          <span
            className="w-3 h-3 rounded-full bg-accent animate-pulse"
            style={{ animationDelay: '160ms' }}
          />
          <span
            className="w-3 h-3 rounded-full bg-accent animate-pulse"
            style={{ animationDelay: '320ms' }}
          />
        </div>
        <p className="text-sm text-text-secondary">Đang chuẩn bị...</p>
      </div>
    </main>
  );
}
```

---

- [ ] **Step 10.7: Create `frontend/app/result/[id]/loading.tsx` (ResultPageSkeleton)**

Skeleton structure mirrors the result page layout:
- Profile header (~88px)
- Overview radar chart placeholder (~280px)
- AI summary text lines (~120px)
- 8 dimension cards in a responsive grid

```tsx
// frontend/app/result/[id]/loading.tsx
export default function ResultLoading() {
  return (
    <main
      id="main-content"
      className="min-h-screen bg-bg-primary px-4 py-8"
      role="status"
      aria-live="polite"
      aria-label="Đang tải kết quả..."
    >
      <div className="max-w-3xl mx-auto space-y-6">

        {/* Profile header skeleton — ~88px */}
        <div className="bg-bg-surface rounded-[12px] border border-border shadow-md p-4 md:p-6 animate-pulse">
          <div className="flex items-start gap-4">
            <div className="w-12 h-12 rounded-full bg-bg-subtle flex-shrink-0" />
            <div className="flex-1 space-y-2">
              <div className="h-5 bg-bg-subtle rounded w-1/3" />
              <div className="h-4 bg-bg-subtle rounded w-1/2" />
              <div className="h-3 bg-bg-subtle rounded w-2/3" />
            </div>
          </div>
        </div>

        {/* Overview chart skeleton — ~280px */}
        <div className="bg-bg-surface rounded-[12px] border border-border shadow-md p-4 md:p-6 animate-pulse">
          <div className="h-5 bg-bg-subtle rounded w-1/4 mb-4" />
          <div className="w-full h-64 bg-bg-subtle rounded-lg" />
        </div>

        {/* AI overview text skeleton — ~120px */}
        <div className="bg-bg-surface rounded-[12px] border border-border shadow-md p-4 md:p-6 animate-pulse space-y-2">
          <div className="h-4 bg-bg-subtle rounded w-full" />
          <div className="h-4 bg-bg-subtle rounded w-5/6" />
          <div className="h-4 bg-bg-subtle rounded w-4/6" />
          <div className="h-4 bg-bg-subtle rounded w-5/6" />
          <div className="h-4 bg-bg-subtle rounded w-3/6" />
        </div>

        {/* 8 dimension cards grid skeleton */}
        <div>
          <div className="h-5 bg-bg-subtle rounded w-1/3 mb-4 animate-pulse" />
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {Array.from({ length: 8 }).map((_, i) => (
              <div
                key={i}
                className="bg-bg-surface rounded-[12px] border border-border shadow-md p-4 animate-pulse space-y-3"
              >
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg bg-bg-subtle" />
                  <div className="h-4 bg-bg-subtle rounded w-1/3" />
                </div>
                <div className="h-2 bg-bg-subtle rounded-full w-full" />
                <div className="h-3 bg-bg-subtle rounded w-2/3" />
              </div>
            ))}
          </div>
        </div>

      </div>
    </main>
  );
}
```

---

- [ ] **Step 10.8: Create `frontend/app/result/[id]/[dimension]/loading.tsx` (DimensionDetailSkeleton)**

Skeleton structure mirrors the dimension detail page layout:
- Back nav + header
- Dimension title + summary score
- Chart (3 tabs × chart area)
- Alert badges row
- 4 AI text lines
- Prev/next navigation

```tsx
// frontend/app/result/[id]/[dimension]/loading.tsx
export default function DimensionDetailLoading() {
  return (
    <main
      id="main-content"
      className="min-h-screen bg-bg-primary px-4 py-8"
      role="status"
      aria-live="polite"
      aria-label="Đang tải lĩnh vực..."
    >
      <div className="max-w-3xl mx-auto space-y-6">

        {/* Back nav skeleton */}
        <div className="h-4 bg-bg-subtle rounded w-24 animate-pulse" />

        {/* Dimension header skeleton */}
        <div className="bg-bg-surface rounded-[12px] border border-border shadow-md p-4 md:p-6 animate-pulse">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 rounded-lg bg-bg-subtle" />
            <div className="h-6 bg-bg-subtle rounded w-1/4" />
          </div>
          {/* Summary score bar */}
          <div className="h-3 bg-bg-subtle rounded-full w-full mb-2" />
          <div className="h-3 bg-bg-subtle rounded w-1/6 ml-auto" />
        </div>

        {/* Chart area skeleton — tabs + chart */}
        <div className="bg-bg-surface rounded-[12px] border border-border shadow-md p-4 md:p-6 animate-pulse">
          {/* Tab bar */}
          <div className="flex gap-2 mb-4">
            <div className="h-8 bg-bg-subtle rounded-md w-20" />
            <div className="h-8 bg-bg-subtle rounded-md w-20" />
            <div className="h-8 bg-bg-subtle rounded-md w-20" />
          </div>
          {/* Chart */}
          <div className="w-full h-48 bg-bg-subtle rounded-lg" />
        </div>

        {/* Alert badges skeleton */}
        <div className="flex flex-wrap gap-2 animate-pulse">
          <div className="h-7 bg-alert-positive-bg border border-alert-positive-bdr rounded-full w-32" />
          <div className="h-7 bg-alert-negative-bg border border-alert-negative-bdr rounded-full w-36" />
          <div className="h-7 bg-alert-positive-bg border border-alert-positive-bdr rounded-full w-28" />
        </div>

        {/* AI interpretation text skeleton — 4 lines */}
        <div className="bg-bg-surface rounded-[12px] border border-border shadow-md p-4 md:p-6 animate-pulse space-y-2">
          <div className="h-4 bg-bg-subtle rounded w-full" />
          <div className="h-4 bg-bg-subtle rounded w-5/6" />
          <div className="h-4 bg-bg-subtle rounded w-full" />
          <div className="h-4 bg-bg-subtle rounded w-4/6" />
        </div>

        {/* Prev / Next navigation skeleton */}
        <div className="flex justify-between items-center animate-pulse">
          <div className="h-10 bg-bg-subtle rounded-md w-28" />
          <div className="h-10 bg-bg-subtle rounded-md w-28" />
        </div>

      </div>
    </main>
  );
}
```

---

- [ ] **Step 10.9: Verify**

```bash
# 1. All error files must be Client Components
grep -rn "'use client'" \
  frontend/app/error.tsx \
  frontend/app/result/*/error.tsx \
  frontend/app/result/*/*/error.tsx \
  frontend/app/processing/*/error.tsx

# 2. All loading files must use animate-pulse
grep -rn "animate-pulse" \
  frontend/app/processing/*/loading.tsx \
  frontend/app/result/*/loading.tsx \
  frontend/app/result/*/*/loading.tsx

# 3. All loading files must have role="status" aria-live="polite"
grep -rn 'role="status"' \
  frontend/app/processing/*/loading.tsx \
  frontend/app/result/*/loading.tsx \
  frontend/app/result/*/*/loading.tsx

# 4. TypeScript check — no errors
cd frontend && npx tsc --noEmit
```

Expected: `grep` finds matches in every listed file; `tsc` exits 0.

---

- [ ] **Step 10.10: Commit**

```bash
git add \
  frontend/app/not-found.tsx \
  frontend/app/error.tsx \
  "frontend/app/result/[id]/error.tsx" \
  "frontend/app/result/[id]/[dimension]/error.tsx" \
  "frontend/app/processing/[id]/error.tsx" \
  "frontend/app/processing/[id]/loading.tsx" \
  "frontend/app/result/[id]/loading.tsx" \
  "frontend/app/result/[id]/[dimension]/loading.tsx"

git commit -m "feat: add error boundaries and loading skeletons for all routes"
```

---

## Task 11: Accessibility

**Goal:** The app meets WCAG 2.1 AA for the Vietnamese-language audience. All interactive elements are keyboard-navigable, screen-reader-friendly, and motion-safe.

**Files modified:** ~15 existing files

---

- [ ] **Step 11.1: Add skip link in `frontend/app/layout.tsx`**

The skip link is visually hidden until focused, letting keyboard users jump past the nav.

**Before:**
```tsx
// frontend/app/layout.tsx
// ...existing body/header/nav opening tags...
<body className={inter.variable}>
  <header>
    {/* nav content */}
  </header>
  <main>
```

**After:**
```tsx
// frontend/app/layout.tsx
<body className={inter.variable}>
  {/* Skip navigation link — visible on focus only */}
  <a
    href="#main-content"
    className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:bg-accent focus:text-white focus:px-4 focus:py-2 focus:rounded-md focus:text-sm focus:font-medium"
  >
    Bỏ qua điều hướng
  </a>
  <header>
    {/* nav content */}
  </header>
  <main>
```

---

- [ ] **Step 11.2: Add `id="main-content"` on all page `<main>` elements**

Every page file that renders a `<main>` tag must have `id="main-content"` so the skip link target resolves correctly.

Files to update:
- `frontend/app/page.tsx` (landing)
- `frontend/app/form/page.tsx`
- `frontend/app/processing/[id]/page.tsx`
- `frontend/app/result/[id]/page.tsx`
- `frontend/app/result/[id]/[dimension]/page.tsx`

**Pattern — find and add the id attribute:**

```tsx
// Before:
<main className="...">

// After:
<main id="main-content" className="...">
```

Apply this to every page's outermost `<main>` element. (Loading and error files already include `id="main-content"` from Task 10.)

---

- [ ] **Step 11.3: Chart ARIA wrappers — wrap all 5 `<ResponsiveContainer>` instances**

Charts are SVG-rendered and invisible to screen readers without explicit ARIA labeling. Wrap each chart in a `<figure>` with a `<figcaption>` for assistive technology.

The 5 chart locations:

1. **Overview radar chart** (`frontend/components/OverviewRadarChart.tsx` or inline in result page)
2. **Lifetime line chart** (dimension detail page or `DimensionLifetimeChart`)
3. **Decade line chart** (`DimensionDecadeChart`)
4. **Monthly bar chart** (`DimensionMonthlyChart`)
5. **Summary score bar** (if rendered as a chart rather than a progress bar)

**Before (each chart):**
```tsx
<ResponsiveContainer width="100%" height={280}>
  {/* chart content */}
</ResponsiveContainer>
```

**After (each chart — adapt label to context):**
```tsx
<figure aria-label="Biểu đồ tổng quan 8 lĩnh vực">
  <figcaption className="sr-only">
    Biểu đồ radar thể hiện điểm số 8 lĩnh vực: Sự nghiệp, Tiền bạc, Hôn nhân, Sức khỏe, Đất đai, Học tập, Con cái, Vận mệnh.
  </figcaption>
  <ResponsiveContainer width="100%" height={280}>
    {/* chart content */}
  </ResponsiveContainer>
</figure>
```

Use context-appropriate `aria-label` values:

| Chart | `aria-label` | `figcaption` text |
|-------|-------------|-------------------|
| Overview radar | `"Biểu đồ tổng quan 8 lĩnh vực"` | `"Biểu đồ radar thể hiện điểm số 8 lĩnh vực."` |
| Lifetime line | `"Biểu đồ điểm số trọn đời"` | `"Biểu đồ đường thể hiện điểm Dương, Âm, Trung bình theo độ tuổi."` |
| Decade line | `"Biểu đồ điểm số 10 năm"` | `"Biểu đồ đường thể hiện điểm Dương, Âm, Trung bình theo từng năm trong thập kỷ."` |
| Monthly bar | `"Biểu đồ điểm số theo tháng"` | `"Biểu đồ cột thể hiện điểm Dương, Âm, Trung bình theo từng tháng trong năm."` |
| Summary score | `"Thanh điểm tổng hợp lĩnh vực"` | `"Thanh điểm thể hiện điểm tổng hợp của lĩnh vực, thang điểm 0–100."` |

---

- [ ] **Step 11.4: Add `aria-label` to `AlertBadge` component**

The badge must announce its semantic meaning to screen readers, not just the visual tag text.

**File:** `frontend/components/AlertBadge.tsx`

**Before:**
```tsx
export function AlertBadge({ type, tag, level }: AlertBadgeProps) {
  return (
    <span className={cn('inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-medium border', ...)}>
      {type === 'positive' ? '▲' : '▼'} {tag}
    </span>
  );
}
```

**After:**
```tsx
export function AlertBadge({ type, tag, level, count }: AlertBadgeProps) {
  const ariaLabel = type === 'positive'
    ? `${count ?? 1} cơ hội tích cực: ${tag}`
    : `${count ?? 1} điểm cần thận trọng: ${tag}`;

  return (
    <span
      className={cn('inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-medium border', ...)}
      aria-label={ariaLabel}
    >
      <span aria-hidden="true">{type === 'positive' ? '▲' : '▼'}</span>
      {tag}
    </span>
  );
}
```

If `AlertBadge` is used inside a list (e.g., inside `DimensionCard`), also wrap the badge list in:
```tsx
<ul role="list" aria-label="Các cảnh báo">
  {alerts.map((a, i) => (
    <li key={i}>
      <AlertBadge {...a} count={1} />
    </li>
  ))}
</ul>
```

---

- [ ] **Step 11.5: Add `aria-label` and `aria-hidden` to `ShareButton`**

**File:** `frontend/components/ShareButton.tsx`

**Before:**
```tsx
<button onClick={handleShare} className="...">
  <ShareIcon className="w-4 h-4" />
  Chia sẻ
</button>
```

**After:**
```tsx
<button
  onClick={handleShare}
  className="..."
  aria-label="Sao chép liên kết để chia sẻ kết quả"
>
  <ShareIcon className="w-4 h-4" aria-hidden="true" />
  Chia sẻ
</button>
```

---

- [ ] **Step 11.6: Add ARIA attributes to `StepIndicator`**

`StepIndicator` shows the 3-step processing progress. Each step needs an ordered list structure and `aria-current` on the active step.

**File:** `frontend/components/StepIndicator.tsx`

**Before:**
```tsx
<div className="flex items-center gap-2">
  {steps.map((step, i) => (
    <div key={i} className={cn('step', { active: i === currentStep })}>
      {step.label}
    </div>
  ))}
</div>
```

**After:**
```tsx
<ol role="list" aria-label="Các bước xử lý" className="flex items-center gap-2">
  {steps.map((step, i) => (
    <li
      key={i}
      className={cn('step', { active: i === currentStep })}
      aria-current={i === currentStep ? 'step' : undefined}
    >
      {step.label}
    </li>
  ))}
</ol>
```

---

- [ ] **Step 11.7: Add `<nav>` landmark to `DimensionNavigation`**

**File:** `frontend/components/DimensionNavigation.tsx`

**Before:**
```tsx
<div className="flex justify-between items-center">
  {prev && <Link href={prev.href}>← {prev.label}</Link>}
  {next && <Link href={next.href}>{next.label} →</Link>}
</div>
```

**After:**
```tsx
<nav aria-label="Điều hướng giữa các lĩnh vực">
  <div className="flex justify-between items-center">
    {prev && (
      <Link href={prev.href} aria-label={`Lĩnh vực trước: ${prev.label}`}>
        <span aria-hidden="true">←</span> {prev.label}
      </Link>
    )}
    {next && (
      <Link href={next.href} aria-label={`Lĩnh vực tiếp theo: ${next.label}`}>
        {next.label} <span aria-hidden="true">→</span>
      </Link>
    )}
  </div>
</nav>
```

---

- [ ] **Step 11.8: Wrap gender radio group in `<fieldset><legend>`**

**File:** `frontend/app/form/page.tsx` (or `frontend/components/BirthForm.tsx`)

**Before:**
```tsx
<div className="space-y-2">
  <label className="text-sm font-medium text-text-primary">Giới tính</label>
  <RadioGroup value={gender} onValueChange={setGender}>
    <RadioGroupItem value="male" id="male" />
    <label htmlFor="male">Nam</label>
    <RadioGroupItem value="female" id="female" />
    <label htmlFor="female">Nữ</label>
  </RadioGroup>
</div>
```

**After:**
```tsx
<fieldset className="space-y-2">
  <legend className="text-sm font-medium text-text-primary mb-1.5">Giới tính</legend>
  <RadioGroup value={gender} onValueChange={setGender} className="flex gap-4">
    <div className="flex items-center gap-2">
      <RadioGroupItem value="male" id="gender-male" />
      <label htmlFor="gender-male" className="text-sm text-text-primary cursor-pointer">Nam</label>
    </div>
    <div className="flex items-center gap-2">
      <RadioGroupItem value="female" id="gender-female" />
      <label htmlFor="gender-female" className="text-sm text-text-primary cursor-pointer">Nữ</label>
    </div>
  </RadioGroup>
</fieldset>
```

---

- [ ] **Step 11.9: Add `role="status" aria-live="polite"` to all loading states (loading.tsx)**

This is already included in the loading files created in Task 10 (Steps 10.6–10.8). Verify all 3 loading files have these attributes:

```tsx
// Verify in all 3 loading files:
<main
  id="main-content"
  role="status"
  aria-live="polite"
  aria-label="Đang tải..."
>
```

If any loading file from a prior task is missing these, add them now.

---

- [ ] **Step 11.10: Verify `prefers-reduced-motion` in `globals.css`**

Animations (pulsing dots, processing animation, skeleton shimmer) must respect the user's motion preferences.

**File:** `frontend/app/globals.css`

Ensure this block exists (add if missing):

```css
/* Respect reduced motion preferences */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

---

- [ ] **Step 11.11: Verify all accessibility changes**

```bash
# 1. Skip link exists in layout
grep -n "Bỏ qua điều hướng" frontend/app/layout.tsx

# 2. All page <main> elements have id="main-content"
grep -rn 'id="main-content"' frontend/app/

# 3. Chart figure wrappers present
grep -rn 'aria-label.*[Bb]iểu đồ' frontend/components/

# 4. AlertBadge aria-label
grep -n 'aria-label' frontend/components/AlertBadge.tsx

# 5. ShareButton aria-label + aria-hidden on icon
grep -n 'aria-label\|aria-hidden' frontend/components/ShareButton.tsx

# 6. StepIndicator ol role="list"
grep -n 'role="list"' frontend/components/StepIndicator.tsx

# 7. DimensionNavigation nav landmark
grep -n 'aria-label="Điều hướng' frontend/components/DimensionNavigation.tsx

# 8. Gender fieldset/legend
grep -n 'fieldset\|legend' frontend/app/form/page.tsx frontend/components/BirthForm.tsx 2>/dev/null

# 9. prefers-reduced-motion in globals.css
grep -n 'prefers-reduced-motion' frontend/app/globals.css
```

Expected: every `grep` returns at least one match.

---

- [ ] **Step 11.12: Commit**

```bash
git add \
  frontend/app/layout.tsx \
  frontend/app/page.tsx \
  frontend/app/form/page.tsx \
  "frontend/app/processing/[id]/page.tsx" \
  "frontend/app/result/[id]/page.tsx" \
  "frontend/app/result/[id]/[dimension]/page.tsx" \
  frontend/components/AlertBadge.tsx \
  frontend/components/ShareButton.tsx \
  frontend/components/StepIndicator.tsx \
  frontend/components/DimensionNavigation.tsx \
  frontend/app/globals.css

git commit -m "feat: add accessibility — skip link, ARIA landmarks, chart wrappers, motion safety"
```

---

## Task 12: Mobile Testing + Final Polish

**Goal:** Verify the complete app meets mobile-first quality standards before the MVP test group receives access. This is a verification-only task — no new files are created unless a bug is found that requires a fix.

**Prerequisites:** Dev server running (`npm run dev` in `frontend/`)

---

- [ ] **Step 12.1: Start dev server**

```bash
cd frontend && npm run dev
# Open http://localhost:3000 in a browser
```

To simulate mobile, use browser DevTools → toggle device toolbar → set to **375 × 812** (iPhone SE / iPhone 14 size).

---

- [ ] **Step 12.2: Landing page at 375px**

Check visually and with DevTools:

| Element | Expected |
|---------|----------|
| `<h1>` text size | ≥ 28px (heading-xl mobile breakpoint) |
| Feature/benefit grid | 1 column on mobile |
| CTA button | Full-width or at least 280px wide |
| Horizontal scroll | None (no overflow-x) |
| Spacing around sections | ≥ 40px (py-10) |

If any item fails, fix the Tailwind classes in the affected component.

---

- [ ] **Step 12.3: Touch targets ≥ 44px**

All tappable elements must meet the 44×44px minimum (WCAG 2.5.5 and Apple HIG).

Verify each:

| Element | How to check |
|---------|-------------|
| Primary CTA button | Inspect → computed height ≥ 44px |
| Gender radio items | Computed height ≥ 44px (use `py-3` or `h-11`) |
| Accordion items (FAQ) | Computed height ≥ 44px per row |
| Dimension cards (clickable) | Computed height ≥ 64px |
| Prev/Next nav links | Computed height ≥ 44px |

If any fall short, add `min-h-[44px]` or increase padding.

---

- [ ] **Step 12.4: Vietnamese text overflow on CTAs**

Long Vietnamese text can break button layouts.

Check these text strings don't overflow or wrap unexpectedly:

| Text | Location |
|------|----------|
| `"Xem kết quả luận giải"` | Result CTA |
| `"Nhập thông tin ngày sinh"` | Form page heading |
| `"Đang tính toán lá số..."` | Processing step label |
| `"Tìm hiểu thêm về lĩnh vực này"` | Dimension CTA |

Fix: use `text-wrap: balance` or `break-words` if text wraps awkwardly.

---

- [ ] **Step 12.5: Chart visibility at 375px**

Per design spec, the radar chart is hidden on mobile (too dense), and the bar chart must be visible.

| Chart | Mobile (375px) | Desktop (768px+) |
|-------|---------------|-----------------|
| Overview radar | Hidden (`hidden sm:block`) | Visible |
| Dimension bar (monthly) | Visible | Visible |
| Dimension line (lifetime/decade) | Visible | Visible |

Verify with DevTools: radar chart container must have `display: none` at 375px, bar chart must be visible.

---

- [ ] **Step 12.6: Chart label density at 375px**

At narrow widths, chart x-axis labels overlap if `interval={0}` (show all). Confirm interval adapts.

**Expected behavior in chart components:**

```tsx
// In any chart component using isMobile detection:
const isMobile = useIsMobile(); // hook or window check

<XAxis
  dataKey="label"
  interval={isMobile ? 1 : 0}
  tick={{ fontSize: isMobile ? 11 : 12 }}
/>
```

If the hook/detection doesn't exist yet:

```tsx
// frontend/hooks/useIsMobile.ts
'use client';
import { useState, useEffect } from 'react';

export function useIsMobile(breakpoint = 640): boolean {
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const check = () => setIsMobile(window.innerWidth < breakpoint);
    check();
    window.addEventListener('resize', check);
    return () => window.removeEventListener('resize', check);
  }, [breakpoint]);

  return isMobile;
}
```

Apply to all 3 chart components (lifetime, decade, monthly).

---

- [ ] **Step 12.7: Grid column counts**

Verify responsive grid behavior:

| Component | Mobile (375px) | Desktop (640px+) |
|-----------|---------------|-----------------|
| `DimensionCards` (result overview) | 1 column | 2 columns |
| `DimensionsPreview` (landing page) | 2 columns | 4 columns |

Expected Tailwind classes:
```tsx
// DimensionCards
<div className="grid grid-cols-1 sm:grid-cols-2 gap-4">

// DimensionsPreview
<div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
```

Fix if different.

---

- [ ] **Step 12.8: Lighthouse audit**

Run in Chrome DevTools → Lighthouse tab → Mobile preset:

| Category | Target |
|----------|--------|
| Performance | ≥ 90 |
| Accessibility | ≥ 90 (aim for 100) |
| Best Practices | ≥ 90 |
| SEO | 100 |

Common fixes if Performance < 90:
- Ensure `next/image` is used for all images
- Ensure font is loaded with `display: swap`
- Check for render-blocking scripts

Common fixes if SEO < 100:
- Ensure each page has a unique `<title>` and `<meta name="description">`
- Ensure links have descriptive text (not "click here")

---

- [ ] **Step 12.9: Bundle size check**

```bash
cd frontend && npm run build
```

Review the route size table output. Expected thresholds for MVP:

| Route | First Load JS |
|-------|--------------|
| `/` (landing) | < 100 kB |
| `/form` | < 120 kB |
| `/processing/[id]` | < 100 kB |
| `/result/[id]` | < 150 kB |
| `/result/[id]/[dimension]` | < 150 kB |

If any route exceeds its threshold, investigate with:
```bash
cd frontend && npx @next/bundle-analyzer
```

Common causes: importing entire icon libraries, large chart bundles not lazy-loaded.

---

- [ ] **Step 12.10: Verify no "7 lĩnh vực" text**

Per CLAUDE.md Rule 4, the app has **8 dimensions** (van_menh + 7). The phrase "7 lĩnh vực" must not appear anywhere in the UI.

```bash
grep -rn "7 lĩnh vực\|7 linh vuc\|seven dimensions" \
  frontend/app/ \
  frontend/components/ \
  frontend/lib/
```

Expected: no matches. If found, replace with "8 lĩnh vực" or the specific dimension names.

---

- [ ] **Step 12.11: Verify van_menh has no alert badges**

Per CLAUDE.md Rule 4, `van_menh` has charts but NO alerts.

```bash
# Check DimensionCard component — van_menh path must skip alerts
grep -n "van_menh\|alerts" frontend/components/DimensionCard.tsx

# Check dimension detail page — alerts section must be conditional
grep -n "van_menh\|alerts\|AlertBadge" "frontend/app/result/[id]/[dimension]/page.tsx"
```

The alerts section in the dimension detail page should be wrapped in a condition:

```tsx
{/* Do NOT show alerts for van_menh */}
{dimension !== 'van_menh' && alerts.length > 0 && (
  <section aria-label="Cảnh báo và cơ hội">
    {/* AlertBadge list */}
  </section>
)}
```

And in `DimensionCard`:
```tsx
{dimensionKey !== 'van_menh' && data.alerts.length > 0 && (
  <div className="flex flex-wrap gap-1 mt-2">
    {/* badges */}
  </div>
)}
```

---

- [ ] **Step 12.12: TypeScript + lint check**

```bash
cd frontend

# TypeScript
npx tsc --noEmit

# ESLint
npx eslint . --ext .ts,.tsx --max-warnings 0
```

Expected: both commands exit 0. Fix all type errors and lint warnings before committing.

---

- [ ] **Step 12.13: Final commit**

```bash
# Stage only files that were modified during polish
git add -p  # review changes interactively, or:
git add frontend/

git commit -m "feat: mobile polish — touch targets, chart intervals, grid fixes, a11y audit"
```

---

## Summary

| Task | Files | Outcome |
|------|-------|---------|
| **Task 10** | 8 new files | Every route shows a skeleton while loading and a friendly error on failure |
| **Task 11** | ~15 modified | Skip link, ARIA landmarks, chart wrappers, radio fieldset, motion safety |
| **Task 12** | 0–3 minor fixes | Verified mobile-ready: 375px layout, touch targets, Lighthouse ≥90, no regressions |

After Task 12 completes, the frontend is ready for integration with the Python backend (FastAPI) and the test group deployment.
