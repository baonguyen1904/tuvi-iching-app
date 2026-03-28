# Frontend Spec — Part 1: Design System + Types

> Part of the frontend design spec. Index: ../2026-03-27-frontend-design-spec.md

---

# Frontend Design Spec — TuVi AI
## Comprehensive UI/UX Specification for Developer Handoff

**Date:** 2026-03-27
**Stack:** Next.js 15+ (App Router, TypeScript), Tailwind CSS, shadcn/ui, Recharts
**Deploy:** Vercel
**Language:** Vietnamese only
**Breakpoints:** Mobile-first. `sm` = 640px, `md` = 768px (max content width)

---

## DESIGN DECISIONS — Overrides from Task 04

The following decisions in this spec explicitly override recommendations or descriptions in `tasks/04_frontend.md`. Do NOT revert to Task 04 behavior without updating this section.

| Decision | This Spec | Task 04 | Rationale |
|----------|-----------|---------|-----------|
| **Dimension detail routing** | Separate routes `/result/[id]/[dimension]` | Option A: accordion on overview page | Enables direct linking, cleaner URL structure, better mobile reading |
| **Dimensions in overview chart** | 8 dimensions including `van_menh` | "7 axes" | `van_menh` is a full dimension with chart data; CLAUDE.md Rule 4 lists 8 dimensions |
| **Charts per dimension** | 3 charts (Lifetime + Decade + Monthly) | "2 charts per dimension" | Monthly data from tuvi.vn scraper is a core feature per CLAUDE.md Rule 5 |
| **Date range** | 1920 to `currentYear` (dynamic) | hardcoded 1920–2010 | Prevents the UI from becoming stale; users born after 2010 may eventually use the app |

---

## PART 1: DESIGN SYSTEM

### 1.1 Color Tokens

Define all tokens in `frontend/lib/tokens.ts` AND as Tailwind CSS variables in `tailwind.config.ts`.

```typescript
// frontend/lib/tokens.ts
export const colors = {
  // Backgrounds
  bgPrimary:    '#FAFAFA',   // Page background
  bgSurface:    '#FFFFFF',   // Cards, panels, inputs
  bgSubtle:     '#F3F4F6',   // Hover states, secondary surfaces, step indicators

  // Text
  textPrimary:   '#111827',  // Headings, critical text — gray-900
  textSecondary: '#6B7280',  // Body text, descriptions — gray-500
  textTertiary:  '#9CA3AF',  // Placeholders, metadata, captions — gray-400

  // Accent (blue)
  accent:        '#2563EB',  // Primary CTA, links, focus rings — blue-600
  accentHover:   '#1D4ED8',  // CTA hover state — blue-700
  accentLight:   '#EFF6FF',  // Accent background — blue-50
  accentBorder:  '#BFDBFE',  // Accent border — blue-200

  // Alerts
  alertPositive:    '#10B981', // ▲ positive alert text/icon — emerald-500
  alertPositiveBg:  '#ECFDF5', // ▲ positive alert background — emerald-50
  alertPositiveBdr: '#A7F3D0', // ▲ positive alert border — emerald-200
  alertNegative:    '#F59E0B', // ▼ negative alert text/icon — amber-500 (NOT red)
  alertNegativeBg:  '#FFFBEB', // ▼ negative alert background — amber-50
  alertNegativeBdr: '#FDE68A', // ▼ negative alert border — amber-200

  // Chart lines
  chartDuong: '#2563EB',   // Dương line — blue-600
  chartAm:    '#F59E0B',   // Âm line — amber-500
  chartTb:    '#9CA3AF',   // TB line — gray-400

  // Borders
  border:      '#E5E7EB',  // Default border — gray-200
  borderFocus: '#2563EB',  // Focus ring — blue-600
} as const;
```

**Tailwind config extension** (`tailwind.config.ts`):

