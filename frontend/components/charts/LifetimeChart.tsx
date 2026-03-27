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
import { useIsMobile } from '@/lib/hooks';
import { DimensionScores, Alert } from '@/lib/types';
import { CHART_COLORS, CHART_DEFAULTS, tooltipStyle, axisStyle } from './chartConfig';

interface LifetimeChartProps {
  scores: DimensionScores;
  alerts: Alert[];
  height?: number;
}

// I4: CustomDot renders ONLY on TB line — alert markers for positive and negative
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const CustomDot = (props: any) => {
  const { cx, cy, payload } = props;
  if (!payload.alert) return <g />;

  const isPositive = payload.alert.type === 'positive';
  const color = isPositive ? '#10B981' : '#F59E0B';
  const symbol = isPositive ? '\u25B2' : '\u25BC';

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
    period: String(label),
    duong: scores.duong[i],
    am: scores.am[i],
    tb: scores.tb[i],
    alert: alerts.find((a) => a.period === String(label)) ?? null,
  }));

  return (
    <figure aria-label="Biểu đồ điểm số trọn đời">
      <figcaption className="sr-only">
        Biểu đồ đường thể hiện điểm Dương, Âm, Trung bình theo độ tuổi.
      </figcaption>
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
          formatter={(value, name) => [Number(value).toFixed(2), name]}
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
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          dot={(props: any) => <CustomDot {...props} />}
          activeDot={{ r: 4, fill: CHART_COLORS.tb }}
          animationDuration={CHART_DEFAULTS.animationDuration}
        />

        {/* Am line — no custom dots */}
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

        {/* Duong line — no custom dots */}
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
    </figure>
  );
}
