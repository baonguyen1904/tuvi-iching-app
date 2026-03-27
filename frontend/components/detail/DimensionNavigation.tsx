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