```typescript
theme: {
  extend: {
    colors: {
      bg: {
        primary: '#FAFAFA',
        surface: '#FFFFFF',
        subtle:  '#F3F4F6',
      },
      text: {
        primary:   '#111827',
        secondary: '#6B7280',
        tertiary:  '#9CA3AF',
      },
      accent: {
        DEFAULT: '#2563EB',
        hover:   '#1D4ED8',
        light:   '#EFF6FF',
        border:  '#BFDBFE',
      },
      alert: {
        'positive':     '#10B981',
        'positive-bg':  '#ECFDF5',
        'positive-bdr': '#A7F3D0',
        'negative':     '#F59E0B',
        'negative-bg':  '#FFFBEB',
        'negative-bdr': '#FDE68A',
      },
      chart: {
        duong: '#2563EB',
        am:    '#F59E0B',
        tb:    '#9CA3AF',
      },
      border: {
        DEFAULT: '#E5E7EB',
        focus:   '#2563EB',
      },
    },
  },
}
```

---

### 1.2 Typography

**Font:** Inter (Google Fonts). Load via `next/font/google` in root `layout.tsx`.

```typescript
// frontend/app/layout.tsx
import { Inter } from 'next/font/google';
const inter = Inter({
  subsets: ['latin', 'vietnamese'],
  variable: '--font-inter',
  display: 'swap',
});
```

**Type Scale** (define as Tailwind utilities or CSS variables):

| Token | Size | Weight | Line Height | Usage |
|-------|------|--------|-------------|-------|
| `heading-xl` | 36px / 2.25rem | 700 | 1.2 | Hero headline (h1) |
| `heading-lg` | 28px / 1.75rem | 700 | 1.2 | Page titles (h2) |
| `heading-md` | 22px / 1.375rem | 600 | 1.3 | Section headings (h3) |
| `heading-sm` | 18px / 1.125rem | 600 | 1.3 | Card titles, labels (h4) |
| `body-lg`    | 16px / 1rem     | 400 | 1.6 | Lead paragraph, subheadline |
| `body`       | 14px / 0.875rem | 400 | 1.6 | Default body text |
| `body-sm`    | 13px / 0.8125rem| 400 | 1.5 | Captions, metadata |
| `caption`    | 12px / 0.75rem  | 400 | 1.4 | Disclaimers, fine print |
| `label`      | 13px / 0.8125rem| 500 | 1.4 | Form labels, button text |
| `mono`       | 13px / 0.8125rem| 400 | 1.5 | Scores, numbers (tabular) |

**Mobile adjustments** (below 640px):
- `heading-xl` → 28px
- `heading-lg` → 22px
- `heading-md` → 18px

---

### 1.3 Spacing System

Base unit: **8px**. All spacing values are multiples.

| Token | Value | Tailwind class | Usage |
|-------|-------|----------------|-------|
| `space-1` | 8px | `p-2` / `m-2` | Micro gap, icon padding |
| `space-2` | 16px | `p-4` / `m-4` | Card padding mobile, inline spacing |
| `space-3` | 24px | `p-6` / `m-6` | Card padding desktop, section sub-spacing |
| `space-4` | 32px | `p-8` / `m-8` | Component separation |
| `space-5` | 40px | `p-10` / `m-10` | Section spacing mobile |
| `space-6` | 48px | `p-12` / `m-12` | Large gaps |
| `space-8` | 64px | `p-16` / `m-16` | Section spacing desktop |

**Card padding:** `p-4` (16px) mobile → `p-6` (24px) desktop
**Section spacing:** `py-10` (40px) mobile → `py-16` (64px) desktop
**Max content width:** `max-w-3xl` = 768px, centered with `mx-auto px-4`

---

### 1.4 Border Radius & Shadows

```css
/* Radius tokens */
--radius-sm: 6px;    /* Inputs, badges, tags */
--radius-md: 8px;    /* Buttons, small cards */
--radius-lg: 12px;   /* Cards, panels */
--radius-xl: 16px;   /* Modal, large panels */
--radius-full: 9999px; /* Pills, avatars */

/* Shadow tokens */
--shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
--shadow-md: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.04);
--shadow-lg: 0 4px 12px rgba(0,0,0,0.08);
```

