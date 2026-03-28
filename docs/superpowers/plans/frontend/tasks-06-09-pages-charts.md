# Frontend Plan — Tasks 6-9: Processing, Charts, Result, Detail

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans. Steps use checkbox (`- [ ]`) syntax.

**Spec references:**
- `docs/superpowers/specs/frontend/03-processing-result.md`
- `docs/superpowers/specs/frontend/04-detail-charts.md`

**Prerequisites:** Tasks 1-5 completed (design system, types, constants, API client, landing page, form)

---

# Task 6: Processing Screen

**Goal:** Build the `/processing/[id]` page that polls the backend every 2 seconds, renders step progress, and navigates to the result page when complete.

**Files to create:**
- `frontend/app/processing/[id]/page.tsx`
- `frontend/components/processing/ProcessingScreen.tsx`
- `frontend/components/processing/StepIndicator.tsx`
- `frontend/components/processing/FunFactRotator.tsx`

---

- [ ] **Step 6.1 — Create `frontend/app/processing/[id]/page.tsx`**

Server shell. Renders the client `ProcessingScreen` with the `profileId` from params.

```tsx
import ProcessingScreen from '@/components/processing/ProcessingScreen';

export default function ProcessingPage({ params }: { params: { id: string } }) {
  return <ProcessingScreen profileId={params.id} />;
}
```

---

- [ ] **Step 6.2 — Create `frontend/components/processing/ProcessingScreen.tsx`**

Client Component. All polling logic lives here.

```tsx
'use client';

import { useEffect, useRef, useState } from 'react';
import { useRouter } from 'next/navigation';
import { AlertTriangle } from 'lucide-react';
import { getProfileStatus, generateProfile } from '@/lib/api';
import { ProfileStatus } from '@/lib/types';
import StepIndicator from './StepIndicator';
import FunFactRotator from './FunFactRotator';

const POLL_INTERVAL = 2000;
const TIMEOUT_MS = 120000;

interface Props {
  profileId: string;
}

export default function ProcessingScreen({ profileId }: Props) {
  const router = useRouter();
  const [currentStatus, setCurrentStatus] = useState<ProfileStatus | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isRetrying, setIsRetrying] = useState(false);
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const retryCount = useRef(0);

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

        timeoutRef.current = setTimeout(poll, POLL_INTERVAL);
      } catch {
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
  }, [profileId, router]);

  const handleRetry = async () => {
    setIsRetrying(true);
    try {
      const lastInput = sessionStorage.getItem('tuvi_last_input');
      if (lastInput) {
        const result = await generateProfile(JSON.parse(lastInput));
        router.push(`/processing/${result.profileId}`);
      } else {
        router.push('/form');
      }
    } catch {
      router.push('/form');
    } finally {
      setIsRetrying(false);
    }
  };

  const aiProgress = currentStatus?.aiProgress ?? 0;
  const step = currentStatus?.status ?? 'scraping_cohoc';

  return (
    <div className="bg-bg-primary min-h-screen flex flex-col items-center justify-center px-4 py-16">
      <div className="max-w-[400px] w-full text-center">
        {/* Pulsing animation */}
        <div className="flex gap-2 justify-center mb-10">
          {[0, 160, 320].map((delay) => (
            <div
              key={delay}
              className="w-2.5 h-2.5 bg-accent rounded-full"
              style={{ animation: `pulse-dot 1.2s ease-in-out infinite ${delay}ms` }}
            />
          ))}
        </div>

        {/* Step indicator */}
        <StepIndicator step={step} />

        {/* Progress text */}
        <div className="mt-6 text-center">
          {error ? (
            <div className="flex flex-col items-center">
              <AlertTriangle className="w-6 h-6 text-amber-500 mb-3" />
              <p className="text-body text-text-primary font-medium">
                Có lỗi xảy ra trong quá trình xử lý.
              </p>
              <p className="text-body-sm text-text-secondary mt-1">{error}</p>
              <button
                onClick={handleRetry}
                disabled={isRetrying}
                className="mt-4 px-6 py-2 bg-accent text-white rounded-[8px] text-body font-medium hover:bg-accent/90 disabled:opacity-50 transition-colors"
              >
                {isRetrying ? 'Đang thử lại...' : 'Thử lại'}
              </button>
            </div>
          ) : step === 'ai_generating' ? (
            <>
              <p className="text-body-sm text-text-secondary">
                {aiProgress}/8 lĩnh vực đã được phân tích
              </p>
              <div className="w-[200px] h-1 bg-bg-subtle rounded-full mx-auto mt-2 overflow-hidden">
                <div
                  className="h-full bg-accent rounded-full transition-[width] duration-300 ease-in-out"
                  style={{ width: `${(aiProgress / 8) * 100}%` }}
                />
              </div>
            </>
          ) : (
            <p className="text-body-sm text-text-secondary">
              {currentStatus?.message ?? 'Đang khởi tạo...'}
            </p>
          )}
        </div>

        {/* Fun fact rotator */}
        {!error && <FunFactRotator />}
      </div>
    </div>
  );
}
```

**Note:** Add the `pulse-dot` keyframes to `frontend/app/globals.css`:

```css
@keyframes pulse-dot {
  0%, 100% { transform: scale(0.8); opacity: 0.4; }
  50%       { transform: scale(1.2); opacity: 1; }
}
```

---

- [ ] **Step 6.3 — Create `frontend/components/processing/StepIndicator.tsx`**

Server-safe (no `'use client'` needed — receives step as string prop). Renders 4 steps with correct status per step.

```tsx
import { CheckCircle2, Loader2 } from 'lucide-react';

type ApiStep =
  | 'scraping_cohoc'
  | 'scraping_tuvivn'
  | 'scoring'
  | 'ai_generating'
  | 'completed'
  | 'failed'
  | string;

interface Props {
  step: ApiStep;
}

// Returns 'completed' | 'in-progress' | 'pending' for each UI step index (0-3)
function getStepStatus(
  uiStepIndex: number,
  apiStep: ApiStep
): 'completed' | 'in-progress' | 'pending' {
  const mapping: Record<ApiStep, number> = {
    scraping_cohoc:  0,
    scraping_tuvivn: 0,
    scoring:         1,
    ai_generating:   2,
    completed:       3,
  };

  const currentUiStep = mapping[apiStep] ?? 0;

  if (uiStepIndex < currentUiStep) return 'completed';
  if (uiStepIndex === currentUiStep) return 'in-progress';
  return 'pending';
}

const STEPS = [
  'Đang lấy lá số...',
  'Đang tính toán điểm số...',
  'Đang phân tích vận mệnh...',
  'Hoàn tất!',
];

export default function StepIndicator({ step }: Props) {
  // When completed, all steps are 'completed'
  const resolvedStep = step === 'completed' ? 'completed' : step;

  return (
    <div className="flex flex-col gap-3 max-w-[280px] mx-auto">
      {STEPS.map((label, i) => {
        const status =
          resolvedStep === 'completed'
            ? 'completed'
            : getStepStatus(i, resolvedStep);

        return (
          <div key={i} className="flex items-center gap-3">
            {/* Status icon */}
            <div className="w-6 h-6 flex-shrink-0 flex items-center justify-center">
              {status === 'completed' ? (
                <CheckCircle2 className="w-5 h-5 text-alert-positive" />
              ) : status === 'in-progress' ? (
                <Loader2 className="w-[18px] h-[18px] text-accent animate-spin" />
              ) : (
                <div className="w-4 h-4 rounded-full border-2 border-border mx-auto" />
              )}
            </div>

            {/* Label */}
            <span
              className={
                status === 'pending'
                  ? 'text-body text-text-tertiary'
                  : 'text-body font-medium text-text-primary'
              }
            >
              {label}
            </span>
          </div>
        );
      })}
    </div>
  );
}
```

---

- [ ] **Step 6.4 — Create `frontend/components/processing/FunFactRotator.tsx`**

Client Component. Rotates through facts every 5 seconds with a fade transition.

```tsx
'use client';

import { useEffect, useState } from 'react';
import { FUN_FACTS } from '@/lib/constants';

export default function FunFactRotator() {
  const [index, setIndex] = useState(0);
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    const interval = setInterval(() => {
      // Fade out
      setVisible(false);
      setTimeout(() => {
        setIndex((prev) => (prev + 1) % FUN_FACTS.length);
        // Fade in
        setVisible(true);
      }, 300);
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="mt-12 max-w-[320px] mx-auto text-center">
      <div className="bg-bg-subtle rounded-[12px] px-5 py-4">
        <p className="text-caption text-text-tertiary font-medium mb-1">Bạn có biết?</p>
        <p
          className="text-body-sm text-text-secondary transition-opacity duration-300"
          style={{ opacity: visible ? 1 : 0 }}
        >
          {FUN_FACTS[index]}
        </p>
      </div>
    </div>
  );
}
```

