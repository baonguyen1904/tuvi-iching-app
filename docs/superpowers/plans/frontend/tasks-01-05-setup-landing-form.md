# Frontend Plan — Tasks 1-5: Setup, Design System, API, Landing, Form

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans. Steps use checkbox (`- [ ]`) syntax.

**Spec reference:** `docs/superpowers/specs/frontend/01-design-system.md` and `docs/superpowers/specs/frontend/02-landing-form.md`

---

## Task 1: Project Setup + Configuration

**Files:** `frontend/` (new project), `.env.local`, `next.config.ts`, `tsconfig.json`, `globals.css`

- [ ] **Step 1.1 — Create Next.js project**
```bash
npx create-next-app@latest frontend --typescript --tailwind --app --no-src-dir
```

- [ ] **Step 1.2 — Install deps**
```bash
cd frontend && npm install recharts react-markdown rehype-raw sonner lucide-react date-fns
```

- [ ] **Step 1.3 — Init shadcn**
```bash
npx shadcn@latest init
```

- [ ] **Step 1.4 — Add shadcn components**
```bash
npx shadcn@latest add accordion calendar popover radio-group select tooltip
```

- [ ] **Step 1.5 — Create `.env.local`**
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

- [ ] **Step 1.6 — Replace `next.config.ts`**
```typescript
import type { NextConfig } from 'next';
const nextConfig: NextConfig = {
  images: { formats: ['image/webp'] },
  reactStrictMode: true,
};
export default nextConfig;
```

- [ ] **Step 1.7 — Fix tsconfig paths**

In `tsconfig.json`, change `"@/*": ["./src/*"]` to `"@/*": ["./*"]`. Also ensure `"strict": true` and `"noUncheckedIndexedAccess": true` are set in `compilerOptions`.

- [ ] **Step 1.8 — Write `globals.css`**

