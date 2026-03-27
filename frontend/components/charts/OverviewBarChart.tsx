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

  // M5: Responsive height — 8 bars x 40px + 32px padding
  const chartHeight = Math.max(280, barData.length * 40 + 32);

  return (
    <figure aria-label="Biểu đồ tổng quan 8 lĩnh vực">
      <figcaption className="sr-only">
        Biểu đồ cột ngang thể hiện điểm số 8 lĩnh vực: Sự nghiệp, Tiền bạc, Hôn nhân, Sức khỏe, Đất đai, Học tập, Con cái, Vận mệnh.
      </figcaption>
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
          formatter={(v) => [`${Number(v).toFixed(0)}/100`, 'Điểm']}
        />

        <Bar dataKey="score" fill="#2563EB" radius={[0, 4, 4, 0]} barSize={16} />
      </BarChart>
    </ResponsiveContainer>
    </figure>
  );
}
