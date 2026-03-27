interface ChartSkeletonProps {
  height?: number;
}

export default function ChartSkeleton({ height = 240 }: ChartSkeletonProps) {
  return (
    <div
      className="w-full bg-bg-subtle rounded-[8px] animate-pulse"
      style={{ height }}
    />
  );
}
