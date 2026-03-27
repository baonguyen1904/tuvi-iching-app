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

// Score normalization: summaryScore (~-20 to +20) -> 0-100
export const normalize = (score: number): number =>
  Math.max(0, Math.min(100, ((score + 20) / 40) * 100));

export default function OverviewRadarChart({ dimensions, height = 280 }: OverviewRadarChartProps) {
  const radarData = DIMENSION_ORDER.map((key) => ({
    dimension: DIMENSION_LABELS[key],
    value: normalize(dimensions[key]?.summaryScore ?? 0),
    fullMark: 100,
  }));

  return (
    <figure aria-label="Biểu đồ tổng quan 8 lĩnh vực">
      <figcaption className="sr-only">
        Biểu đồ radar thể hiện điểm số 8 lĩnh vực: Sự nghiệp, Tiền bạc, Hôn nhân, Sức khỏe, Đất đai, Học tập, Con cái, Vận mệnh.
      </figcaption>
    <ResponsiveContainer width="100%" height={height}>
      <RadarChart cx="50%" cy="50%" outerRadius="75%" data={radarData}>
        <PolarGrid stroke="#E5E7EB" />

        {/* M6: At 640px the radar labels can overlap for longer names — truncate >6 chars */}
        <PolarAngleAxis
          dataKey="dimension"
          tick={{ fill: '#6B7280', fontSize: 10 }}
          tickFormatter={(label: string) =>
            label.length > 6 ? label.slice(0, 6) + '\u2026' : label
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
          formatter={(v) => [`${Number(v).toFixed(0)}/100`, 'Điểm']}
        />
      </RadarChart>
    </ResponsiveContainer>
    </figure>
  );
}