Use `shadow-md` for cards, `shadow-sm` for buttons, no shadow for inline elements.

---

### 1.5 Component Design Tokens

**Buttons:**

```
Primary:   bg-accent text-white rounded-md px-5 py-2.5 font-medium text-sm
           hover: bg-accent-hover  focus: ring-2 ring-accent ring-offset-2
           height: 40px desktop, 48px mobile (larger touch target)

Secondary: bg-transparent border border-border text-text-primary rounded-md px-5 py-2.5
           hover: bg-bg-subtle

Ghost:     bg-transparent text-accent px-3 py-2 rounded-md
           hover: bg-accent-light

Disabled:  opacity-40 cursor-not-allowed (all variants)

Loading:   Primary + spinner (24px Lucide Loader2, animate-spin) + text "Đang xử lý..."
```

**Inputs:**

```
Default:   border border-border rounded-[6px] px-3 py-3 text-sm text-text-primary
           bg-bg-surface w-full
           height: 48px (large touch target)
           placeholder: text-text-tertiary
           focus: outline-none border-border-focus ring-1 ring-border-focus

Error:     border-red-400 focus:border-red-500 focus:ring-red-400

Label:     text-label text-text-primary mb-1.5 block
Error msg: text-body-sm text-red-500 mt-1.5
```

**Cards:**

```
Default: bg-bg-surface rounded-[12px] border border-border shadow-md p-6 (desktop) / p-4 (mobile)
Hover (clickable): hover:border-accent-border hover:shadow-lg transition-all duration-150
Active: bg-bg-subtle
```

---

### 1.6 Icon System

Use **Lucide React** exclusively. Import individually for tree-shaking.

```typescript
import { Briefcase, TrendingUp, Heart, Activity, Home, BookOpen, Baby, Compass } from 'lucide-react';
```

**Dimension icon map** (`frontend/lib/constants.ts`):

```typescript
export const DIMENSION_ICONS = {
  su_nghiep: 'Briefcase',
  tien_bac:  'TrendingUp',
  hon_nhan:  'Heart',
  suc_khoe:  'Activity',
  dat_dai:   'Home',
  hoc_tap:   'BookOpen',
  con_cai:   'Baby',
  van_menh:  'Compass',
} as const;

export const DIMENSION_LABELS = {
  su_nghiep: 'Sự nghiệp',
  tien_bac:  'Tiền bạc',
  hon_nhan:  'Hôn nhân',
  suc_khoe:  'Sức khỏe',
  dat_dai:   'Đất đai',
  hoc_tap:   'Học tập',
  con_cai:   'Con cái',
  van_menh:  'Vận mệnh',
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
```

---

### 1.7 shadcn/ui Component Mapping

Install: `npx shadcn@latest init` then add individual components.

| UI Need | shadcn Component | Notes |
|---------|-----------------|-------|
| Date picker | `Calendar` + `Popover` | Wrap with custom trigger input |
| Dropdown select | `Select` | Giờ sinh dropdown |
| Radio group | `RadioGroup` + `RadioGroupItem` | Giới tính |
| Accordion | `Accordion` + `AccordionItem` | FAQ section |
| Toast | `Sonner` (via `sonner` package) | Share link copied, feedback |
| Tooltip | `Tooltip` + `TooltipTrigger` | Giờ sinh info |
| Dialog/Modal | Not needed MVP | — |
| Badge | Custom (not shadcn) | Alert badges |
| Progress | Custom (not shadcn) | Processing steps |

**Do NOT use shadcn Button, Card, Input** — implement custom to match exact design tokens.
Use shadcn only for complex interactive primitives (Calendar, Select, Accordion, Tooltip).

---

## PART 2: TYPE DEFINITIONS

```typescript
// frontend/lib/types.ts

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
  //   monthly  → strings:       ["Th.1/2026", "Th.1/2026", "Th.2/2026", ..., "Th.12/2026"]
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

---