Replace the default `app/globals.css` with:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --radius-sm: 6px; --radius-md: 8px; --radius-lg: 12px; --radius-xl: 16px; --radius-full: 9999px;
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.04);
  --shadow-lg: 0 4px 12px rgba(0,0,0,0.08);
}
*,*::before,*::after { box-sizing: border-box; }
html { -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }
body { background-color: #FAFAFA; color: #111827; }

@keyframes pulse-dot {
  0%,100% { transform: scale(0.8); opacity: 0.4; }
  50% { transform: scale(1.2); opacity: 1; }
}
.animate-pulse-dot { animation: pulse-dot 1.2s ease-in-out infinite; }

@media (prefers-reduced-motion: reduce) {
  .animate-pulse-dot,.animate-spin,.animate-pulse,.animate-bounce { animation: none; opacity: 1; transform: none; }
}
```

- [ ] **Step 1.9 — Commit**
```bash
git add frontend/ && git commit -m "feat: init Next.js 15 project with shadcn, deps, and config"
```

---

## Task 2: Design System Foundation

**Files:** `frontend/lib/tokens.ts`, `frontend/lib/types.ts`, `frontend/lib/constants.ts`, `frontend/lib/utils.ts`, `frontend/tailwind.config.ts`

- [ ] **Step 2.1 — Create `lib/tokens.ts`**

```typescript
export const colors = {
  bgPrimary: '#FAFAFA', bgSurface: '#FFFFFF', bgSubtle: '#F3F4F6',
  textPrimary: '#111827', textSecondary: '#6B7280', textTertiary: '#9CA3AF',
  accent: '#2563EB', accentHover: '#1D4ED8', accentLight: '#EFF6FF', accentBorder: '#BFDBFE',
  alertPositive: '#10B981', alertPositiveBg: '#ECFDF5', alertPositiveBdr: '#A7F3D0',
  alertNegative: '#F59E0B', alertNegativeBg: '#FFFBEB', alertNegativeBdr: '#FDE68A',
  chartDuong: '#2563EB', chartAm: '#F59E0B', chartTb: '#9CA3AF',
  border: '#E5E7EB', borderFocus: '#2563EB',
} as const;
```

- [ ] **Step 2.2 — Create `lib/types.ts`**

```typescript
export interface BirthInput {
  name?: string;
  birthDate: string;       // ISO: "1994-07-19"
  birthHour: string;       // enum: ty|suu|dan|mao|thin|ty_|ngo|mui|than|dau|tuat|hoi
  gender: 'male' | 'female';
  namXem: number;          // current year, auto-set
}

export interface ChartDataPoint {
  label: string;           // x-axis: "10-20", "2026", "Th.1"
  duong: number;
  am: number;
  tb: number;
}

export interface DimensionScores {
  // NOTE: label types vary by timeframe:
  //   lifetime → integer ages:  [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110]
  //   decade   → integer years: [2026, 2027, 2028, ..., 2035]
  //   monthly  → strings:       ["Th.1/2026", "Th.2/2026", ..., "Th.12/2026"]
  // Chart data transforms must call String(label) before using as React key or display text.
  labels: (string | number)[];
  duong: number[];
  am: number[];
  tb: number[];
}

export interface Alert {
  type: 'positive' | 'negative';
  period: string;          // matches chart x-axis label
  tag: string;             // Vietnamese tag text
  level: 30 | 50;
  starName: string;
}

export interface DimensionData {
  label: string;
  summaryScore: number;
  lifetime: DimensionScores;
  decade: DimensionScores;
  monthly: DimensionScores;
  alerts: Alert[];
  interpretation: string | null;   // null for van_menh
}

export interface ProfileMetadata {
  nam: string;             // "Giáp Tuất"
  menh: string;            // "Mộc"
  cuc: string;             // "Thủy Nhị Cục"
  amDuong: string;         // "Dương Nam"
  cungMenh: string;
  nguHanh: string;
}

export interface ProfileData {
  profileId: string;
  name: string | null;
  birthDate: string;
  birthHour: string;       // human-readable: "Giờ Dần (03:00–05:00)"
  gender: string;          // "Nam" | "Nữ"
  metadata: ProfileMetadata;
  overview: { summary: string };
  dimensions: Record<string, DimensionData>;
  createdAt: string;
}

export interface ProfileStatus {
  profileId: string;
  status: 'processing' | 'completed' | 'failed';
  step: string;
  message: string;
  aiProgress?: number;     // 0-8
}

export interface Feedback {
  profileId: string;
  helpful: boolean;
  comment?: string;
}
```

- [ ] **Step 2.3 — Create `lib/constants.ts`**

```typescript
export const DIMENSION_ICONS = {
  su_nghiep: 'Briefcase', tien_bac: 'TrendingUp', hon_nhan: 'Heart',
  suc_khoe: 'Activity', dat_dai: 'Home', hoc_tap: 'BookOpen',
  con_cai: 'Baby', van_menh: 'Compass',
} as const;

export const DIMENSION_LABELS = {
  su_nghiep: 'Sự nghiệp', tien_bac: 'Tiền bạc', hon_nhan: 'Hôn nhân',
  suc_khoe: 'Sức khỏe', dat_dai: 'Đất đai', hoc_tap: 'Học tập',
  con_cai: 'Con cái', van_menh: 'Vận mệnh',
} as const;

export const DIMENSION_ORDER = [
  'su_nghiep', 'tien_bac', 'hon_nhan', 'suc_khoe',
  'dat_dai', 'hoc_tap', 'con_cai', 'van_menh',
] as const;

export type DimensionKey = typeof DIMENSION_ORDER[number];

export const BIRTH_HOURS = [
  { value: 'ty',   label: 'Giờ Tý',   range: '23:00 – 01:00' },
  { value: 'suu',  label: 'Giờ Sửu',  range: '01:00 – 03:00' },
  { value: 'dan',  label: 'Giờ Dần',  range: '03:00 – 05:00' },
  { value: 'mao',  label: 'Giờ Mão',  range: '05:00 – 07:00' },
  { value: 'thin', label: 'Giờ Thìn', range: '07:00 – 09:00' },
  { value: 'ty_',  label: 'Giờ Tỵ',   range: '09:00 – 11:00' },
  { value: 'ngo',  label: 'Giờ Ngọ',  range: '11:00 – 13:00' },
  { value: 'mui',  label: 'Giờ Mùi',  range: '13:00 – 15:00' },
  { value: 'than', label: 'Giờ Thân', range: '15:00 – 17:00' },
  { value: 'dau',  label: 'Giờ Dậu',  range: '17:00 – 19:00' },
  { value: 'tuat', label: 'Giờ Tuất', range: '19:00 – 21:00' },
  { value: 'hoi',  label: 'Giờ Hợi',  range: '21:00 – 23:00' },
] as const;

export const FUN_FACTS: readonly string[] = [
  'Hệ thống Tử Vi Đẩu Số có 14 chính tinh và hơn 100 phụ tinh, tạo ra vô số tổ hợp độc đáo.',
  'Lá số của bạn là duy nhất — chỉ ai sinh cùng ngày, giờ và giới tính mới có lá số giống hệt.',
  'Tử Vi Đẩu Số có nguồn gốc hơn 1000 năm, được hoàn thiện trong triều đại Tống ở Trung Hoa.',
  'Hệ thống chia cuộc đời thành các chu kỳ 10 năm (Đại Vận) — mỗi chu kỳ có năng lượng riêng.',
  'AI đang phân tích hàng trăm điểm dữ liệu từ lá số của bạn để tạo luận giải cá nhân hóa.',
];
```

- [ ] **Step 2.4 — Create `lib/utils.ts`**

```typescript
'use client';
import * as React from 'react';

export function preprocessInterpretation(text: string): string {
  return text
    .replace(/▲/g, '<span class="text-emerald-600 font-medium">▲</span>')
    .replace(/▼/g, '<span class="text-amber-600 font-medium">▼</span>');
}

export function useIsMobile(breakpoint = 640): boolean {
  const [isMobile, setIsMobile] = React.useState(false);
  React.useEffect(() => {
    const mq = window.matchMedia(`(max-width: ${breakpoint - 1}px)`);
    setIsMobile(mq.matches);
    const handler = (e: MediaQueryListEvent) => setIsMobile(e.matches);
    mq.addEventListener('change', handler);
    return () => mq.removeEventListener('change', handler);
  }, [breakpoint]);
  return isMobile;
}
```

- [ ] **Step 2.5 — Update `tailwind.config.ts`**

```typescript
import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        bg: { primary: '#FAFAFA', surface: '#FFFFFF', subtle: '#F3F4F6' },
        text: { primary: '#111827', secondary: '#6B7280', tertiary: '#9CA3AF' },
        accent: { DEFAULT: '#2563EB', hover: '#1D4ED8', light: '#EFF6FF', border: '#BFDBFE' },
        alert: {
          'positive': '#10B981', 'positive-bg': '#ECFDF5', 'positive-bdr': '#A7F3D0',
          'negative': '#F59E0B', 'negative-bg': '#FFFBEB', 'negative-bdr': '#FDE68A',
        },
        chart: { duong: '#2563EB', am: '#F59E0B', tb: '#9CA3AF' },
        border: { DEFAULT: '#E5E7EB', focus: '#2563EB' },
      },
      fontFamily: { sans: ['var(--font-inter)', 'ui-sans-serif', 'system-ui', 'sans-serif'] },
      boxShadow: {
        sm: '0 1px 2px rgba(0,0,0,0.05)',
        md: '0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.04)',
        lg: '0 4px 12px rgba(0,0,0,0.08)',
      },
      borderRadius: { sm: '6px', md: '8px', lg: '12px', xl: '16px', full: '9999px' },
      maxWidth: { content: '768px' },
    },
  },
  plugins: [],
};
export default config;
```

- [ ] **Step 2.6 — Commit**
```bash
git add frontend/lib/ frontend/tailwind.config.ts && git commit -m "feat: add design system — tokens, types, constants, utils, tailwind theme"
```

---

## Task 3: API Client + Mock Data

**Files:** `frontend/lib/api.ts`, `frontend/lib/mock-data.ts`, `frontend/lib/utils.test.ts`, `frontend/vitest.config.ts`

- [ ] **Step 3.1 — Install Vitest**
```bash
cd frontend && npm install --save-dev vitest @vitejs/plugin-react
```

Add `"test": "vitest run"` to `package.json` scripts. Create `vitest.config.ts`:
```typescript
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
export default defineConfig({ plugins: [react()], test: { environment: 'node' } });
```

- [ ] **Step 3.2 — Create `lib/api.ts`**

```typescript
import type { BirthInput, ProfileData, ProfileStatus, Feedback } from '@/lib/types';

if (!process.env.NEXT_PUBLIC_API_URL) {
  console.warn('[TuViAI] NEXT_PUBLIC_API_URL is not set. Falling back to http://localhost:8000.');
}
const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';
const FETCH_TIMEOUT_MS = 30_000;

