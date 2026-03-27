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

interface DecadeChartProps {
  scores: DimensionScores;
  alerts: Alert[];
  height?: number;
}

// I4: CustomDot ONLY on TB line
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const CustomDot = (props: any) => {
  const { cx, cy, payload } = props;
  if (!payload.alert) return <g />;

  const isPositive = payload.alert.type === 'positive';
  const color = isPositive ? '#10B981' : '#F59E0B';

  return (
    <g>
      <circle cx={cx} cy={cy} r={5} fill={color} />
      <text x={cx} y={cy - 10} textAnchor="middle" fontSize={10} fill={color}>
        {isPositive ? '\u25B2' : '\u25BC'}
      </text>
    </g>
  );
};

export default function DecadeChart({ scores, alerts, height = 240 }: DecadeChartProps) {
  const isMobile = useIsMobile();

  const chartData = scores.labels.map((label, i) => ({
    period: String(label),
    duong: scores.duong[i],
    am: scores.am[i],
    tb: scores.tb[i],
    alert: alerts.find((a) => a.period === String(label)) ?? null,
  }));

  return (
    <figure aria-label="Biểu đồ điểm số 10 năm">
      <figcaption className="sr-only">
        Biểu đồ đường thể hiện điểm Dương, Âm, Trung bình theo từng năm trong thập kỷ.
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
          formatter={(value, name) => [Number(value).toFixed(2), name]}
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
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
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
    </figure>
  );
}
