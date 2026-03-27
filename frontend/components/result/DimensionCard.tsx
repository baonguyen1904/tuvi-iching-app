import Link from 'next/link';
import { ChevronRight } from 'lucide-react';
import { DimensionData } from '@/lib/types';
import { DimensionKey, DIMENSION_LABELS } from '@/lib/constants';
import { DIMENSION_ICON_COMPONENTS } from '@/lib/dimension-icons';
import AlertBadge from './AlertBadge';

interface DimensionCardProps {
  dimensionKey: DimensionKey;
  data: DimensionData;
  profileId: string;
}

export default function DimensionCard({ dimensionKey, data, profileId }: DimensionCardProps) {
  const summaryScore = data.summaryScore;
  // Score normalization: ~-20 to +20 -> 0-100%
  const barWidth = Math.max(0, Math.min(100, ((summaryScore + 20) / 40) * 100));

  const positiveAlerts = data.alerts?.filter((a) => a.type === 'positive') ?? [];
  const negativeAlerts = data.alerts?.filter((a) => a.type === 'negative') ?? [];

  const Icon = DIMENSION_ICON_COMPONENTS[dimensionKey];
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
