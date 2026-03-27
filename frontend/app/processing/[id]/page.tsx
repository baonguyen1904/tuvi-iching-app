import ProcessingScreen from '@/components/processing/ProcessingScreen';

export default async function ProcessingPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  return <ProcessingScreen profileId={id} />;
}
