# Frontend Spec — Part 4: Dimension Detail + Charts

> Part of the frontend design spec. Index: ../2026-03-27-frontend-design-spec.md

---

## PART 7: PAGE 5 — DIMENSION DETAIL (`/result/[id]/[dimension]`)

### 7.1 Component Tree

```
app/result/[id]/[dimension]/page.tsx (Server Component)
└── DimensionDetailLayout
    ├── DetailHeader (back link + share)
    ├── DimensionTitleBlock (icon + name + summary badge)
    ├── ChartsSection
    │   ├── ChartCard (Lifetime chart)
    │   │   ├── ChartHeader
    │   │   └── LifetimeChart (Client — Recharts)
    │   ├── ChartCard (Decade chart)
    │   │   └── DecadeChart (Client — Recharts)
    │   └── ChartCard (Monthly chart)
    │       └── MonthlyChart (Client — Recharts)
    ├── AlertsSummarySection (hidden for van_menh)
    ├── AIInterpretationSection
    ├── DimensionNavigation (prev/next)
    └── ResultFooter
```

### 7.2 Data Fetching

```typescript
// app/result/[id]/[dimension]/page.tsx
export default async function DimensionDetailPage({
  params,
}: {
  params: { id: string; dimension: string };
}) {
  // Validate dimension key
  if (!DIMENSION_ORDER.includes(params.dimension as DimensionKey)) {
    notFound();
  }

  const profile = await getProfile(params.id);
  const dimensionData = profile.dimensions[params.dimension];

  // B9: Defensive guard — if dimension data is missing (e.g. partial API response),
  // show not-found rather than crashing. This also protects van_menh if it ever
  // lacks data due to a backend issue.
  if (!dimensionData) notFound();

  return (
    <DimensionDetailLayout
      profile={profile}
      dimensionKey={params.dimension as DimensionKey}
      dimensionData={dimensionData}
    />
  );
}
```

### 7.3 DetailHeader

```
Position: sticky top-0, z-40
Height: 56px, bg-bg-surface border-b border-border
Max-w-3xl mx-auto px-4 flex items-center justify-between

Left:
  Link → href={`/result/${profileId}`}
  flex items-center gap-1.5 text-body text-text-secondary hover:text-text-primary
  ChevronLeft icon (16px) + "Tổng quan"

Right: ShareButton (same as result page)
```

### 7.4 DimensionTitleBlock

```
mt-[56px] px-4 pt-6 pb-4
max-w-3xl mx-auto

Layout: flex items-center gap-3

[Icon block]
  w-12 h-12 rounded-[12px] bg-accent-light flex items-center justify-center
  Icon: 24px Lucide, color accent

[Text block]
  Dimension label: text-heading-md font-bold text-text-primary
  Sub: "{profile.name ? profile.name + ' — ' : ''}{DIMENSION_LABELS[dimensionKey]}"
  Score badge (inline):
    text-body-sm text-text-secondary mt-0.5
    "Tổng điểm: " + score value styled text-mono font-medium text-text-primary
```

### 7.5 ChartCard Component

**File:** `frontend/components/charts/ChartCard.tsx`

```typescript
interface ChartCardProps {
  title: string;
  subtitle?: string;
  children: React.ReactNode;   // Chart component
}
```

```
Container: bg-bg-surface border border-border rounded-[12px] p-4 / p-6 mt-4

Header:
  Title: text-label font-semibold text-text-primary
  Subtitle: text-body-sm text-text-tertiary mt-0.5 (e.g., "12 mốc • Cả cuộc đời")

Chart area: mt-4, overflow-hidden

Legend row (below chart):
  flex gap-4 mt-3 justify-center
  3 items: Dương (blue), Âm (amber), TB (gray)
  Each: flex items-center gap-1.5 text-caption text-text-secondary
  Line indicator: w-8 h-0.5 (not dots — matches chart line style)
    bg-chart-duong / bg-chart-am / bg-chart-tb
```

### 7.6 AlertsSummarySection