**Prerequisite:** `FUN_FACTS` must exist in `lib/constants.ts`. If not already present, add:

```ts
export const FUN_FACTS = [
  'Hệ thống Tử Vi Đẩu Số có 14 chính tinh và hơn 100 phụ tinh, tạo ra vô số tổ hợp độc đáo.',
  'Lá số của bạn là duy nhất — chỉ ai sinh cùng ngày, giờ và giới tính mới có lá số giống hệt.',
  'Tử Vi Đẩu Số có nguồn gốc hơn 1000 năm, được hoàn thiện trong triều đại Tống ở Trung Hoa.',
  'Hệ thống chia cuộc đời thành các chu kỳ 10 năm (Đại Vận) — mỗi chu kỳ có năng lượng riêng.',
  'AI đang phân tích hàng trăm điểm dữ liệu từ lá số của bạn để tạo luận giải cá nhân hóa.',
];
```

---

- [ ] **Step 6.5 — Verify Task 6**

```
- [ ] Navigate to /processing/[any-id] — page renders without error
- [ ] Polling starts immediately (network tab shows GET /api/profile/{id}/status every 2s)
- [ ] Steps advance correctly as API step changes:
      scraping_cohoc  → step 1 spinner, steps 2-4 pending
      scoring         → step 1 check, step 2 spinner, steps 3-4 pending
      ai_generating   → steps 1-2 check, step 3 spinner, step 4 pending
      completed       → all 4 steps show check, redirect fires
- [ ] ai_generating shows progress bar: "{n}/8 lĩnh vực đã được phân tích"
- [ ] Progress bar width = (n/8)*100%
- [ ] Error state: AlertTriangle + message + "Thử lại" button
- [ ] Retry with sessionStorage data → re-POST → navigate to new /processing/[newId]
- [ ] Retry with no sessionStorage → navigate to /form
- [ ] Network timeout after 3 failures → "Mất kết nối" error
- [ ] Global timeout after 120s → "Quá thời gian chờ" error
- [ ] Fun facts rotate every 5s with fade
- [ ] Cleanup: polling stops on unmount (no memory leaks)
- [ ] Pulsing dots animation plays (3 dots, staggered 0/160/320ms)
```

- [ ] **Step 6.6 — Commit Task 6**

```bash
git add frontend/app/processing frontend/components/processing frontend/app/globals.css
git commit -m "feat: add processing screen with polling, steps, and fun facts"
```

---

# Task 7: Chart Components

**Goal:** Build all Recharts components used in the dimension detail page and the overview page.

**Files to create:**
- `frontend/components/charts/chartConfig.ts`
- `frontend/components/charts/ChartCard.tsx`
- `frontend/components/charts/ChartSkeleton.tsx`
- `frontend/components/charts/LifetimeChart.tsx`
- `frontend/components/charts/DecadeChart.tsx`
- `frontend/components/charts/MonthlyChart.tsx`
- `frontend/components/charts/OverviewRadarChart.tsx`
- `frontend/components/charts/OverviewBarChart.tsx`

**Test file:**
- `frontend/components/charts/__tests__/scoreNormalization.test.ts`

**Install dependency:** `npm install recharts react-markdown rehype-raw` (if not already installed)

---

- [ ] **Step 7.1 — Create `frontend/components/charts/chartConfig.ts`**

No React import needed — pure constants.

```ts
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
  dotRadius: 0,
  activeDotRadius: 4,
} as const;

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

- [ ] **Step 7.2 — Create `frontend/components/charts/ChartCard.tsx`**

Server Component — no `'use client'`. Wrapper with title, subtitle, legend.

```tsx
import { ReactNode } from 'react';

interface ChartCardProps {
  title: string;
  subtitle?: string;
  children: ReactNode;
}