async function fetchAPI<T>(path: string, options?: RequestInit): Promise<T> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);
  try {
    const res = await fetch(`${API_BASE}${path}`, {
      ...options, signal: controller.signal,
      headers: { 'Content-Type': 'application/json', ...options?.headers },
    });
    if (!res.ok) {
      const error = await res.json().catch(() => ({}));
      throw new Error((error as { detail?: string }).detail ?? `HTTP ${res.status}`);
    }
    return res.json() as Promise<T>;
  } catch (err) {
    if (err instanceof Error && err.name === 'AbortError') {
      throw new Error('Yêu cầu quá thời gian. Vui lòng thử lại.');
    }
    throw err;
  } finally { clearTimeout(timeoutId); }
}

export const generateProfile = (input: BirthInput) =>
  fetchAPI<{ profileId: string; status: string }>('/api/generate', { method: 'POST', body: JSON.stringify(input) });

export const getProfileStatus = (id: string) =>
  fetchAPI<ProfileStatus>(`/api/profile/${id}/status`);

export const getProfile = (id: string) =>
  fetchAPI<ProfileData>(`/api/profile/${id}`, { cache: 'force-cache' });

export const submitFeedback = (feedback: Feedback) =>
  fetchAPI<void>('/api/feedback', { method: 'POST', body: JSON.stringify(feedback) });
```

- [ ] **Step 3.3 — Create `lib/mock-data.ts`**

Create a complete `ProfileData` mock object. Requirements:
- `profileId`: `"mock-profile-001"`
- `name`: `"Nguyễn Văn An"`
- `birthDate`: `"1994-07-19"`
- `birthHour`: `"Giờ Dần (03:00–05:00)"`
- `gender`: `"Nam"`
- `metadata`: `{ nam: "Giáp Tuất", menh: "Mộc", cuc: "Thủy Nhị Cục", amDuong: "Dương Nam", cungMenh: "Mệnh Cung Thìn", nguHanh: "Thổ" }`
- `overview.summary`: 2–3 sentence Vietnamese paragraph summarizing the chart
- All 8 dimensions with:
  - `lifetime.labels`: `[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110]` (integers)
  - `decade.labels`: `[2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034, 2035]` (integers)
  - `monthly.labels`: `["Th.1/2026", "Th.2/2026", ..., "Th.12/2026"]` (strings)
  - Realistic `duong`, `am`, `tb` arrays (values between -15 and 15)
  - `van_menh`: `alerts: []`, `interpretation: null`
  - Other 7 dimensions: 1–3 alerts mixing `positive`/`negative` types, levels `30` and `50`
  - Each non-van_menh dimension: `interpretation` is a Markdown string with at least one `##` heading and uses `▲`/`▼` markers

Example alert shape:
```typescript
{ type: 'positive', period: '2028', tag: 'Thiên Quan', level: 50, starName: 'Thiên Quan' }
```

Example interpretation snippet:
```markdown
## Sự nghiệp 2026–2035

▲ **Giai đoạn thăng tiến mạnh (2028–2029):** Thiên Quan chiếu cung Quan Lộc...

▼ **Cần thận trọng (2031):** Kình Dương nhập cung, nên tránh quyết định lớn...
```

- [ ] **Step 3.4 — Create `lib/utils.test.ts`**

```typescript
import { describe, it, expect } from 'vitest';
import { preprocessInterpretation } from './utils';

describe('preprocessInterpretation', () => {
  it('wraps ▲ with emerald span', () => {
    expect(preprocessInterpretation('▲ tốt')).toBe('<span class="text-emerald-600 font-medium">▲</span> tốt');
  });
  it('wraps ▼ with amber span', () => {
    expect(preprocessInterpretation('▼ kém')).toBe('<span class="text-amber-600 font-medium">▼</span> kém');
  });
  it('handles both markers', () => {
    const result = preprocessInterpretation('▲ thuận ▼ cần chú ý');
    expect(result).toContain('text-emerald-600');
    expect(result).toContain('text-amber-600');
  });
  it('returns unchanged when no markers', () => {
    expect(preprocessInterpretation('Bình thường')).toBe('Bình thường');
  });
});

describe('score normalisation', () => {
  const norm = (s: number) => ((s + 20) / 40) * 100;
  it('-20 → 0', () => expect(norm(-20)).toBe(0));
  it('0 → 50', () => expect(norm(0)).toBe(50));
  it('20 → 100', () => expect(norm(20)).toBe(100));
  it('8.7 → ~71.75', () => expect(norm(8.7)).toBeCloseTo(71.75));
});
```

- [ ] **Step 3.5 — Run tests**

```bash
cd frontend && npm test
```

Expected: 8 tests pass, 0 failures.

- [ ] **Step 3.6 — Commit**
```bash
git add frontend/lib/api.ts frontend/lib/mock-data.ts frontend/lib/utils.test.ts frontend/vitest.config.ts frontend/package.json
git commit -m "feat: add API client, mock data, and utils tests"
```

---

## Task 4: Landing Page

**Files:** `frontend/app/layout.tsx`, `frontend/app/page.tsx`, and 10 components under `frontend/components/landing/`

### Step 4.1 — Root layout (`app/layout.tsx`)

```typescript
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { Toaster } from 'sonner';
import './globals.css';

const inter = Inter({
  subsets: ['latin', 'vietnamese'],
  variable: '--font-inter',
  display: 'swap',
});

export const metadata: Metadata = {
  title: 'TuVi AI — Luận giải tử vi cá nhân hóa bằng AI',
  description: 'Nhập ngày giờ sinh, nhận luận giải tử vi chi tiết cho 8 lĩnh vực đời sống dựa trên Tử Vi Đẩu Số.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="vi" className={inter.variable}>
      <body className="font-sans bg-bg-primary text-text-primary">
        {children}
        <Toaster richColors position="top-center" />
      </body>
    </html>
  );
}
```

- [ ] **Step 4.2 — Landing page route (`app/page.tsx`)**

```typescript
import type { Metadata } from 'next';
import LandingNav from '@/components/landing/LandingNav';
import HeroSection from '@/components/landing/HeroSection';
import HowItWorksSection from '@/components/landing/HowItWorksSection';
import DimensionsPreviewSection from '@/components/landing/DimensionsPreviewSection';
import TrustBuildingSection from '@/components/landing/TrustBuildingSection';
import SamplePreviewSection from '@/components/landing/SamplePreviewSection';
import FAQSection from '@/components/landing/FAQSection';
import FinalCTASection from '@/components/landing/FinalCTASection';
import LandingFooter from '@/components/landing/LandingFooter';

export const metadata: Metadata = {
  title: 'TuVi AI — Luận giải tử vi cá nhân hóa bằng AI',
  description: 'Nhập ngày giờ sinh, nhận luận giải tử vi chi tiết cho 8 lĩnh vực đời sống dựa trên Tử Vi Đẩu Số.',
  openGraph: {
    title: 'TuVi AI — Luận giải tử vi cá nhân hóa bằng AI',
    description: 'AI phân tích lá số tử vi của bạn, cho ra luận giải chi tiết từng lĩnh vực.',
    type: 'website',
  },
};

export default function LandingPage() {
  return (
    <main>
      <LandingNav />
      <div className="max-w-3xl mx-auto px-4">
        <HeroSection />
        <HowItWorksSection />
      </div>
      <DimensionsPreviewSection />
      <div className="max-w-3xl mx-auto px-4">
        <TrustBuildingSection />
        <SamplePreviewSection />
      </div>
      <FAQSection />
      <div className="max-w-3xl mx-auto px-4">
        <FinalCTASection />
      </div>
      <LandingFooter />
    </main>
  );
}
```

