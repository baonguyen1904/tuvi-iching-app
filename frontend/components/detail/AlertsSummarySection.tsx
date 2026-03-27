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
