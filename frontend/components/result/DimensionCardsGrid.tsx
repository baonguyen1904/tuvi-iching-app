import { ProfileData } from '@/lib/types';
import { DIMENSION_ORDER } from '@/lib/constants';
import DimensionCard from './DimensionCard';

interface Props {
  profile: ProfileData;
}

export default function DimensionCardsGrid({ profile }: Props) {
  return (
    <section className="mt-8">
      <h2 className="text-heading-sm font-semibold text-text-primary mb-4">
        Xem chi tiết từng lĩnh vực
      </h2>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
        {DIMENSION_ORDER.map((key) => {
          const data = profile.dimensions[key];
          // B9: Guard — skip if dimension data is missing (protects against partial API response)
          if (!data) return null;
          return (
            <DimensionCard
              key={key}
              dimensionKey={key}
              data={data}
              profileId={profile.profileId}
            />
          );
        })}
      </div>
    </section>
  );
}