- [ ] **Step 4.3 — `components/landing/LandingNav.tsx`** (Client Component)

Sticky nav with scroll border effect:

```typescript
'use client';
import { useState, useEffect } from 'react';
import Link from 'next/link';

export default function LandingNav() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 8);
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <nav
      className={`sticky top-0 z-50 h-14 flex items-center justify-between px-4
        bg-[rgba(250,250,250,0.9)] backdrop-blur-sm transition-colors duration-150
        ${scrolled ? 'border-b border-border' : 'border-b border-transparent'}`}
    >
      <span className="font-semibold text-text-primary text-sm">TuVi AI</span>
      <Link
        href="/form"
        className="bg-accent hover:bg-accent-hover text-white text-sm font-medium
          px-4 py-1.5 rounded-md transition-colors duration-100 h-9 flex items-center"
      >
        Xem luận giải
      </Link>
    </nav>
  );
}
```

- [ ] **Step 4.4 — `components/landing/HeroSection.tsx`** (Server Component)

```typescript
import Link from 'next/link';
import HeroIllustration from './HeroIllustration';

export default function HeroSection() {
  return (
    <section className="flex flex-col items-center text-center py-14 sm:py-20">
      <div className="max-w-[600px]">
        {/* Eyebrow badge */}
        <span className="inline-block bg-accent-light border border-accent-border text-accent
          text-xs font-medium px-3 py-1 rounded-full mb-6">
          Miễn phí · Không cần đăng ký
        </span>

        {/* Headline */}
        <h1 className="text-[28px] sm:text-[36px] font-bold text-text-primary leading-tight">
          Hiểu vận mệnh — Ra quyết định tốt hơn
        </h1>

        {/* Subheadline */}
        <p className="text-base text-text-secondary mt-4 max-w-[480px] mx-auto leading-relaxed">
          Luận giải tử vi cá nhân hóa bằng AI, dựa trên hệ thống Tử Vi Đẩu Số và kiến thức chuyên gia.
        </p>

        {/* CTA */}
        <Link
          href="/form"
          className="inline-flex items-center bg-accent hover:bg-accent-hover text-white
            font-medium text-base px-8 h-12 rounded-md mt-8
            hover:scale-[1.01] transition-all duration-100"
        >
          Xem luận giải miễn phí →
        </Link>

        {/* Sub-text */}
        <p className="text-xs text-text-tertiary mt-3">
          Miễn phí · Không cần đăng ký · Kết quả trong 30 giây
        </p>
      </div>

      {/* Hero illustration */}
      <div className="mt-12">
        <HeroIllustration />
      </div>
    </section>
  );
}
```

- [ ] **Step 4.5 — `components/landing/HeroIllustration.tsx`** (Server Component)

Inline SVG concentric circles — purely decorative, stroke only, no fill:

```typescript
export default function HeroIllustration() {
  return (
    <svg
      width="280" height="280"
      viewBox="0 0 280 280"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-label="Biểu đồ tử vi trực quan"
      role="img"
      className="w-[220px] h-[220px] sm:w-[280px] sm:h-[280px]"
    >
      {/* Concentric circles */}
      <circle cx="140" cy="140" r="120" stroke="#E5E7EB" strokeWidth="1" />
      <circle cx="140" cy="140" r="90"  stroke="#E5E7EB" strokeWidth="1" />
      <circle cx="140" cy="140" r="60"  stroke="#BFDBFE" strokeWidth="1.5" />
      <circle cx="140" cy="140" r="30"  stroke="#2563EB" strokeWidth="2" />

      {/* Node dots at compass points on outer circle */}
      <circle cx="140" cy="20"  r="5" fill="#2563EB" />
      <circle cx="260" cy="140" r="5" fill="#2563EB" />
      <circle cx="140" cy="260" r="5" fill="#2563EB" />
      <circle cx="20"  cy="140" r="5" fill="#2563EB" />

      {/* Node dots at 45° points on mid circle */}
      <circle cx="203.6" cy="76.4"  r="4" fill="#BFDBFE" />
      <circle cx="203.6" cy="203.6" r="4" fill="#BFDBFE" />
      <circle cx="76.4"  cy="203.6" r="4" fill="#BFDBFE" />
      <circle cx="76.4"  cy="76.4"  r="4" fill="#BFDBFE" />

      {/* Spokes */}
      <line x1="140" y1="20"  x2="140" y2="260" stroke="#E5E7EB" strokeWidth="1" strokeDasharray="4 4" />
      <line x1="20"  y1="140" x2="260" y2="140" stroke="#E5E7EB" strokeWidth="1" strokeDasharray="4 4" />

      {/* Center dot */}
      <circle cx="140" cy="140" r="6" fill="#2563EB" />
    </svg>
  );
}
```

- [ ] **Step 4.6 — `components/landing/HowItWorksSection.tsx`** (Server Component)