```
Hidden entirely for van_menh (check: dimensionKey === 'van_menh').

Title: "Các mốc cần chú ý"
  text-label font-semibold text-text-primary mt-6 mb-3

If no alerts:
  text-body-sm text-text-tertiary "Không có mốc đặc biệt trong giai đoạn này."

Each alert card (map over dimension.alerts, sorted by: positives first, then negatives):
  bg-alert-positive-bg / bg-alert-negative-bg
  border border-alert-positive-bdr / border-alert-negative-bdr
  rounded-[8px] p-3 mb-2

  Layout: flex items-start gap-2.5

  [Icon] TrendingUp (positive) / TrendingDown (negative)
    16px, color alert-positive / alert-negative, mt-0.5 flex-shrink-0

  [Content]
    Period: text-label font-medium text-text-primary "{alert.period}"
    Tag: text-body-sm text-text-secondary mt-0.5 "{alert.tag}"
    Level badge: text-caption rounded-full px-1.5 py-0.5 ml-2 (inline after period)
      Level 50: "Mức cao" bg-amber-100 text-amber-800 border border-amber-300 font-semibold
        — I5: Use amber-100/amber-800 (NOT red). Red implies danger/error; amber is visually
          distinct from level-30 (amber-50/amber-600) while staying in the cautionary palette.
      Level 30: "Đáng chú ý" bg-amber-50 text-amber-700 border border-amber-200
```

### 7.7 AIInterpretationSection

**Component type: Server Component** — react-markdown v9 is pure ESM and works in Server Components
without any `'use client'` directive. rehype-raw also runs server-side. No client bundle overhead.
Do NOT add `'use client'` to `AIInterpretationSection.tsx` unless adding interactivity later.

```
mt-6

Header: flex items-center gap-2 mb-4
  Sparkles icon (Lucide, 18px, color accent)
  "AI Luận Giải" text-label font-semibold text-text-primary
  separator line: flex-1 h-px bg-border ml-2

Content container: prose-like styling (NOT using Tailwind typography plugin — custom)

Rendered markdown (interpretation field) — use react-markdown:
  npm install react-markdown

  Custom component overrides:
    h2: text-heading-sm font-semibold text-text-primary mt-6 mb-2
    h3: text-label font-semibold text-text-primary mt-4 mb-1.5
    p: text-body text-text-secondary leading-relaxed mb-3
    ul: list-disc pl-5 text-body text-text-secondary space-y-1
    li: leading-relaxed
    strong: font-semibold text-text-primary
    em: italic text-text-secondary
    hr: border-border my-6
    blockquote: border-l-2 border-accent pl-4 text-text-secondary italic

  Alert emoji handling (I7): Pre-process the interpretation text BEFORE passing to react-markdown.
    Use a `preprocessInterpretation` function that injects raw HTML `<span>` tags, then render
    with `rehype-raw` so react-markdown passes those tags through to the DOM.
    rehype-raw is a required dependency (see §13.6).

    ```typescript
    // frontend/lib/utils.ts (or inline in AIInterpretationSection)
    /**
     * I7: Wraps ▲ and ▼ characters in colored <span> tags so react-markdown renders them styled.
     * Must run BEFORE passing text to <ReactMarkdown>.
     * Requires rehype-raw to be passed as a rehype plugin so the raw HTML spans are rendered.
     */
    export function preprocessInterpretation(text: string): string {
      return text
        .replace(/▲/g, '<span class="text-emerald-600 font-medium">▲</span>')
        .replace(/▼/g, '<span class="text-amber-600 font-medium">▼</span>');
    }

    // Usage — rehype-raw is required to render the injected HTML spans:
    // import rehypeRaw from 'rehype-raw';
    // <ReactMarkdown rehypePlugins={[rehypeRaw]}>{preprocessInterpretation(text)}</ReactMarkdown>
    ```

For van_menh — interpretation is null:
  Show placeholder card:
  bg-bg-subtle border border-border rounded-[12px] p-6 text-center
  Clock icon (Lucide, 24px, text-text-tertiary) mb-3
  "Luận giải Vận mệnh đang được cập nhật."
  text-body text-text-secondary
  "Vận mệnh là bức tranh tổng thể — xem từng lĩnh vực để hiểu chi tiết."
  text-body-sm text-text-tertiary mt-1
```

