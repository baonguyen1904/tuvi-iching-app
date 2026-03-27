import { notFound } from 'next/navigation';
import { getProfile } from '@/lib/api';
import { ProfileData } from '@/lib/types';
import ResultHeader from '@/components/result/ResultHeader';
import ProfileHeaderCard from '@/components/result/ProfileHeaderCard';
import OverviewChartCard from '@/components/result/OverviewChartCard';
import AIOverviewCard from '@/components/result/AIOverviewCard';
import DimensionCardsGrid from '@/components/result/DimensionCardsGrid';
import FeedbackWidget from '@/components/result/FeedbackWidget';
import ResultFooter from '@/components/result/ResultFooter';

export default async function ResultPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;

  let profile: ProfileData;

  try {
    profile = await getProfile(id);
  } catch {
    notFound();
  }

  if (!profile) notFound();

  return (
    <div className="bg-bg-primary min-h-screen">
      <ResultHeader profileId={profile.profileId} />

      <main id="main-content" className="max-w-3xl mx-auto px-4 mt-[56px] pb-8">
        <ProfileHeaderCard profile={profile} />
        <OverviewChartCard dimensions={profile.dimensions} />
        <AIOverviewCard summary={profile.overview?.summary ?? null} />
        <DimensionCardsGrid profile={profile} />
        <FeedbackWidget profileId={profile.profileId} />
        <ResultFooter />
      </main>
    </div>
  );
}