```typescript
import { ClipboardList, BarChart2, FileText } from 'lucide-react';

const steps = [
  {
    icon: ClipboardList,
    title: 'Nhập ngày giờ sinh',
    desc: 'Chỉ cần ngày sinh dương lịch, giờ sinh và giới tính.',
  },
  {
    icon: BarChart2,
    title: 'AI phân tích lá số',
    desc: 'Hệ thống tính toán biểu đồ vận mệnh dựa trên Tử Vi Đẩu Số.',
  },
  {
    icon: FileText,
    title: 'Nhận luận giải chi tiết',
    desc: '8 lĩnh vực đời sống (bao gồm Vận mệnh tổng thể), mỗi lĩnh vực có biểu đồ và lời khuyên cụ thể.',
  },
];

export default function HowItWorksSection() {
  return (
    <section className="py-10 sm:py-16">
      <h2 className="text-[18px] sm:text-[22px] font-semibold text-text-primary text-center mb-10">
        Cách hoạt động
      </h2>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 sm:gap-6 relative">
        {steps.map((step, i) => {
          const Icon = step.icon;
          return (
            <div
              key={i}
              className="flex flex-row sm:flex-col items-start sm:items-center
                sm:text-center gap-4 sm:gap-0 p-4 sm:p-6
                bg-bg-surface border border-border rounded-[12px]"
            >
              <div className="w-10 h-10 rounded-full bg-accent-light flex items-center justify-center flex-shrink-0">
                <Icon size={20} className="text-accent" />
              </div>
              <div className="sm:mt-4">
                <h3 className="text-[15px] font-semibold text-text-primary">
                  {step.title}
                </h3>
                <p className="text-sm text-text-secondary mt-1 sm:mt-2 leading-relaxed">
                  {step.desc}
                </p>
              </div>
            </div>
          );
        })}

        {/* Connector lines — desktop only */}
        <div className="hidden sm:block absolute top-[52px] left-[calc(33.33%-8px)] w-[calc(16px)]
          border-t border-dashed border-border pointer-events-none" />
        <div className="hidden sm:block absolute top-[52px] left-[calc(66.66%-8px)] w-[calc(16px)]
          border-t border-dashed border-border pointer-events-none" />
      </div>
    </section>
  );
}
```

- [ ] **Step 4.7 — `components/landing/DimensionsPreviewSection.tsx`** (Server Component)

```typescript
import { Briefcase, TrendingUp, Heart, Activity, Home, BookOpen, Baby, Compass, LucideIcon } from 'lucide-react';

const dimensions: Array<{ icon: LucideIcon; name: string; desc: string }> = [
  { icon: Briefcase,   name: 'Sự nghiệp', desc: 'Xu hướng thăng tiến, thời điểm thuận lợi' },
  { icon: TrendingUp,  name: 'Tiền bạc',  desc: 'Biến động tài chính, cơ hội tích lũy' },
  { icon: Heart,       name: 'Hôn nhân',  desc: 'Tình duyên, tương thích, thời điểm tốt' },
  { icon: Activity,    name: 'Sức khỏe',  desc: 'Giai đoạn cần chú ý, cách phòng tránh' },
  { icon: Home,        name: 'Đất đai',   desc: 'Mua bán bất động sản, thời điểm giao dịch' },
  { icon: BookOpen,    name: 'Học tập',   desc: 'Phát triển bản thân, học vấn, thi cử' },
  { icon: Baby,        name: 'Con cái',   desc: 'Vận con cái, thời điểm sinh con' },
  { icon: Compass,     name: 'Vận mệnh',  desc: 'Bức tranh toàn cục và vận khí tổng thể' },
];

export default function DimensionsPreviewSection() {
  return (
    <section className="py-10 sm:py-16 -mx-4 px-4 bg-bg-subtle">
      <div className="max-w-3xl mx-auto">
        <h2 className="text-[18px] sm:text-[22px] font-semibold text-text-primary text-center mb-2">
          8 lĩnh vực được phân tích
        </h2>
        <p className="text-sm text-text-secondary text-center mb-10">
          Mỗi lĩnh vực có biểu đồ và lời khuyên riêng
        </p>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {dimensions.map((dim) => {
            const Icon = dim.icon;
            return (
              <div
                key={dim.name}
                className="flex flex-col items-center text-center p-4 min-h-[100px]
                  bg-bg-surface border border-border rounded-[12px]
                  hover:border-accent-border transition-colors duration-150"
              >
                <div className="w-10 h-10 rounded-[8px] bg-accent-light flex items-center justify-center">
                  <Icon size={20} className="text-accent" />
                </div>
                <p className="text-[13px] font-medium text-text-primary mt-3">{dim.name}</p>
                <p className="text-xs text-text-secondary mt-1 leading-snug">{dim.desc}</p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
```

- [ ] **Step 4.8 — `components/landing/TrustBuildingSection.tsx`** (Server Component)

```typescript
import { CheckCircle2 } from 'lucide-react';

const points = [
  'Dựa trên Tử Vi Đẩu Số — hệ thống có phương pháp khoa học, không phải xem bói cảm tính',
  'Knowledge base được xây dựng từ chuyên gia 20+ năm kinh nghiệm thực chiến',
  'AI phân tích dữ liệu thực từ lá số của bạn — không bịa đặt, không generic',
  'Biểu đồ trực quan theo từng giai đoạn đời người, lời khuyên cụ thể có thể hành động ngay',
];

export default function TrustBuildingSection() {
  return (
    <section className="py-10 sm:py-16">
      <h2 className="text-[18px] sm:text-[22px] font-semibold text-text-primary text-center mb-10">
        Tại sao khác biệt?
      </h2>

      <div className="flex flex-col gap-4 max-w-[560px] mx-auto">
        {points.map((point, i) => (
          <div key={i} className="flex items-start gap-4">
            <CheckCircle2 size={20} className="text-alert-positive flex-shrink-0 mt-0.5" />
            <p className="text-sm text-text-primary leading-relaxed">{point}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
```

- [ ] **Step 4.9 — `components/landing/SamplePreviewSection.tsx`** (Server Component)

Use placeholder (image not yet available in MVP):

```typescript
import Link from 'next/link';

export default function SamplePreviewSection() {
  return (
    <section className="py-10 sm:py-16">
      <h2 className="text-[18px] sm:text-[22px] font-semibold text-text-primary text-center mb-2">
        Kết quả bạn sẽ nhận được
      </h2>
      <p className="text-sm text-text-secondary text-center mb-10">
        Luận giải chi tiết, biểu đồ trực quan cho từng giai đoạn cuộc đời
      </p>

      <div className="max-w-[600px] mx-auto border border-border rounded-[12px] overflow-hidden shadow-lg relative">
        {/* M1: Placeholder — replace with Next.js Image when screenshot is ready */}
        <div className="w-full aspect-[16/10] bg-bg-subtle flex items-center justify-center">
          <p className="text-xs text-text-tertiary">Ảnh mẫu đang được cập nhật...</p>
        </div>

        {/* Gradient overlay */}
        <div className="absolute bottom-0 left-0 right-0 h-[40%]
          bg-gradient-to-t from-bg-primary to-transparent pointer-events-none" />

        {/* CTA overlay */}
        <div className="absolute bottom-6 left-0 right-0 flex justify-center">
          <Link
            href="/form"
            className="bg-accent hover:bg-accent-hover text-white font-medium text-sm
              px-6 h-10 rounded-md flex items-center transition-colors duration-100"
          >
            Xem kết quả của bạn →
          </Link>
        </div>
      </div>
    </section>
  );
}
```

