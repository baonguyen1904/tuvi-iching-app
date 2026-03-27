import { DimensionData } from '@/lib/types';
import { DimensionKey, DIMENSION_LABELS } from '@/lib/constants';
import { DIMENSION_ICON_COMPONENTS } from '@/lib/dimension-icons';

interface Props {
  dimensionKey: DimensionKey;
  dimensionData: DimensionData;
  profileName: string | null;
}

export default function DimensionTitleBlock({ dimensionKey, dimensionData, profileName }: Props) {
  const Icon = DIMENSION_ICON_COMPONENTS[dimensionKey];
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
