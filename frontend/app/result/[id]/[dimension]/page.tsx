import { notFound } from 'next/navigation';
import { getProfile } from '@/lib/api';
import { ProfileData } from '@/lib/types';
import { DIMENSION_ORDER, DimensionKey } from '@/lib/constants';
import DetailHeader from '@/components/detail/DetailHeader';
import DimensionTitleBlock from '@/components/detail/DimensionTitleBlock';
import ChartCard from '@/components/charts/ChartCard';
import LifetimeChart from '@/components/charts/LifetimeChart';
import DecadeChart from '@/components/charts/DecadeChart';
import MonthlyChart from '@/components/charts/MonthlyChart';
import AlertsSummarySection from '@/components/detail/AlertsSummarySection';
import AIInterpretationSection from '@/components/detail/AIInterpretationSection';
import DimensionNavigation from '@/components/detail/DimensionNavigation';
import ResultFooter from '@/components/result/ResultFooter';

export default async function DimensionDetailPage({
  params,
}: {
  params: Promise<{ id: string; dimension: string }>;
}) {
  const { id, dimension } = await params;

  // Validate dimension key
  if (!DIMENSION_ORDER.includes(dimension as DimensionKey)) {
    notFound();
  }

  let profile: ProfileData;
  try {
    profile = await getProfile(id);
  } catch {
    notFound();
  }

  const dimensionKey = dimension as DimensionKey;
  const dimensionData = profile.dimensions[dimensionKey];

  // B9: Defensive guard — missing dimension data -> 404
  if (!dimensionData) notFound();

  return (
    <div className="bg-bg-primary min-h-screen">
      <DetailHeader profileId={profile.profileId} />

      <main className="max-w-3xl mx-auto px-4 pb-8">
        <DimensionTitleBlock
          dimensionKey={dimensionKey}
          dimensionData={dimensionData}
          profileName={profile.name ?? null}
        />

        {/* Charts */}
        <ChartCard title="Vận trình trọn đời" subtitle="12 mốc &bull; Cả cuộc đời">
          <LifetimeChart
            scores={dimensionData.lifetime}
            alerts={dimensionData.alerts}
          />
        </ChartCard>

        <ChartCard title="Đại vận 10 năm" subtitle="10 mốc &bull; Thập niên hiện tại">
          <DecadeChart
            scores={dimensionData.decade}
            alerts={dimensionData.alerts}
          />
        </ChartCard>

        <ChartCard title="Tiểu vận hàng tháng" subtitle="13 tháng &bull; Năm hiện tại">
          <MonthlyChart
            scores={dimensionData.monthly}
            alerts={dimensionData.alerts}
          />
        </ChartCard>

        <AlertsSummarySection
          dimensionKey={dimensionKey}
          alerts={dimensionData.alerts}
        />

        <AIInterpretationSection
          dimensionKey={dimensionKey}
          interpretation={dimensionData.interpretation ?? null}
        />

        <DimensionNavigation
          profileId={profile.profileId}
          currentKey={dimensionKey}
        />

        <ResultFooter />
      </main>
    </div>
  );
}
