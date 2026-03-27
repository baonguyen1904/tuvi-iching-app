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