### 7.8 DimensionNavigation

```
Placement: mt-10 border-t border-border pt-6 pb-4

Layout: flex justify-between items-center gap-4 max-w-3xl mx-auto px-4

Left (prev dimension):
  If not first dimension:
    Link → href={`/result/${profileId}/${prevKey}`}
    flex items-center gap-2 text-body text-text-secondary hover:text-text-primary
    ChevronLeft icon (16px)
    [right of icon]:
      text-caption text-text-tertiary "Trước"
      text-body-sm font-medium text-text-primary prevLabel

Right (next dimension):
  If not last dimension:
    Link → href={`/result/${profileId}/${nextKey}`}
    flex items-center gap-2 text-body text-text-secondary hover:text-text-primary text-right
    [left of icon]:
      text-caption text-text-tertiary "Tiếp theo"
      text-body-sm font-medium text-text-primary nextLabel
    ChevronRight icon (16px)

Navigation order: su_nghiep → tien_bac → hon_nhan → suc_khoe → dat_dai → hoc_tap → con_cai → van_menh
su_nghiep: no prev, has next
van_menh: has prev, no next
```

---

## PART 8: CHART SPECIFICATIONS (Recharts)

### 8.1 Shared Chart Config

```typescript
// frontend/components/charts/chartConfig.ts

export const CHART_COLORS = {
  duong: '#2563EB',
  am:    '#F59E0B',
  tb:    '#9CA3AF',
} as const;

export const CHART_DEFAULTS = {
  margin: { top: 16, right: 8, bottom: 8, left: -16 },
  animationDuration: 600,
  animationEasing: 'ease-out' as const,
  strokeWidth: 2,
  dotRadius: 0,     // no dots by default — only show on hover and alerts
  activeDotRadius: 4,
} as const;

// Tooltip style
export const tooltipStyle = {
  backgroundColor: '#FFFFFF',
  border: '1px solid #E5E7EB',
  borderRadius: '8px',
  fontSize: '13px',
  boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
  padding: '8px 12px',
};

export const axisStyle = {
  tick: { fill: '#9CA3AF', fontSize: 11 },
  line: { stroke: '#E5E7EB' },
};
```

---

### 8.2 LifetimeChart Component

**File:** `frontend/components/charts/LifetimeChart.tsx`
Client Component (`'use client'`)

```typescript
interface LifetimeChartProps {
  scores: DimensionScores;   // .labels (12 items), .duong, .am, .tb
  alerts: Alert[];
  height?: number;           // default 240
}
```

**Recharts implementation:**

```typescript
// Transform data
const chartData = scores.labels.map((label, i) => ({
  period: label,                 // e.g. "10-20"
  duong: scores.duong[i],
  am: scores.am[i],
  tb: scores.tb[i],
  alert: alerts.find(a => a.period === label) ?? null,
}));

// Custom dot for alert markers
const CustomDot = (props: any) => {
  const { cx, cy, payload } = props;
  if (!payload.alert) return null;

  const isPositive = payload.alert.type === 'positive';
  return (
    <g>
      <circle cx={cx} cy={cy} r={5} fill={isPositive ? '#10B981' : '#F59E0B'} />
      <text x={cx} y={cy - 10} textAnchor="middle" fontSize={10} fill={isPositive ? '#10B981' : '#F59E0B'}>
        {isPositive ? '▲' : '▼'}
      </text>
    </g>
  );
};
```