export default function ChartCard({ title, subtitle, children }: ChartCardProps) {
  return (
    <div className="bg-bg-surface border border-border rounded-[12px] p-4 sm:p-6 mt-4">
      <div>
        <p className="text-label font-semibold text-text-primary">{title}</p>
        {subtitle && (
          <p className="text-body-sm text-text-tertiary mt-0.5">{subtitle}</p>
        )}
      </div>

      <div className="mt-4 overflow-hidden">{children}</div>

      {/* Legend */}
      <div className="flex gap-4 mt-3 justify-center">
        {[
          { label: 'Dương', color: 'bg-chart-duong' },
          { label: 'Âm',    color: 'bg-chart-am' },
          { label: 'TB',    color: 'bg-chart-tb' },
        ].map(({ label, color }) => (
          <div key={label} className="flex items-center gap-1.5">
            <div className={`w-8 h-0.5 ${color}`} />
            <span className="text-caption text-text-secondary">{label}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
```

---

- [ ] **Step 7.3 — Create `frontend/components/charts/ChartSkeleton.tsx`**

Server Component. Animate-pulse placeholder shown while chart data loads.

```tsx
interface ChartSkeletonProps {
  height?: number;
}

export default function ChartSkeleton({ height = 240 }: ChartSkeletonProps) {
  return (
    <div
      className="w-full bg-bg-subtle rounded-[8px] animate-pulse"
      style={{ height }}
    />
  );
}
```

---

- [ ] **Step 7.4 — Create `frontend/components/charts/LifetimeChart.tsx`**

Client Component. 12 data points, 3 lines. `CustomDot` renders alert markers **only on the TB line** (I4).

```tsx
'use client';

import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from 'recharts';
import { useIsMobile } from '@/lib/utils';
import { DimensionScores, Alert } from '@/lib/types';
import { CHART_COLORS, CHART_DEFAULTS, tooltipStyle, axisStyle } from './chartConfig';

interface LifetimeChartProps {
  scores: DimensionScores;
  alerts: Alert[];
  height?: number;
}

// I4: CustomDot renders ONLY on TB line — alert markers for positive (▲) and negative (▼)
const CustomDot = (props: any) => {
  const { cx, cy, payload } = props;
  if (!payload.alert) return <g />;

  const isPositive = payload.alert.type === 'positive';
  const color = isPositive ? '#10B981' : '#F59E0B';
  const symbol = isPositive ? '▲' : '▼';

  return (
    <g>
      <circle cx={cx} cy={cy} r={5} fill={color} />
      <text
        x={cx}
        y={cy - 10}
        textAnchor="middle"
        fontSize={10}
        fill={color}
      >
        {symbol}
      </text>
    </g>
  );
};

export default function LifetimeChart({ scores, alerts, height = 240 }: LifetimeChartProps) {
  const isMobile = useIsMobile();

  const chartData = scores.labels.map((label, i) => ({
    period: label,
    duong: scores.duong[i],
    am: scores.am[i],
    tb: scores.tb[i],
    alert: alerts.find((a) => a.period === label) ?? null,
  }));

  return (
    <ResponsiveContainer width="100%" height={height}>
      <LineChart data={chartData} margin={CHART_DEFAULTS.margin}>
        <CartesianGrid strokeDasharray="3 3" stroke="#F3F4F6" vertical={false} />

        <XAxis
          dataKey="period"
          tick={axisStyle.tick}
          axisLine={false}
          tickLine={false}
          interval={isMobile ? 1 : 0}
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

        {/* TB line — CustomDot ONLY here (I4) */}
        <Line
          type="monotone"
          dataKey="tb"
          name="TB"
          stroke={CHART_COLORS.tb}
          strokeWidth={1.5}
          strokeDasharray="4 4"
          dot={(props: any) => <CustomDot {...props} />}
          activeDot={{ r: 4, fill: CHART_COLORS.tb }}
          animationDuration={CHART_DEFAULTS.animationDuration}
        />

        {/* Âm line — no custom dots */}
        <Line
          type="monotone"
          dataKey="am"
          name="Âm"
          stroke={CHART_COLORS.am}
          strokeWidth={2}
          dot={false}
          activeDot={{ r: 4, fill: CHART_COLORS.am }}
          animationDuration={CHART_DEFAULTS.animationDuration}
        />

        {/* Dương line — no custom dots */}
        <Line
          type="monotone"
          dataKey="duong"
          name="Dương"
          stroke={CHART_COLORS.duong}
          strokeWidth={2}
          dot={false}
          activeDot={{ r: 4, fill: CHART_COLORS.duong }}
          animationDuration={CHART_DEFAULTS.animationDuration}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
```

---

- [ ] **Step 7.5 — Create `frontend/components/charts/DecadeChart.tsx`**

Client Component. 10 data points (year integers). Same structure as `LifetimeChart` with integer year labels.

```tsx
'use client';

import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from 'recharts';
import { useIsMobile } from '@/lib/utils';
import { DimensionScores, Alert } from '@/lib/types';
import { CHART_COLORS, CHART_DEFAULTS, tooltipStyle, axisStyle } from './chartConfig';

interface DecadeChartProps {
  scores: DimensionScores;
  alerts: Alert[];
  height?: number;
}

// I4: CustomDot ONLY on TB line
const CustomDot = (props: any) => {
  const { cx, cy, payload } = props;
  if (!payload.alert) return <g />;

  const isPositive = payload.alert.type === 'positive';
  const color = isPositive ? '#10B981' : '#F59E0B';

  return (
    <g>
      <circle cx={cx} cy={cy} r={5} fill={color} />
      <text x={cx} y={cy - 10} textAnchor="middle" fontSize={10} fill={color}>
        {isPositive ? '▲' : '▼'}
      </text>
    </g>
  );
};

export default function DecadeChart({ scores, alerts, height = 240 }: DecadeChartProps) {
  const isMobile = useIsMobile();

  const chartData = scores.labels.map((label, i) => ({
    period: label,
    duong: scores.duong[i],
    am: scores.am[i],
    tb: scores.tb[i],
    alert: alerts.find((a) => a.period === String(label)) ?? null,
  }));

  return (
    <ResponsiveContainer width="100%" height={height}>
      <LineChart data={chartData} margin={CHART_DEFAULTS.margin}>
        <CartesianGrid strokeDasharray="3 3" stroke="#F3F4F6" vertical={false} />

        <XAxis
          dataKey="period"
          tick={axisStyle.tick}
          axisLine={false}
          tickLine={false}
          interval={isMobile ? 1 : 0}
          tickFormatter={(v) => String(v)}
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
          labelFormatter={(label) => `Năm: ${label}`}
        />

        {/* TB — CustomDot only (I4) */}
        <Line
          type="monotone"
          dataKey="tb"
          name="TB"
          stroke={CHART_COLORS.tb}
          strokeWidth={1.5}
          strokeDasharray="4 4"
          dot={(props: any) => <CustomDot {...props} />}
          activeDot={{ r: 4, fill: CHART_COLORS.tb }}
          animationDuration={CHART_DEFAULTS.animationDuration}
        />

        <Line
          type="monotone"
          dataKey="am"
          name="Âm"
          stroke={CHART_COLORS.am}
          strokeWidth={2}
          dot={false}
          activeDot={{ r: 4, fill: CHART_COLORS.am }}
          animationDuration={CHART_DEFAULTS.animationDuration}
        />

        <Line
          type="monotone"
          dataKey="duong"
          name="Dương"
          stroke={CHART_COLORS.duong}
          strokeWidth={2}
          dot={false}
          activeDot={{ r: 4, fill: CHART_COLORS.duong }}
          animationDuration={CHART_DEFAULTS.animationDuration}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
```

---

- [ ] **Step 7.6 — Create `frontend/components/charts/MonthlyChart.tsx`**

Client Component. 13 data points. Strips year from X-axis labels; shows full label in tooltip. Duplicate-month note below chart.

```tsx
'use client';

import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from 'recharts';
import { useIsMobile } from '@/lib/utils';
import { DimensionScores, Alert } from '@/lib/types';
import { CHART_COLORS, CHART_DEFAULTS, tooltipStyle, axisStyle } from './chartConfig';

interface MonthlyChartProps {
  scores: DimensionScores;
  alerts: Alert[];
  height?: number;
}

// I4: CustomDot ONLY on TB line
const CustomDot = (props: any) => {
  const { cx, cy, payload } = props;
  if (!payload.alert) return <g />;

  const isPositive = payload.alert.type === 'positive';
  const color = isPositive ? '#10B981' : '#F59E0B';

  return (
    <g>
      <circle cx={cx} cy={cy} r={5} fill={color} />
      <text x={cx} y={cy - 10} textAnchor="middle" fontSize={10} fill={color}>
        {isPositive ? '▲' : '▼'}
      </text>
    </g>
  );
};

// Strip year suffix: "Th.1/2026" → "Th.1"
const tickFormatter = (label: string | number) =>
  String(label).split('/')[0] ?? String(label);

export default function MonthlyChart({ scores, alerts, height = 240 }: MonthlyChartProps) {
  const isMobile = useIsMobile();

  const chartData = scores.labels.map((label, i) => ({
    period: label,
    duong: scores.duong[i],
    am: scores.am[i],
    tb: scores.tb[i],
    alert: alerts.find((a) => a.period === label) ?? null,
  }));

  return (
    <div>
      <ResponsiveContainer width="100%" height={height}>
        <LineChart data={chartData} margin={CHART_DEFAULTS.margin}>
          <CartesianGrid strokeDasharray="3 3" stroke="#F3F4F6" vertical={false} />

          <XAxis
            dataKey="period"
            tick={axisStyle.tick}
            axisLine={false}
            tickLine={false}
            interval={isMobile ? 2 : 1}
            tickFormatter={tickFormatter}
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
            labelFormatter={(label) => `Tháng: ${label}`}
          />

          {/* TB — CustomDot only (I4) */}
          <Line
            type="monotone"
            dataKey="tb"
            name="TB"
            stroke={CHART_COLORS.tb}
            strokeWidth={1.5}
            strokeDasharray="4 4"
            dot={(props: any) => <CustomDot {...props} />}
            activeDot={{ r: 4, fill: CHART_COLORS.tb }}
            animationDuration={CHART_DEFAULTS.animationDuration}
          />

          <Line
            type="monotone"
            dataKey="am"
            name="Âm"
            stroke={CHART_COLORS.am}
            strokeWidth={2}
            dot={false}
            activeDot={{ r: 4, fill: CHART_COLORS.am }}
            animationDuration={CHART_DEFAULTS.animationDuration}
          />

          <Line
            type="monotone"
            dataKey="duong"
            name="Dương"
            stroke={CHART_COLORS.duong}
            strokeWidth={2}
            dot={false}
            activeDot={{ r: 4, fill: CHART_COLORS.duong }}
            animationDuration={CHART_DEFAULTS.animationDuration}
          />
        </LineChart>
      </ResponsiveContainer>

      <p className="text-caption text-text-tertiary mt-2">
        * Tháng 1 được hiển thị hai lần do cách tính của hệ thống.
      </p>
    </div>
  );
}
```

---

- [ ] **Step 7.7 — Create `frontend/components/charts/OverviewRadarChart.tsx`**

Client Component. 8-dimension radar. Normalized 0–100. Label truncation at 6 chars (M6).

```tsx
'use client';

import {
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  Tooltip,
} from 'recharts';
import { DimensionData } from '@/lib/types';
import { DIMENSION_ORDER, DIMENSION_LABELS } from '@/lib/constants';
import { tooltipStyle } from './chartConfig';

interface OverviewRadarChartProps {
  dimensions: Record<string, DimensionData>;
  height?: number;
}

// Score normalization: summaryScore (~-20 to +20) → 0-100
export const normalize = (score: number): number =>
  Math.max(0, Math.min(100, ((score + 20) / 40) * 100));

export default function OverviewRadarChart({ dimensions, height = 280 }: OverviewRadarChartProps) {
  const radarData = DIMENSION_ORDER.map((key) => ({
    dimension: DIMENSION_LABELS[key],
    value: normalize(dimensions[key]?.summaryScore ?? 0),
    fullMark: 100,
  }));

  return (
    <ResponsiveContainer width="100%" height={height}>
      <RadarChart cx="50%" cy="50%" outerRadius="75%" data={radarData}>
        <PolarGrid stroke="#E5E7EB" />

        {/* M6: At 640px the radar labels can overlap for longer names — truncate >6 chars */}
        <PolarAngleAxis
          dataKey="dimension"
          tick={{ fill: '#6B7280', fontSize: 10 }}
          tickFormatter={(label: string) =>
            label.length > 6 ? label.slice(0, 6) + '…' : label
          }
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
  );
}
```

---

- [ ] **Step 7.8 — Create `frontend/components/charts/OverviewBarChart.tsx`**

Client Component. Horizontal bar chart for mobile. Responsive height (M5).

```tsx
'use client';

import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from 'recharts';
import { DimensionData } from '@/lib/types';
import { DIMENSION_ORDER, DIMENSION_LABELS } from '@/lib/constants';
import { tooltipStyle, axisStyle } from './chartConfig';
import { normalize } from './OverviewRadarChart';

interface OverviewBarChartProps {
  dimensions: Record<string, DimensionData>;
}

export default function OverviewBarChart({ dimensions }: OverviewBarChartProps) {
  const barData = DIMENSION_ORDER.map((key) => ({
    name: DIMENSION_LABELS[key],
    score: normalize(dimensions[key]?.summaryScore ?? 0),
  }));

  // M5: Responsive height — 8 bars × 40px + 32px padding
  const chartHeight = Math.max(280, barData.length * 40 + 32);

  return (
    <ResponsiveContainer width="100%" height={chartHeight}>
      <BarChart
        data={barData}
        layout="vertical"
        margin={{ top: 4, right: 40, bottom: 4, left: 56 }}
      >
        <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#F3F4F6" />

        <XAxis
          type="number"
          domain={[0, 100]}
          tick={axisStyle.tick}
          axisLine={false}
          tickLine={false}
        />

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
  );
}
```

---

- [ ] **Step 7.9 — Create `frontend/components/charts/__tests__/scoreNormalization.test.ts`**

Vitest unit test for score normalization formula.

```ts
import { describe, it, expect } from 'vitest';
import { normalize } from '../OverviewRadarChart';

describe('normalize (score normalization)', () => {
  it('maps -20 to 0', () => {
    expect(normalize(-20)).toBe(0);
  });

  it('maps 0 to 50', () => {
    expect(normalize(0)).toBe(50);
  });

  it('maps +20 to 100', () => {
    expect(normalize(20)).toBe(100);
  });

  it('clamps below -20 to 0', () => {
    expect(normalize(-30)).toBe(0);
  });

  it('clamps above +20 to 100', () => {
    expect(normalize(30)).toBe(100);
  });

  it('maps +10 to 75', () => {
    expect(normalize(10)).toBe(75);
  });

  it('maps -10 to 25', () => {
    expect(normalize(-10)).toBe(25);
  });
});
```

---

- [ ] **Step 7.10 — Verify Task 7**

```
- [ ] npx vitest run components/charts/__tests__/scoreNormalization.test.ts — all 7 tests pass
- [ ] LifetimeChart renders 3 lines in Storybook/dev; CustomDot only appears on TB line
- [ ] Positive alerts show green ▲ dot; negative show amber ▼ dot
- [ ] DecadeChart: X-axis labels are integers via String(label)
- [ ] MonthlyChart: "Th.1/2026" tick displays as "Th.1"; tooltip shows full "Tháng: Th.1/2026"
- [ ] MonthlyChart: duplicate-month note appears below chart
- [ ] OverviewRadarChart: labels longer than 6 chars are truncated with "…"
- [ ] OverviewBarChart: height = Math.max(280, n * 40 + 32) for n dimensions
- [ ] ChartCard: legend shows 3 line indicators (Dương/Âm/TB) as w-8 h-0.5 divs
- [ ] ChartSkeleton: animate-pulse placeholder at requested height
- [ ] No 'use client' in ChartCard, ChartSkeleton (Server Components)
```

- [ ] **Step 7.11 — Commit Task 7**

```bash
git add frontend/components/charts
git commit -m "feat: add chart components (lifetime, decade, monthly, radar, bar) with Recharts"
```

---

# Task 8: Result Overview Page

**Goal:** Build the `/result/[id]` page: server-fetched profile data, sticky header with share, profile card, overview chart, AI summary, dimension cards grid, feedback widget, footer.

**Files to create:**
- `frontend/app/result/[id]/page.tsx`
- `frontend/components/result/ResultHeader.tsx`
- `frontend/components/result/ShareButton.tsx`
- `frontend/components/result/ProfileHeaderCard.tsx`
- `frontend/components/result/OverviewChartCard.tsx`
- `frontend/components/result/AIOverviewCard.tsx`
- `frontend/components/result/DimensionCardsGrid.tsx`
- `frontend/components/result/DimensionCard.tsx`
- `frontend/components/result/AlertBadge.tsx`
- `frontend/components/result/FeedbackWidget.tsx`
- `frontend/components/result/ResultFooter.tsx`

---

- [ ] **Step 8.1 — Create `frontend/app/result/[id]/page.tsx`**

Server Component. Fetches profile; calls `notFound()` on failure.

```tsx
import { notFound } from 'next/navigation';
import { getProfile } from '@/lib/api';
import { ProfileData } from '@/lib/types';
import ResultHeader from '@/components/result/ResultHeader';
import ProfileHeaderCard from '@/components/result/ProfileHeaderCard';
import OverviewChartCard from '@/components/result/OverviewChartCard';
import AIOverviewCard from '@/components/result/AIOverviewCard';
import DimensionCardsGrid from '@/components/result/DimensionCardsGrid';
import FeedbackWidget from '@/components/result/FeedbackWidget';
import ResultFooter from '@/components/result/ResultFooter';

export default async function ResultPage({ params }: { params: { id: string } }) {
  let profile: ProfileData;

  try {
    profile = await getProfile(params.id);
  } catch {
    notFound();
  }

  if (!profile) notFound();

  return (
    <div className="bg-bg-primary min-h-screen">
      <ResultHeader profileId={profile.profileId} />

      <main className="max-w-3xl mx-auto px-4 mt-[56px] pb-8">
        <ProfileHeaderCard profile={profile} />
        <OverviewChartCard dimensions={profile.dimensions} />
        <AIOverviewCard summary={profile.overview?.summary ?? null} />
        <DimensionCardsGrid profile={profile} />
        <FeedbackWidget profileId={profile.profileId} />
        <ResultFooter />
      </main>
    </div>
  );
}
```

---

- [ ] **Step 8.2 — Create `frontend/components/result/ResultHeader.tsx`**

Server Component. Contains the `ShareButton` Client island.

```tsx
import Link from 'next/link';
import ShareButton from './ShareButton';

interface Props {
  profileId: string;
}

export default function ResultHeader({ profileId: _ }: Props) {
  return (
    <header className="sticky top-0 z-40 h-14 bg-bg-surface border-b border-border">
      <div className="max-w-3xl mx-auto px-4 h-full flex items-center justify-between">
        <Link href="/" className="text-sm font-semibold text-text-primary">
          TuVi AI
        </Link>
        <ShareButton />
      </div>
    </header>
  );
}
```

---

- [ ] **Step 8.3 — Create `frontend/components/result/ShareButton.tsx`**

Client Component. Clipboard with `execCommand` fallback (I1).

```tsx
'use client';

import { Share2 } from 'lucide-react';
import { toast } from 'sonner';

export default function ShareButton() {
  async function handleShare() {
    const url = window.location.href;
    try {
      await navigator.clipboard.writeText(url);
      toast.success('Đã copy link!', { duration: 3000 });
    } catch {
      // I1: Fallback for browsers without Clipboard API (HTTP context, older Safari)
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

  return (
    <button
      onClick={handleShare}
      className="flex items-center gap-2 text-body text-text-secondary hover:text-text-primary transition-colors px-2 py-1 rounded"
    >
      <Share2 className="w-4 h-4" />
      <span>Chia sẻ</span>
    </button>
  );
}
```

---

- [ ] **Step 8.4 — Create `frontend/components/result/ProfileHeaderCard.tsx`**

Server Component. Name, birth info, menh, ngu hanh pills.

```tsx
import { ProfileData } from '@/lib/types';

interface Props {
  profile: ProfileData;
}

export default function ProfileHeaderCard({ profile }: Props) {
  const birthDate = profile.birthDate;

  return (
    <div className="bg-bg-surface border border-border rounded-[12px] p-6 sm:p-4 flex flex-col gap-1 mt-4">
      <p className="text-caption font-medium text-text-tertiary uppercase tracking-wide mb-1">
        Chánh Ngã Đồ
      </p>

      <h1 className="text-heading-md font-bold text-text-primary">
        {profile.name ? profile.name : 'Kết quả luận giải của bạn'}
      </h1>

      <p className="text-body text-text-secondary mt-1">
        Sinh {birthDate} ({profile.metadata?.nam}), {profile.birthHour}, {profile.gender}
      </p>

      <p className="text-body text-text-secondary">
        Cung Mệnh: {profile.metadata?.cungMenh} — Mệnh {profile.metadata?.menh}
      </p>

      <div className="flex flex-wrap gap-2 mt-3">
        {[profile.metadata?.nam, profile.metadata?.cuc, profile.metadata?.amDuong]
          .filter(Boolean)
          .map((tag) => (
            <span
              key={tag}
              className="text-caption bg-bg-subtle border border-border text-text-secondary px-2 py-1 rounded-full"
            >
              {tag}
            </span>
          ))}
      </div>
    </div>
  );
}
```

---

- [ ] **Step 8.5 — Create `frontend/components/result/OverviewChartCard.tsx`**

Server Component. CSS dual-render (I2): radar hidden below `sm`, bar hidden at `sm` and above.

```tsx
import { DimensionData } from '@/lib/types';
import OverviewRadarChart from '@/components/charts/OverviewRadarChart';
import OverviewBarChart from '@/components/charts/OverviewBarChart';

interface Props {
  dimensions: Record<string, DimensionData>;
}

export default function OverviewChartCard({ dimensions }: Props) {
  return (
    <div className="bg-bg-surface border border-border rounded-[12px] p-4 mt-4">
      <h2 className="text-heading-sm font-semibold text-text-primary mb-4">
        Tổng quan 8 lĩnh vực
      </h2>

      {/* I2: INTENTIONAL DUAL RENDER — both charts are in DOM; CSS handles visibility.
          Avoids hydration mismatch from server/client window width discrepancy. */}
      <div className="hidden sm:block" style={{ height: 300 }}>
        <OverviewRadarChart dimensions={dimensions} height={300} />
      </div>
      <div className="block sm:hidden">
        <OverviewBarChart dimensions={dimensions} />
      </div>

      {/* Legend */}
      <div className="flex gap-4 justify-center mt-2">
        {[
          { label: 'Dương', color: 'bg-chart-duong' },
          { label: 'Âm',    color: 'bg-chart-am' },
          { label: 'TB (Tổng)', color: 'bg-chart-tb' },
        ].map(({ label, color }) => (
          <div key={label} className="flex items-center gap-1.5">
            <div className={`w-8 h-[3px] ${color}`} />
            <span className="text-body-sm text-text-secondary">{label}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
```

---

- [ ] **Step 8.6 — Create `frontend/components/result/AIOverviewCard.tsx`**

Server Component. Summary text or skeleton fallback.

```tsx
import { Sparkles } from 'lucide-react';

interface Props {
  summary: string | null;
}

export default function AIOverviewCard({ summary }: Props) {
  return (
    <div className="bg-bg-surface border border-border rounded-[12px] p-4 mt-4">
      <div className="flex items-center gap-2">
        <Sparkles className="w-[18px] h-[18px] text-accent flex-shrink-0" />
        <h2 className="text-heading-sm font-semibold text-text-primary">
          Tổng quan vận mệnh
        </h2>
      </div>

      <div className="mt-3">
        {summary ? (
          <p className="text-body text-text-secondary leading-relaxed">{summary}</p>
        ) : (
          <div className="flex flex-col gap-2">
            <div className="h-4 bg-bg-subtle rounded animate-pulse" />
            <div className="h-4 bg-bg-subtle rounded animate-pulse" />
            <div className="h-2.5 w-3/4 bg-bg-subtle rounded animate-pulse" />
          </div>
        )}
      </div>
    </div>
  );
}
```

---

- [ ] **Step 8.7 — Create `frontend/components/result/DimensionCardsGrid.tsx`**

Server Component. Maps `DIMENSION_ORDER` with B9 guard.

```tsx
import { ProfileData } from '@/lib/types';
import { DIMENSION_ORDER, DimensionKey } from '@/lib/constants';
import DimensionCard from './DimensionCard';

interface Props {
  profile: ProfileData;
}

export default function DimensionCardsGrid({ profile }: Props) {
  return (
    <section className="mt-8">
      <h2 className="text-heading-sm font-semibold text-text-primary mb-4">
        Xem chi tiết từng lĩnh vực
      </h2>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
        {DIMENSION_ORDER.map((key) => {
          const data = profile.dimensions[key];
          // B9: Guard — skip if dimension data is missing (protects against partial API response)
          if (!data) return null;
          return (
            <DimensionCard
              key={key}
              dimensionKey={key}
              data={data}
              profileId={profile.profileId}
            />
          );
        })}
      </div>
    </section>
  );
}
```

---

- [ ] **Step 8.8 — Create `frontend/components/result/DimensionCard.tsx`**

Server Component. Link wrapper, score bar, alert badges. Hides alerts for `van_menh`.

```tsx
import Link from 'next/link';
import { ChevronRight } from 'lucide-react';
import { DimensionData } from '@/lib/types';
import { DimensionKey, DIMENSION_LABELS, DIMENSION_ICONS } from '@/lib/constants';
import AlertBadge from './AlertBadge';

interface DimensionCardProps {
  dimensionKey: DimensionKey;
  data: DimensionData;
  profileId: string;
}

export default function DimensionCard({ dimensionKey, data, profileId }: DimensionCardProps) {
  const summaryScore = data.summaryScore;
  // Score normalization: ~-20 to +20 → 0-100%
  const barWidth = Math.max(0, Math.min(100, ((summaryScore + 20) / 40) * 100));

  const positiveAlerts = data.alerts?.filter((a) => a.type === 'positive') ?? [];
  const negativeAlerts = data.alerts?.filter((a) => a.type === 'negative') ?? [];

  const Icon = DIMENSION_ICONS[dimensionKey];
  const label = DIMENSION_LABELS[dimensionKey];

  const previewText = data.interpretation
    ? data.interpretation.replace(/[#*_`>]/g, '').slice(0, 80)
    : null;

  return (
    <Link
      href={`/result/${profileId}/${dimensionKey}`}
      className="block bg-bg-surface border border-border rounded-[12px] p-4 hover:border-accent-border hover:shadow-lg transition-all duration-150 cursor-pointer"
    >
      <div className="flex flex-col gap-3">
        {/* Top row: icon + name + arrow */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-[8px] bg-accent-light flex items-center justify-center flex-shrink-0">
              <Icon className="w-[18px] h-[18px] text-accent" />
            </div>
            <span className="text-label font-semibold text-text-primary">{label}</span>
          </div>
          <ChevronRight className="w-4 h-4 text-text-tertiary flex-shrink-0" />
        </div>

        {/* Score bar */}
        <div className="flex items-center gap-2 mt-1">
          <span className="text-mono text-body-sm text-text-tertiary">TB:</span>
          <span className="text-mono font-medium text-text-primary">
            {summaryScore.toFixed(1)}
          </span>
          <div className="flex-1 h-1.5 bg-bg-subtle rounded-full overflow-hidden">
            <div
              className="h-full bg-accent rounded-full"
              style={{ width: `${barWidth}%` }}
            />
          </div>
        </div>

        {/* Alert badges — hidden for van_menh */}
        {dimensionKey !== 'van_menh' && (positiveAlerts.length > 0 || negativeAlerts.length > 0) && (
          <div className="flex flex-wrap gap-1.5">
            {positiveAlerts.length > 0 && (
              <AlertBadge type="positive" count={positiveAlerts.length} />
            )}
            {negativeAlerts.length > 0 && (
              <AlertBadge type="negative" count={negativeAlerts.length} />
            )}
          </div>
        )}

        {/* Interpretation preview */}
        {previewText && (
          <p className="text-body-sm text-text-tertiary leading-snug line-clamp-2">
            {previewText}
          </p>
        )}
      </div>
    </Link>
  );
}
```

---

- [ ] **Step 8.9 — Create `frontend/components/result/AlertBadge.tsx`**

Server Component. Uses `text-emerald-700` / `text-amber-700` per B3 (NOT `text-alert-positive`/`text-alert-negative` which are lower-contrast token values).

```tsx
interface AlertBadgeProps {
  type: 'positive' | 'negative';
  count: number;
  label?: string;
}

export default function AlertBadge({ type, count, label }: AlertBadgeProps) {
  if (type === 'positive') {
    const text = label ?? (count > 1 ? `▲ ${count} cơ hội` : '▲ Cơ hội');
    return (
      <span className="bg-alert-positive-bg border border-alert-positive-bdr text-emerald-700 px-2 py-0.5 rounded-full text-caption font-medium">
        {text}
      </span>
    );
  }

  const text = label ?? `▼ ${count} cần chú ý`;
  return (
    <span className="bg-alert-negative-bg border border-alert-negative-bdr text-amber-700 px-2 py-0.5 rounded-full text-caption font-medium">
      {text}
    </span>
  );
}
```

---

- [ ] **Step 8.10 — Create `frontend/components/result/FeedbackWidget.tsx`**

Client Component. 6-state machine: `idle → positive/negative → expanded → submitted/error` (I6).

**Note on `helpful` field:** `handleVote` immediately transitions to `'expanded'`, so by the time `handleSubmit` runs `state` is `'expanded'`. Store the vote in a ref to preserve it. The corrected implementation below applies this fix directly.

```tsx
'use client';

import { useState, useRef } from 'react';
import { ThumbsUp, ThumbsDown, CheckCircle2, AlertTriangle } from 'lucide-react';
import { submitFeedback } from '@/lib/api';

// B10: profileId passed as prop — do NOT read from URL params
interface FeedbackWidgetProps {
  profileId: string;
}

type FeedbackState = 'idle' | 'positive' | 'negative' | 'expanded' | 'submitted' | 'error';

export default function FeedbackWidget({ profileId }: FeedbackWidgetProps) {
  const [state, setState] = useState<FeedbackState>('idle');
  const [comment, setComment] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  // Correction: track vote in a ref to preserve it after state transitions
  const voteRef = useRef<'positive' | 'negative' | null>(null);

  const handleVote = (vote: 'positive' | 'negative') => {
    voteRef.current = vote;
    setState('expanded');
  };

  const handleSubmit = async () => {
    setIsSubmitting(true);
    try {
      // I6: Catch API errors and set 'error' state
      await submitFeedback({
        profileId,
        helpful: voteRef.current === 'positive',
        comment,
      });
      setState('submitted');
    } catch {
      setState('error');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="mt-12 mb-8 text-center">
      {state === 'idle' && (
        <>
          <p className="text-body text-text-secondary mb-4">
            Luận giải này có ích cho bạn không?
          </p>
          <div className="flex justify-center gap-3">
            <button
              onClick={() => handleVote('positive')}
              className="flex items-center gap-2 px-4 py-2 border border-border rounded-[8px] text-body text-text-secondary hover:border-accent-border hover:text-text-primary transition-colors"
            >
              <ThumbsUp className="w-4 h-4" />
              Có
            </button>
            <button
              onClick={() => handleVote('negative')}
              className="flex items-center gap-2 px-4 py-2 border border-border rounded-[8px] text-body text-text-secondary hover:border-accent-border hover:text-text-primary transition-colors"
            >
              <ThumbsDown className="w-4 h-4" />
              Không
            </button>
          </div>
        </>
      )}

      {state === 'expanded' && (
        <>
          <p className="text-body-sm text-text-secondary mb-3">
            Cảm ơn! Bạn muốn chia sẻ thêm không?
          </p>
          <textarea
            rows={3}
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder="Chia sẻ suy nghĩ (không bắt buộc)..."
            className="w-full max-w-sm border border-border rounded-[8px] px-3 py-2 text-body text-text-primary bg-bg-surface resize-none focus:outline-none focus:border-accent-border transition-colors"
          />
          <button
            onClick={handleSubmit}
            disabled={isSubmitting}
            className="block w-full max-w-sm mx-auto mt-2 py-2 bg-accent text-white rounded-[8px] text-body font-medium hover:bg-accent/90 disabled:opacity-50 transition-colors"
          >
            {isSubmitting ? 'Đang gửi...' : 'Gửi phản hồi'}
          </button>
          <button
            onClick={() => setState('submitted')}
            className="block w-full text-sm text-text-tertiary mt-1 hover:text-text-secondary transition-colors"
          >
            Bỏ qua
          </button>
        </>
      )}

      {state === 'submitted' && (
        <div className="flex flex-col items-center gap-2">
          <CheckCircle2 className="w-6 h-6 text-alert-positive" />
          <p className="text-body text-text-secondary">Cảm ơn bạn đã phản hồi!</p>
        </div>
      )}

      {/* I6: Error state */}
      {state === 'error' && (
        <div className="flex flex-col items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-amber-500" />
          <p className="text-body-sm text-text-secondary">
            Gửi thất bại, vui lòng thử lại.
          </p>
          <button
            onClick={() => setState('expanded')}
            className="px-4 py-2 border border-border rounded-[8px] text-body text-text-secondary hover:border-accent-border transition-colors"
          >
            Thử lại
          </button>
        </div>
      )}
    </div>
  );
}
```

---

- [ ] **Step 8.11 — Create `frontend/components/result/ResultFooter.tsx`**

Server Component. Disclaimer + copyright.

```tsx
export default function ResultFooter() {
  return (
    <footer className="mt-8 pb-8 border-t border-border pt-6 text-center">
      <p className="text-caption text-text-tertiary max-w-[400px] mx-auto">
        Nội dung luận giải mang tính tham khảo dựa trên hệ thống Tử Vi Đẩu Số.
        Không phải lời khuyên chuyên nghiệp. Mọi quyết định cuối cùng là của bạn.
      </p>
      <p className="text-caption text-text-tertiary mt-2">© 2026 TuVi AI</p>
    </footer>
  );
}
```

---

- [ ] **Step 8.12 — Verify Task 8**

```
- [ ] /result/[valid-id] loads — no crash, sticky header visible
- [ ] /result/[invalid-id] returns 404 page
- [ ] ProfileHeaderCard: name, birth, menh, 3 pill tags render correctly
- [ ] OverviewChartCard: radar visible at ≥640px, bar visible at <640px (toggle DevTools)
- [ ] AIOverviewCard: renders summary text; shows animate-pulse skeleton when summary is null
- [ ] DimensionCardsGrid: 8 cards in 2-col grid (desktop), 1-col (mobile)
- [ ] DimensionCard van_menh: no alert badges section rendered
- [ ] DimensionCard (non-van_menh): positive badges show text-emerald-700, negative show text-amber-700
- [ ] Score bar: score 0 → 50% width; score -20 → 0%; score +20 → 100%
- [ ] Clicking any DimensionCard navigates to /result/[id]/[dimensionKey]
- [ ] ShareButton: clicking copies URL; toast shows "Đã copy link!"
- [ ] FeedbackWidget idle: two buttons (Có / Không)
- [ ] FeedbackWidget after vote: textarea + "Gửi phản hồi" + "Bỏ qua"
- [ ] FeedbackWidget submitted: CheckCircle2 + "Cảm ơn bạn đã phản hồi!"
- [ ] FeedbackWidget error: AlertTriangle + "Thử lại" → returns to expanded
- [ ] ResultFooter: disclaimer + © 2026 TuVi AI
- [ ] B9 guard: profile.dimensions missing a key → that card is skipped, no crash
```

- [ ] **Step 8.13 — Commit Task 8**

```bash
git add frontend/app/result/[id] frontend/components/result
git commit -m "feat: add result overview page with profile card, charts, dimension grid, and feedback"
```

---

# Task 9: Dimension Detail Page

**Goal:** Build the `/result/[id]/[dimension]` page showing a single dimension's 3 charts, alerts, AI interpretation in markdown, and prev/next navigation.

**Files to create:**
- `frontend/app/result/[id]/[dimension]/page.tsx`
- `frontend/components/detail/DetailHeader.tsx`
- `frontend/components/detail/DimensionTitleBlock.tsx`
- `frontend/components/detail/AlertsSummarySection.tsx`
- `frontend/components/detail/AIInterpretationSection.tsx`
- `frontend/components/detail/DimensionNavigation.tsx`

**Install dependencies (if not already done in Task 7):**

```bash
npm install react-markdown rehype-raw
```

---

- [ ] **Step 9.1 — Create `frontend/app/result/[id]/[dimension]/page.tsx`**

Server Component. Validates dimension key, applies B9 guard, renders layout.

```tsx
import { notFound } from 'next/navigation';
import { getProfile } from '@/lib/api';
import { ProfileData, DimensionData } from '@/lib/types';
import { DIMENSION_ORDER, DimensionKey } from '@/lib/constants';
import ResultHeader from '@/components/result/ResultHeader';
import ResultFooter from '@/components/result/ResultFooter';
import DetailHeader from '@/components/detail/DetailHeader';
import DimensionTitleBlock from '@/components/detail/DimensionTitleBlock';
import ChartCard from '@/components/charts/ChartCard';
import LifetimeChart from '@/components/charts/LifetimeChart';
import DecadeChart from '@/components/charts/DecadeChart';
import MonthlyChart from '@/components/charts/MonthlyChart';
import AlertsSummarySection from '@/components/detail/AlertsSummarySection';
import AIInterpretationSection from '@/components/detail/AIInterpretationSection';
import DimensionNavigation from '@/components/detail/DimensionNavigation';

export default async function DimensionDetailPage({
  params,
}: {
  params: { id: string; dimension: string };
}) {
  // Validate dimension key
  if (!DIMENSION_ORDER.includes(params.dimension as DimensionKey)) {
    notFound();
  }

  let profile: ProfileData;
  try {
    profile = await getProfile(params.id);
  } catch {
    notFound();
  }

  const dimensionKey = params.dimension as DimensionKey;
  const dimensionData = profile.dimensions[dimensionKey];

  // B9: Defensive guard — missing dimension data → 404
  if (!dimensionData) notFound();

  return (
    <div className="bg-bg-primary min-h-screen">
      <DetailHeader profileId={profile.profileId} />

      <main className="max-w-3xl mx-auto px-4 pb-8">
        <DimensionTitleBlock
          dimensionKey={dimensionKey}
          dimensionData={dimensionData}
          profileName={profile.name ?? null}
        />

        {/* Charts */}
        <ChartCard title="Vận trình trọn đời" subtitle="12 mốc • Cả cuộc đời">
          <LifetimeChart
            scores={dimensionData.scores.lifetime}
            alerts={dimensionData.alerts}
          />
        </ChartCard>

        <ChartCard title="Đại vận 10 năm" subtitle="10 mốc • Thập niên hiện tại">
          <DecadeChart
            scores={dimensionData.scores.decade}
            alerts={dimensionData.alerts}
          />
        </ChartCard>

        <ChartCard title="Tiểu vận hàng tháng" subtitle="13 tháng • Năm hiện tại">
          <MonthlyChart
            scores={dimensionData.scores.monthly}
            alerts={dimensionData.alerts}
          />
        </ChartCard>

        <AlertsSummarySection
          dimensionKey={dimensionKey}
          alerts={dimensionData.alerts}
        />

        <AIInterpretationSection
          dimensionKey={dimensionKey}
          interpretation={dimensionData.interpretation ?? null}
        />

        <DimensionNavigation
          profileId={profile.profileId}
          currentKey={dimensionKey}
        />

        <ResultFooter />
      </main>
    </div>
  );
}
```

---

- [ ] **Step 9.2 — Create `frontend/components/detail/DetailHeader.tsx`**

Server Component. Back link to overview + `ShareButton` island.

```tsx
import Link from 'next/link';
import { ChevronLeft } from 'lucide-react';
import ShareButton from '@/components/result/ShareButton';

interface Props {
  profileId: string;
}

export default function DetailHeader({ profileId }: Props) {
  return (
    <header className="sticky top-0 z-40 h-14 bg-bg-surface border-b border-border">
      <div className="max-w-3xl mx-auto px-4 h-full flex items-center justify-between">
        <Link
          href={`/result/${profileId}`}
          className="flex items-center gap-1.5 text-body text-text-secondary hover:text-text-primary transition-colors"
        >
          <ChevronLeft className="w-4 h-4" />
          Tổng quan
        </Link>
        <ShareButton />
      </div>
    </header>
  );
}
```

---

- [ ] **Step 9.3 — Create `frontend/components/detail/DimensionTitleBlock.tsx`**

Server Component. Icon, label, score badge.

```tsx
import { DimensionData } from '@/lib/types';
import { DimensionKey, DIMENSION_LABELS, DIMENSION_ICONS } from '@/lib/constants';

interface Props {
  dimensionKey: DimensionKey;
  dimensionData: DimensionData;
  profileName: string | null;
}

export default function DimensionTitleBlock({ dimensionKey, dimensionData, profileName }: Props) {
  const Icon = DIMENSION_ICONS[dimensionKey];
  const label = DIMENSION_LABELS[dimensionKey];

  return (
    <div className="mt-[56px] px-0 pt-6 pb-4">
      <div className="flex items-center gap-3">
        {/* Icon block */}
        <div className="w-12 h-12 rounded-[12px] bg-accent-light flex items-center justify-center flex-shrink-0">
          <Icon className="w-6 h-6 text-accent" />
        </div>

        {/* Text block */}
        <div>
          <h1 className="text-heading-md font-bold text-text-primary">{label}</h1>
          <p className="text-body-sm text-text-secondary mt-0.5">
            {profileName ? `${profileName} — ` : ''}
            {label}
          </p>
          <p className="text-body-sm text-text-secondary mt-0.5">
            Tổng điểm:{' '}
            <span className="text-mono font-medium text-text-primary">
              {dimensionData.summaryScore.toFixed(2)}
            </span>
          </p>
        </div>
      </div>
    </div>
  );
}
```

---

- [ ] **Step 9.4 — Create `frontend/components/detail/AlertsSummarySection.tsx`**

Server Component. Hidden entirely for `van_menh`. Alert cards sorted: positives first. Level-50 uses `bg-amber-100 text-amber-800` (I5, NOT red).

```tsx
import { TrendingUp, TrendingDown } from 'lucide-react';
import { Alert } from '@/lib/types';
import { DimensionKey } from '@/lib/constants';

interface Props {
  dimensionKey: DimensionKey;
  alerts: Alert[];
}

function LevelBadge({ level }: { level: number }) {
  if (level >= 50) {
    // I5: Use amber-100/amber-800 for level-50 (NOT red — red implies error, amber stays in cautionary palette)
    return (
      <span className="text-caption rounded-full px-1.5 py-0.5 ml-2 inline-block bg-amber-100 text-amber-800 border border-amber-300 font-semibold">
        Mức cao
      </span>
    );
  }
  return (
    <span className="text-caption rounded-full px-1.5 py-0.5 ml-2 inline-block bg-amber-50 text-amber-700 border border-amber-200">
      Đáng chú ý
    </span>
  );
}

export default function AlertsSummarySection({ dimensionKey, alerts }: Props) {
  // Hidden entirely for van_menh
  if (dimensionKey === 'van_menh') return null;

  // Sort: positives first, then negatives
  const sorted = [...alerts].sort((a, b) => {
    if (a.type === b.type) return 0;
    return a.type === 'positive' ? -1 : 1;
  });

  return (
    <section className="mt-6">
      <h2 className="text-label font-semibold text-text-primary mb-3">
        Các mốc cần chú ý
      </h2>

      {sorted.length === 0 ? (
        <p className="text-body-sm text-text-tertiary">
          Không có mốc đặc biệt trong giai đoạn này.
        </p>
      ) : (
        <div>
          {sorted.map((alert, i) => {
            const isPositive = alert.type === 'positive';
            return (
              <div
                key={i}
                className={`rounded-[8px] p-3 mb-2 flex items-start gap-2.5 border ${
                  isPositive
                    ? 'bg-alert-positive-bg border-alert-positive-bdr'
                    : 'bg-alert-negative-bg border-alert-negative-bdr'
                }`}
              >
                {isPositive ? (
                  <TrendingUp className="w-4 h-4 text-alert-positive mt-0.5 flex-shrink-0" />
                ) : (
                  <TrendingDown className="w-4 h-4 text-alert-negative mt-0.5 flex-shrink-0" />
                )}

                <div>
                  <p className="text-label font-medium text-text-primary">
                    {alert.period}
                    <LevelBadge level={alert.level} />
                  </p>
                  {alert.tag && (
                    <p className="text-body-sm text-text-secondary mt-0.5">{alert.tag}</p>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </section>
  );
}
```

---

- [ ] **Step 9.5 — Create `frontend/components/detail/AIInterpretationSection.tsx`**

Server Component — no `'use client'` (react-markdown v9 is pure ESM, works server-side). Uses `preprocessInterpretation` + `rehype-raw` to render styled ▲/▼ characters. Van_menh null → placeholder card.

```tsx
import ReactMarkdown from 'react-markdown';
import rehypeRaw from 'rehype-raw';
import { Sparkles, Clock } from 'lucide-react';
import { DimensionKey } from '@/lib/constants';
import { preprocessInterpretation } from '@/lib/utils';

interface Props {
  dimensionKey: DimensionKey;
  interpretation: string | null;
}

export default function AIInterpretationSection({ dimensionKey, interpretation }: Props) {
  return (
    <section className="mt-6">
      {/* Header */}
      <div className="flex items-center gap-2 mb-4">
        <Sparkles className="w-[18px] h-[18px] text-accent flex-shrink-0" />
        <h2 className="text-label font-semibold text-text-primary">AI Luận Giải</h2>
        <div className="flex-1 h-px bg-border ml-2" />
      </div>

      {/* van_menh: null interpretation → placeholder */}
      {dimensionKey === 'van_menh' && !interpretation ? (
        <div className="bg-bg-subtle border border-border rounded-[12px] p-6 text-center">
          <Clock className="w-6 h-6 text-text-tertiary mx-auto mb-3" />
          <p className="text-body text-text-secondary">
            Luận giải Vận mệnh đang được cập nhật.
          </p>
          <p className="text-body-sm text-text-tertiary mt-1">
            Vận mệnh là bức tranh tổng thể — xem từng lĩnh vực để hiểu chi tiết.
          </p>
        </div>
      ) : interpretation ? (
        <ReactMarkdown
          rehypePlugins={[rehypeRaw]}
          components={{
            h2: ({ children }) => (
              <h2 className="text-heading-sm font-semibold text-text-primary mt-6 mb-2">
                {children}
              </h2>
            ),
            h3: ({ children }) => (
              <h3 className="text-label font-semibold text-text-primary mt-4 mb-1.5">
                {children}
              </h3>
            ),
            p: ({ children }) => (
              <p className="text-body text-text-secondary leading-relaxed mb-3">
                {children}
              </p>
            ),
            ul: ({ children }) => (
              <ul className="list-disc pl-5 text-body text-text-secondary space-y-1">
                {children}
              </ul>
            ),
            li: ({ children }) => (
              <li className="leading-relaxed">{children}</li>
            ),
            strong: ({ children }) => (
              <strong className="font-semibold text-text-primary">{children}</strong>
            ),
            em: ({ children }) => (
              <em className="italic text-text-secondary">{children}</em>
            ),
            hr: () => <hr className="border-border my-6" />,
            blockquote: ({ children }) => (
              <blockquote className="border-l-2 border-accent pl-4 text-text-secondary italic">
                {children}
              </blockquote>
            ),
          }}
        >
          {preprocessInterpretation(interpretation)}
        </ReactMarkdown>
      ) : (
        <p className="text-body-sm text-text-tertiary">
          Không có nội dung luận giải.
        </p>
      )}
    </section>
  );
}
```

---

- [ ] **Step 9.6 — Create `frontend/components/detail/DimensionNavigation.tsx`**

Server Component. Prev/next links using `DIMENSION_ORDER`. First dimension has no prev; last has no next.

```tsx
import Link from 'next/link';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { DIMENSION_ORDER, DimensionKey, DIMENSION_LABELS } from '@/lib/constants';

interface Props {
  profileId: string;
  currentKey: DimensionKey;
}

export default function DimensionNavigation({ profileId, currentKey }: Props) {
  const currentIndex = DIMENSION_ORDER.indexOf(currentKey);
  const prevKey = currentIndex > 0 ? DIMENSION_ORDER[currentIndex - 1] : null;
  const nextKey = currentIndex < DIMENSION_ORDER.length - 1 ? DIMENSION_ORDER[currentIndex + 1] : null;

  return (
    <nav className="mt-10 border-t border-border pt-6 pb-4">
      <div className="flex justify-between items-center gap-4 max-w-3xl mx-auto">
        {/* Prev */}
        <div className="flex-1">
          {prevKey ? (
            <Link
              href={`/result/${profileId}/${prevKey}`}
              className="flex items-center gap-2 text-body text-text-secondary hover:text-text-primary transition-colors"
            >
              <ChevronLeft className="w-4 h-4 flex-shrink-0" />
              <div>
                <p className="text-caption text-text-tertiary">Trước</p>
                <p className="text-body-sm font-medium text-text-primary">
                  {DIMENSION_LABELS[prevKey]}
                </p>
              </div>
            </Link>
          ) : (
            <div />
          )}
        </div>

        {/* Next */}
        <div className="flex-1 flex justify-end">
          {nextKey ? (
            <Link
              href={`/result/${profileId}/${nextKey}`}
              className="flex items-center gap-2 text-body text-text-secondary hover:text-text-primary transition-colors text-right"
            >
              <div>
                <p className="text-caption text-text-tertiary">Tiếp theo</p>
                <p className="text-body-sm font-medium text-text-primary">
                  {DIMENSION_LABELS[nextKey]}
                </p>
              </div>
              <ChevronRight className="w-4 h-4 flex-shrink-0" />
            </Link>
          ) : (
            <div />
          )}
        </div>
      </div>
    </nav>
  );
}
```

---

- [ ] **Step 9.7 — Verify Task 9**

```
- [ ] /result/[id]/su_nghiep loads — no crash
- [ ] /result/[id]/invalid-key returns 404
- [ ] /result/[id]/van_menh loads — AlertsSummarySection renders null
- [ ] /result/[id]/van_menh with null interpretation → placeholder card with Clock icon
- [ ] DetailHeader: "← Tổng quan" link navigates back to /result/[id]
- [ ] DimensionTitleBlock: correct icon, label, score displayed
- [ ] 3 ChartCard wrappers rendered — each has title, subtitle, legend (Dương/Âm/TB)
- [ ] LifetimeChart: 12 X-axis points, TB line is dashed, alert dots appear on TB line only
- [ ] DecadeChart: X-axis shows integer years via String(label)
- [ ] MonthlyChart: "Th.1/2026" displays as "Th.1" on axis; full label in tooltip
- [ ] MonthlyChart: duplicate-month note visible below chart
- [ ] AlertsSummarySection: positives listed before negatives
- [ ] AlertsSummarySection level-50: bg-amber-100 text-amber-800 (not red)
- [ ] AlertsSummarySection level-30: bg-amber-50 text-amber-700
- [ ] AIInterpretationSection: markdown renders with correct heading/paragraph styles
- [ ] ▲ renders as text-emerald-600, ▼ renders as text-amber-600 (via preprocessInterpretation + rehype-raw)
- [ ] DimensionNavigation on su_nghiep: no "Trước" link, has "Tiếp theo → Tiền bạc"
- [ ] DimensionNavigation on van_menh: has "Trước → Con cái", no "Tiếp theo" link
- [ ] DimensionNavigation on middle dimension: both prev and next visible
- [ ] No 'use client' in DetailHeader, DimensionTitleBlock, AlertsSummarySection,
      AIInterpretationSection, DimensionNavigation (all Server Components)
- [ ] B9 guard: if dimensionData is undefined → notFound() fires
```

- [ ] **Step 9.8 — Commit Task 9**

```bash
git add frontend/app/result/[id]/[dimension] frontend/components/detail
git commit -m "feat: add dimension detail page with charts, alerts, AI interpretation, and navigation"
```

---

## Cross-Task Notes

**`lib/types.ts` assumptions** (must match what was built in Tasks 1–5):
- `ProfileData.dimensions` is `Record<DimensionKey, DimensionData>`
- `DimensionData.scores` has `.lifetime`, `.decade`, `.monthly` — each a `DimensionScores` with `.labels`, `.duong`, `.am`, `.tb`
- `DimensionData.alerts` is `Alert[]`; `Alert` has `.type`, `.period`, `.level`, `.tag`
- `ProfileData.overview.summary` is `string | null`
- `ProfileData.metadata` has `.nam`, `.cungMenh`, `.menh`, `.cuc`, `.amDuong`
- `DimensionKey` is a union type exported from `lib/constants.ts` alongside `DIMENSION_ORDER`

**`lib/constants.ts` assumptions:**
- `DIMENSION_ORDER` is an array of `DimensionKey` values in order: `su_nghiep, tien_bac, hon_nhan, suc_khoe, dat_dai, hoc_tap, con_cai, van_menh`
- `DIMENSION_LABELS` maps each key to a Vietnamese display name
- `DIMENSION_ICONS` maps each key to a Lucide icon component
- `FUN_FACTS` is a string array (add if missing)

**Tailwind custom tokens used** (must be defined in `tailwind.config.ts` / `tokens.ts`):
- Colors: `bg-accent`, `text-accent`, `bg-accent-light`, `border-accent-border`, `bg-bg-primary`, `bg-bg-surface`, `bg-bg-subtle`, `text-text-primary`, `text-text-secondary`, `text-text-tertiary`, `border-border`
- Alert tokens: `bg-alert-positive-bg`, `border-alert-positive-bdr`, `text-alert-positive`, `bg-alert-negative-bg`, `border-alert-negative-bdr`, `text-alert-negative`
- Chart tokens: `bg-chart-duong`, `bg-chart-am`, `bg-chart-tb`