- [ ] **Step 4.10 — `components/landing/FAQSection.tsx`** (Client Component)

```typescript
'use client';
import {
  Accordion, AccordionContent, AccordionItem, AccordionTrigger,
} from '@/components/ui/accordion';

const faqs = [
  {
    q: 'Khác gì với xem bói trực tuyến thông thường?',
    a: 'Tử Vi Đẩu Số là hệ thống có phương pháp rõ ràng — lá số được tính toán từ dữ liệu cụ thể (ngày giờ sinh, giới tính) và cho cùng một kết quả với cùng dữ liệu đầu vào. AI của chúng tôi chỉ luận giải dựa trên điểm số thực từ lá số của bạn — không bịa đặt, không nói chung chung.',
  },
  {
    q: 'Kết quả có chính xác không?',
    a: 'Tử Vi Đẩu Số là hệ thống có tính logic cao, nhưng không có hệ thống nào dự đoán tương lai 100%. Kết quả phản ánh xu hướng vận khí — hãy dùng như một công cụ tham khảo để ra quyết định tốt hơn, không phải lời phán quyết tuyệt đối.',
  },
  {
    q: 'Thông tin của tôi có được bảo mật không?',
    a: 'Dữ liệu ngày giờ sinh được lưu dưới dạng mã hóa, chỉ dùng để tạo lá số. Chúng tôi không liên kết với danh tính thật của bạn và không bán dữ liệu cho bên thứ ba.',
  },
  {
    q: 'Tại sao cần biết giờ sinh chính xác?',
    a: 'Trong Tử Vi Đẩu Số, giờ sinh xác định Cung Mệnh — yếu tố quan trọng nhất của lá số. Sai giờ sinh có thể dẫn đến kết quả hoàn toàn khác. Nếu không biết chính xác, hãy hỏi cha mẹ hoặc xem sổ khai sinh.',
  },
  {
    q: 'Hoàn toàn miễn phí không?',
    a: 'Có, giai đoạn này hoàn toàn miễn phí. Chúng tôi đang trong giai đoạn thử nghiệm với nhóm người dùng nhỏ để thu thập phản hồi và cải thiện chất lượng luận giải.',
  },
];

export default function FAQSection() {
  return (
    <section className="py-10 sm:py-16 -mx-4 px-4 bg-bg-subtle">
      <div className="max-w-3xl mx-auto">
        <h2 className="text-[18px] sm:text-[22px] font-semibold text-text-primary text-center mb-10">
          Câu hỏi thường gặp
        </h2>

        <div className="max-w-[600px] mx-auto">
          <Accordion type="single" collapsible>
            {faqs.map((faq, i) => (
              <AccordionItem key={i} value={`faq-${i}`} className="border-b border-border last:border-0">
                <AccordionTrigger className="text-sm font-medium text-text-primary py-4 hover:no-underline text-left">
                  {faq.q}
                </AccordionTrigger>
                <AccordionContent className="text-sm text-text-secondary pb-4 leading-relaxed">
                  {faq.a}
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </div>
      </div>
    </section>
  );
}
```

- [ ] **Step 4.11 — `components/landing/FinalCTASection.tsx`** (Server Component)

```typescript
import Link from 'next/link';

export default function FinalCTASection() {
  return (
    <section className="py-14 sm:py-20 text-center">
      <h2 className="text-[18px] sm:text-[22px] font-semibold text-text-primary">
        Bắt đầu ngay. Miễn phí. Không cần đăng ký.
      </h2>
      <p className="text-sm text-text-secondary mt-3">
        Nhận luận giải tử vi cá nhân hóa trong 30 giây.
      </p>
      <Link
        href="/form"
        className="inline-flex items-center bg-accent hover:bg-accent-hover text-white
          font-medium text-base px-10 h-[52px] rounded-md mt-8
          transition-colors duration-100"
      >
        Xem luận giải của bạn →
      </Link>
    </section>
  );
}
```

- [ ] **Step 4.12 — `components/landing/LandingFooter.tsx`** (Server Component)

```typescript
export default function LandingFooter() {
  return (
    <footer className="border-t border-border py-8">
      <div className="max-w-3xl mx-auto px-4 flex flex-col sm:flex-row items-start sm:items-center
        justify-between gap-3">
        <span className="text-xs text-text-tertiary">© 2026 TuVi AI</span>
        <p className="text-[11px] text-text-tertiary max-w-[400px] leading-relaxed">
          Nội dung mang tính tham khảo, không phải lời khuyên chuyên nghiệp.
          Mọi quyết định cuối cùng là của bạn.
        </p>
      </div>
    </footer>
  );
}
```

- [ ] **Step 4.13 — Verify**
```bash
cd frontend && npx tsc --noEmit
```
Then run `npm run dev` and visually check all 9 landing page sections render correctly on both mobile (375px) and desktop (768px+).

- [ ] **Step 4.14 — Commit**
```bash
git add frontend/app/layout.tsx frontend/app/page.tsx frontend/components/landing/
git commit -m "feat: add landing page with all 9 sections"
```

---

## Task 5: Input Form

**Files:** `frontend/app/form/page.tsx`, `frontend/components/form/BirthInputForm.tsx`, `frontend/components/form/DatePickerField.tsx`, `frontend/lib/validateDate.test.ts`

- [ ] **Step 5.1 — Form page route (`app/form/page.tsx`)** (Server Component)

```typescript
import type { Metadata } from 'next';
import Link from 'next/link';
import { ChevronLeft } from 'lucide-react';
import BirthInputForm from '@/components/form/BirthInputForm';

export const metadata: Metadata = {
  title: 'Nhập thông tin — TuVi AI',
  description: 'Nhập ngày giờ sinh để nhận luận giải tử vi cá nhân hóa.',
};

export default function FormPage() {
  return (
    <div className="min-h-screen bg-bg-primary">
      {/* Fixed header */}
      <header className="fixed top-0 left-0 right-0 h-14 z-10
        bg-bg-surface border-b border-border flex items-center px-4">
        <Link
          href="/"
          className="flex items-center gap-1 text-sm text-text-secondary hover:text-text-primary
            transition-colors duration-100 px-2 py-1.5 rounded-md hover:bg-bg-subtle"
        >
          <ChevronLeft size={16} />
          Trang chủ
        </Link>
        <span className="absolute left-1/2 -translate-x-1/2 font-semibold text-sm text-text-primary">
          TuVi AI
        </span>
      </header>

      {/* Form content */}
      <div className="flex flex-col items-center justify-center px-4 py-12 pt-[80px]">
        <div className="max-w-[480px] w-full bg-bg-surface border border-border
          rounded-[12px] shadow-md p-4 sm:p-6">
          <BirthInputForm />
        </div>
      </div>
    </div>
  );
}
```