```tsx
<ResponsiveContainer width="100%" height={height ?? 240}>
  <LineChart data={chartData} margin={CHART_DEFAULTS.margin}>
    <CartesianGrid strokeDasharray="3 3" stroke="#F3F4F6" vertical={false} />

    <XAxis
      dataKey="period"
      tick={axisStyle.tick}
      axisLine={false}
      tickLine={false}
      interval={isMobile ? 1 : 0}  // mobile: every other label; desktop: all labels
      fontSize={11}
    />

    <YAxis
      tick={axisStyle.tick}
      axisLine={false}
      tickLine={false}
      width={32}
      tickFormatter={(v) => v.toFixed(0)}
    />

    <Tooltip
      contentStyle={tooltipStyle}
      formatter={(value: number, name: string) => [value.toFixed(2), name]}
      labelFormatter={(label) => `Giai đoạn: ${label}`}
    />

    {/* TB line first (behind) — alert markers ONLY on this line (I4) */}
    <Line
      type="monotone"
      dataKey="tb"
      name="TB"
      stroke={CHART_COLORS.tb}
      strokeWidth={1.5}
      dot={(props) => <CustomDot {...props} />}   // I4: CustomDot ONLY on TB line
      activeDot={{ r: 4, fill: CHART_COLORS.tb }}
      strokeDasharray="4 4"        // dashed for TB
    />

    {/* Âm line — NO custom dots */}
    <Line
      type="monotone"
      dataKey="am"
      name="Âm"
      stroke={CHART_COLORS.am}
      strokeWidth={2}
      dot={false}
      activeDot={{ r: 4, fill: CHART_COLORS.am }}
    />

    {/* Dương line (on top) — NO custom dots */}
    <Line
      type="monotone"
      dataKey="duong"
      name="Dương"
      stroke={CHART_COLORS.duong}
      strokeWidth={2}
      dot={false}
      activeDot={{ r: 4, fill: CHART_COLORS.duong }}
    />
  </LineChart>
</ResponsiveContainer>
```

**Alert marker placement (I4):** `CustomDot` renders ONLY on the TB (summary) line. This avoids duplication — since TB = Dương + Âm combined, alerts most meaningfully apply to TB. DecadeChart and MonthlyChart follow the same rule: attach `CustomDot` only to the TB `<Line>`, use `dot={false}` on Dương and Âm lines.

**Mobile notes:**
- At 375px: 12 labels crowd the X-axis. Use `interval={isMobile ? 1 : 0}` — shows every other label
  on mobile (e.g. "10-20", "30-40", ...) and all labels on desktop. See `useIsMobile` in §8.3.
- Min font size for axis labels: 10px.

---

### 8.3 DecadeChart Component

**File:** `frontend/components/charts/DecadeChart.tsx`

```typescript
interface DecadeChartProps {
  scores: DimensionScores;   // .labels (10 items: years), .duong, .am, .tb
  alerts: Alert[];
  height?: number;           // default 240
}
```

Same structure as LifetimeChart. Key differences:
- X-axis labels are integers from API (e.g. 2026, 2027, ...) — render via `String(label)` in tickFormatter
- `interval={0}` on desktop (≥640px) — all 10 year labels fit
- `interval={1}` on mobile (<640px) — I10: show every other label (2026, 2028, 2030...) to prevent crowding at 375px
  Pass `isMobile` as a prop from the parent Server Component page, computed as:
  `const isMobile = typeof window !== 'undefined' && window.innerWidth < 640`
  (evaluated in the parent Client Component that wraps the chart, or via the pattern below).
  Example: `interval={isMobile ? 1 : 0}`

  If a reusable hook is preferred, add this to `frontend/lib/utils.ts`:
  ```typescript
  // Simple SSR-safe media query hook for Client Components
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
  Charts are Client Components (`'use client'`) so this hook is safe to call directly inside them.
- Font size can stay 11px — years are short strings
- alert markers: CustomDot only on TB line (consistent with I4)

---

### 8.4 MonthlyChart Component

**File:** `frontend/components/charts/MonthlyChart.tsx`

```typescript
interface MonthlyChartProps {
  scores: DimensionScores;   // .labels (13 items: months), .duong, .am, .tb
  alerts: Alert[];
  height?: number;           // default 240
}
```

Key differences from Lifetime:
- 13 data points: first label is repeated (the first "Th.1/YYYY" is the prepended anchor from lifetime)
- Backend sends full labels in format "Th.X/YYYY" (e.g. "Th.1/2026", "Th.2/2026") — as specified in ARCHITECTURE.md §5
- X-axis display: truncate to "Th.X" for readability using `tickFormatter`:
  ```typescript
  // Strip year suffix for X-axis display — keep full label in tooltip
  const tickFormatter = (label: string | number) => String(label).split('/')[0] ?? String(label);
  // e.g. "Th.1/2026" → "Th.1"
  ```
- Tooltip `labelFormatter` should show the FULL label including year: `(label) => \`Tháng: \${label}\``
- Display note below chart: text-caption text-text-tertiary "* Tháng 1 được hiển thị hai lần do cách tính của hệ thống."
- `interval={1}` — with 13 items, still manageable on desktop.
  On mobile (<640px): use `interval={2}` to show "Th.1", "Th.3", "Th.5"... — pass as prop or detect via window width hook.
  <!-- M10: interval clarification — desktop interval={1}, mobile interval={2} -->

