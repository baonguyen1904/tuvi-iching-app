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