- [ ] **Step 5.2 — `components/form/DatePickerField.tsx`** (Client Component)

```typescript
'use client';
import { useState } from 'react';
import { format } from 'date-fns';
import { vi } from 'date-fns/locale';
import { Calendar as CalendarIcon, ChevronDown, AlertCircle } from 'lucide-react';
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';
import { Calendar } from '@/components/ui/calendar';

interface DatePickerFieldProps {
  value: Date | undefined;
  onChange: (date: Date | undefined) => void;
  error?: string;
}

export default function DatePickerField({ value, onChange, error }: DatePickerFieldProps) {
  const [open, setOpen] = useState(false);
  const currentYear = new Date().getFullYear();

  return (
    <div className="flex flex-col gap-1.5">
      <label className="text-[13px] font-medium text-text-primary">
        Ngày sinh <span className="text-accent">*</span>
      </label>

      <Popover open={open} onOpenChange={setOpen}>
        <PopoverTrigger asChild>
          <button
            type="button"
            data-error={error ? 'true' : undefined}
            className={`w-full h-12 flex items-center gap-2 px-3 text-sm text-left
              border rounded-[6px] bg-bg-surface transition-colors duration-100
              focus:outline-none focus:ring-1 focus:ring-border-focus focus:border-border-focus
              ${error
                ? 'border-red-400 focus:border-red-500 focus:ring-red-400'
                : 'border-border hover:border-gray-300'
              }`}
          >
            <CalendarIcon size={16} className="text-text-tertiary flex-shrink-0" />
            <span className={`flex-1 ${value ? 'text-text-primary' : 'text-text-tertiary'}`}>
              {value ? format(value, 'dd/MM/yyyy') : 'Chọn ngày sinh'}
            </span>
            <ChevronDown size={16} className="text-text-tertiary flex-shrink-0" />
          </button>
        </PopoverTrigger>
        <PopoverContent className="w-auto p-0" align="start">
          <Calendar
            mode="single"
            selected={value}
            onSelect={(date) => {
              onChange(date);
              setOpen(false);
            }}
            fromYear={1920}
            toYear={currentYear}
            captionLayout="dropdown-buttons"
            showOutsideDays={false}
            locale={vi}
            className="rounded-[8px]"
          />
        </PopoverContent>
      </Popover>

      {error && (
        <p className="flex items-center gap-1 text-xs text-red-500 mt-0.5">
          <AlertCircle size={14} />
          {error}
        </p>
      )}
    </div>
  );
}
```

- [ ] **Step 5.3 — `components/form/BirthInputForm.tsx`** (Client Component)