---

### 8.5 OverviewChart — Radar (Desktop)

**File:** `frontend/components/charts/OverviewRadarChart.tsx`

```typescript
interface OverviewRadarChartProps {
  dimensions: Record<string, DimensionData>;
  height?: number;   // default 280
}
```

```typescript
// Transform: normalize summaryScore to 0-100 for radar
const normalize = (score: number) => Math.max(0, Math.min(100, ((score + 20) / 40) * 100));

const radarData = DIMENSION_ORDER.map(key => ({
  dimension: DIMENSION_LABELS[key],
  value: normalize(dimensions[key].summaryScore),
  fullMark: 100,
}));
```

```tsx
<ResponsiveContainer width="100%" height={280}>
  <RadarChart cx="50%" cy="50%" outerRadius="75%" data={radarData}>
    <PolarGrid stroke="#E5E7EB" />
    {/* M6: At 640px (the sm breakpoint), radar labels can overlap for longer names.
        Use fontSize=10 and truncate labels >6 chars to keep the chart readable.
        The radar chart is hidden below 640px (CSS), so this only applies at exactly 640–768px. */}
    <PolarAngleAxis
      dataKey="dimension"
      tick={{ fill: '#6B7280', fontSize: 10 }}
      tickFormatter={(label: string) => label.length > 6 ? label.slice(0, 6) + '…' : label}
    />
    <PolarRadiusAxis
      angle={90}
      domain={[0, 100]}
      tick={false}
      axisLine={false}
    />
    <Radar
      name="Vận mệnh"
      dataKey="value"
      stroke="#2563EB"
      fill="#2563EB"
      fillOpacity={0.08}
      strokeWidth={2}
    />
    <Tooltip
      contentStyle={tooltipStyle}
      formatter={(v: number) => [`${v.toFixed(0)}/100`, 'Điểm']}
    />
  </RadarChart>
</ResponsiveContainer>
```

---

### 8.6 OverviewChart — Horizontal Bar (Mobile)

**File:** `frontend/components/charts/OverviewBarChart.tsx`

```typescript
// Same props as RadarChart
```

```tsx
const barData = DIMENSION_ORDER.map(key => ({
  name: DIMENSION_LABELS[key],
  score: normalize(dimensions[key].summaryScore),
}));

{/* M5: Responsive height — 8 bars × 40px + 32px padding = 352px fixed.
    On mobile the bar labels may be tight; min-height 280px (7px per bar min).
    ResponsiveContainer fills parent width, height is pixel-fixed based on data count. */}
<ResponsiveContainer width="100%" height={Math.max(280, barData.length * 40 + 32)}>
  <BarChart
    data={barData}
    layout="vertical"
    margin={{ top: 4, right: 40, bottom: 4, left: 56 }}
  >
    <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#F3F4F6" />
    <XAxis type="number" domain={[0, 100]} tick={axisStyle.tick} axisLine={false} tickLine={false} />
    <YAxis
      type="category"
      dataKey="name"
      width={52}
      tick={{ fill: '#6B7280', fontSize: 12 }}
      axisLine={false}
      tickLine={false}
    />
    <Tooltip
      contentStyle={tooltipStyle}
      formatter={(v: number) => [`${v.toFixed(0)}/100`, 'Điểm']}
    />
    <Bar dataKey="score" fill="#2563EB" radius={[0, 4, 4, 0]} barSize={16} />
  </BarChart>
</ResponsiveContainer>
```

---