```typescript
'use client';
import { useState, useMemo } from 'react';
import { useRouter } from 'next/navigation';
import { format } from 'date-fns';
import { Info, Loader2, Lock, AlertCircle } from 'lucide-react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';
import DatePickerField from './DatePickerField';
import { BIRTH_HOURS } from '@/lib/constants';
import { generateProfile } from '@/lib/api';

interface FormState {
  name: string;
  birthDate: Date | undefined;
  birthHour: string;
  gender: 'male' | 'female' | '';
}

interface FormErrors {
  birthDate?: string;
  birthHour?: string;
  gender?: string;
  submit?: string;
}

function validateDate(date: Date | undefined): string | undefined {
  const currentYear = new Date().getFullYear();
  if (!date) return 'Vui lòng chọn ngày sinh.';
  const year = date.getFullYear();
  if (year < 1920 || year > currentYear) {
    return `Ngày sinh phải từ năm 1920 đến ${currentYear}.`;
  }
  return undefined;
}

export default function BirthInputForm() {
  const router = useRouter();
  const [formState, setFormState] = useState<FormState>({
    name: '', birthDate: undefined, birthHour: '', gender: '',
  });
  const [errors, setErrors] = useState<FormErrors>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const isFormValid = useMemo(
    () => !!formState.birthDate && !validateDate(formState.birthDate)
      && !!formState.birthHour && !!formState.gender,
    [formState.birthDate, formState.birthHour, formState.gender],
  );

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    const newErrors: FormErrors = {
      birthDate: validateDate(formState.birthDate),
      birthHour: !formState.birthHour ? 'Vui lòng chọn giờ sinh.' : undefined,
      gender: !formState.gender ? 'Vui lòng chọn giới tính.' : undefined,
    };

    if (Object.values(newErrors).some(Boolean)) {
      setErrors(newErrors);
      // I9: Focus first invalid field
      setTimeout(() => {
        const firstErrorEl = document.querySelector<HTMLElement>('[data-error="true"]');
        firstErrorEl?.focus();
      }, 0);
      return;
    }

    setIsSubmitting(true);
    setErrors({});

    try {
      const birthInputData = {
        name: formState.name || undefined,
        birthDate: format(formState.birthDate!, 'yyyy-MM-dd'),
        birthHour: formState.birthHour,
        gender: formState.gender as 'male' | 'female',
        namXem: new Date().getFullYear(),
      };
      const result = await generateProfile(birthInputData);
      // M4: Store input for retry on processing error
      sessionStorage.setItem('tuvi_last_input', JSON.stringify(birthInputData));
      router.push(`/processing/${result.profileId}`);
    } catch (err) {
      setErrors({ submit: err instanceof Error ? err.message : 'Có lỗi xảy ra. Vui lòng thử lại.' });
      setIsSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} noValidate>
      {/* Form header */}
      <div className="mb-6">
        <h1 className="text-[18px] font-semibold text-text-primary">
          Nhập thông tin ngày sinh
        </h1>
        <p className="text-xs text-text-tertiary mt-1">
          Tất cả thông tin được mã hóa và bảo mật
        </p>
      </div>

      <div className="flex flex-col gap-5">
        {/* Name field — optional */}
        <div className="flex flex-col gap-1.5">
          <label htmlFor="name" className="text-[13px] font-medium text-text-primary flex items-center">
            Họ tên
            <span className="text-[11px] text-text-tertiary bg-bg-subtle px-1.5 py-0.5 rounded ml-2">
              Không bắt buộc
            </span>
          </label>
          <input
            id="name"
            type="text"
            placeholder="Nguyễn Văn A"
            maxLength={100}
            value={formState.name}
            onChange={(e) => setFormState((s) => ({ ...s, name: e.target.value }))}
            className="w-full h-12 border border-border rounded-[6px] px-3 text-sm
              text-text-primary bg-bg-surface placeholder:text-text-tertiary
              focus:outline-none focus:border-border-focus focus:ring-1 focus:ring-border-focus"
          />
          <p className="text-xs text-text-tertiary">
            Dùng trong luận giải để cá nhân hóa nội dung.
          </p>
        </div>

        {/* Date field */}
        <DatePickerField
          value={formState.birthDate}
          onChange={(date) => setFormState((s) => ({ ...s, birthDate: date }))}
          error={errors.birthDate}
        />

        {/* Hour field */}
        <div className="flex flex-col gap-1.5">
          <label className="text-[13px] font-medium text-text-primary flex items-center">
            Giờ sinh <span className="text-accent ml-0.5">*</span>
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <button type="button" className="ml-1.5 cursor-help" aria-label="Tại sao cần giờ sinh?">
                    <Info size={15} className="text-text-tertiary" />
                  </button>
                </TooltipTrigger>
                <TooltipContent className="max-w-[280px] text-xs p-3 rounded-[8px]">
                  Giờ sinh xác định Cung Mệnh — yếu tố quan trọng nhất trong Tử Vi Đẩu Số.
                  Nếu không biết chính xác, hãy hỏi cha mẹ hoặc xem sổ khai sinh.
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
          </label>

          <Select
            value={formState.birthHour}
            onValueChange={(v) => setFormState((s) => ({ ...s, birthHour: v }))}
          >
            <SelectTrigger
              data-error={errors.birthHour ? 'true' : undefined}
              className={`w-full h-12 text-sm rounded-[6px]
                ${errors.birthHour ? 'border-red-400' : 'border-border'}`}
            >
              <SelectValue placeholder="Chọn giờ sinh" />
            </SelectTrigger>
            <SelectContent>
              {BIRTH_HOURS.map((h) => (
                <SelectItem key={h.value} value={h.value} className="py-2.5 text-sm">
                  {h.label} ({h.range})
                </SelectItem>
              ))}
            </SelectContent>
          </Select>

          {errors.birthHour && (
            <p className="flex items-center gap-1 text-xs text-red-500 mt-0.5">
              <AlertCircle size={14} />
              {errors.birthHour}
            </p>
          )}
        </div>

        {/* Gender field */}
        <div className="flex flex-col gap-1.5">
          <label className="text-[13px] font-medium text-text-primary">
            Giới tính <span className="text-accent">*</span>
          </label>

          <RadioGroup
            value={formState.gender}
            onValueChange={(v) => setFormState((s) => ({ ...s, gender: v as 'male' | 'female' }))}
            className="flex gap-4 mt-1"
          >
            {[
              { value: 'male', label: 'Nam' },
              { value: 'female', label: 'Nữ' },
            ].map((opt) => (
              <label
                key={opt.value}
                className="flex items-center gap-2 cursor-pointer"
                data-error={errors.gender && !formState.gender ? 'true' : undefined}
              >
                <RadioGroupItem value={opt.value} id={`gender-${opt.value}`} className="w-5 h-5" />
                <span className="text-sm text-text-primary">{opt.label}</span>
              </label>
            ))}
          </RadioGroup>

          {errors.gender && (
            <p className="flex items-center gap-1 text-xs text-red-500 mt-0.5">
              <AlertCircle size={14} />
              {errors.gender}
            </p>
          )}
        </div>

        {/* Submit error */}
        {errors.submit && (
          <p className="flex items-center gap-1 text-xs text-red-500">
            <AlertCircle size={14} />
            {errors.submit}
          </p>
        )}

        {/* Submit button */}
        <button
          type="submit"
          disabled={!isFormValid || isSubmitting}
          className={`w-full h-12 rounded-[8px] text-white font-medium text-sm mt-3
            flex items-center justify-center gap-2 transition-colors duration-100
            ${!isFormValid || isSubmitting
              ? 'bg-accent opacity-40 cursor-not-allowed'
              : 'bg-accent hover:bg-accent-hover cursor-pointer'
            }`}
        >
          {isSubmitting ? (
            <>
              <Loader2 size={16} className="animate-spin" />
              Đang xử lý...
            </>
          ) : (
            'Xem luận giải →'
          )}
        </button>

        {/* Privacy note */}
        <p className="flex items-center justify-center gap-1 text-[11px] text-text-tertiary mt-1">
          <Lock size={12} />
          Thông tin ngày sinh không được lưu trữ gắn với danh tính của bạn.
        </p>
      </div>
    </form>
  );
}
```

- [ ] **Step 5.4 — Create `lib/validateDate.test.ts`**

```typescript
import { describe, it, expect } from 'vitest';

function validateDate(date: Date | undefined): string | undefined {
  const currentYear = new Date().getFullYear();
  if (!date) return 'Vui lòng chọn ngày sinh.';
  const year = date.getFullYear();
  if (year < 1920 || year > currentYear) {
    return `Ngày sinh phải từ năm 1920 đến ${currentYear}.`;
  }
  return undefined;
}

describe('validateDate', () => {
  const currentYear = new Date().getFullYear();

  it('returns error when date is undefined', () => {
    expect(validateDate(undefined)).toBe('Vui lòng chọn ngày sinh.');
  });

  it('returns error for year before 1920', () => {
    const result = validateDate(new Date(1919, 0, 1));
    expect(result).toContain('1920');
  });

  it('returns error for year after currentYear', () => {
    const result = validateDate(new Date(currentYear + 1, 0, 1));
    expect(result).toContain(String(currentYear));
  });

  it('returns undefined for valid year 1994', () => {
    expect(validateDate(new Date(1994, 6, 19))).toBeUndefined();
  });

  it('returns undefined for year 1920 (boundary)', () => {
    expect(validateDate(new Date(1920, 0, 1))).toBeUndefined();
  });

  it('returns undefined for currentYear (boundary)', () => {
    expect(validateDate(new Date(currentYear, 0, 1))).toBeUndefined();
  });
});
```

- [ ] **Step 5.5 — Verify**
```bash
cd frontend && npx tsc --noEmit && npm test
```

Expected: all tests pass (12+ total). Then run `npm run dev` and visually check:
- All 4 fields render correctly
- Submit button disabled until birthDate + birthHour + gender are all filled
- Validation errors appear on submit with missing fields
- First error field receives focus (I9)
- Loading state shows spinner during submit

- [ ] **Step 5.6 — Commit**
```bash
git add frontend/app/form/ frontend/components/form/ frontend/lib/validateDate.test.ts
git commit -m "feat: add input form with validation and submit flow"
```
