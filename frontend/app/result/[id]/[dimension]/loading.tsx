export default function DimensionDetailLoading() {
  return (
    <main
      id="main-content"
      className="min-h-screen bg-bg-primary px-4 py-8"
      role="status"
      aria-live="polite"
      aria-label="Đang tải lĩnh vực..."
    >
      <div className="max-w-3xl mx-auto space-y-6">

        {/* Back nav skeleton */}
        <div className="h-4 bg-bg-subtle rounded w-24 animate-pulse" />

        {/* Dimension header skeleton */}
        <div className="bg-bg-surface rounded-[12px] border border-border shadow-md p-4 md:p-6 animate-pulse">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 rounded-lg bg-bg-subtle" />
            <div className="h-6 bg-bg-subtle rounded w-1/4" />
          </div>
          {/* Summary score bar */}
          <div className="h-3 bg-bg-subtle rounded-full w-full mb-2" />
          <div className="h-3 bg-bg-subtle rounded w-1/6 ml-auto" />
        </div>

        {/* Chart area skeleton */}
        <div className="bg-bg-surface rounded-[12px] border border-border shadow-md p-4 md:p-6 animate-pulse">
          {/* Tab bar */}
          <div className="flex gap-2 mb-4">
            <div className="h-8 bg-bg-subtle rounded-md w-20" />
            <div className="h-8 bg-bg-subtle rounded-md w-20" />
            <div className="h-8 bg-bg-subtle rounded-md w-20" />
          </div>
          {/* Chart */}
          <div className="w-full h-48 bg-bg-subtle rounded-lg" />
        </div>

        {/* Alert badges skeleton */}
        <div className="flex flex-wrap gap-2 animate-pulse">
          <div className="h-7 bg-alert-positive-bg border border-alert-positive-bdr rounded-full w-32" />
          <div className="h-7 bg-alert-negative-bg border border-alert-negative-bdr rounded-full w-36" />
          <div className="h-7 bg-alert-positive-bg border border-alert-positive-bdr rounded-full w-28" />
        </div>

        {/* AI interpretation text skeleton */}
        <div className="bg-bg-surface rounded-[12px] border border-border shadow-md p-4 md:p-6 animate-pulse space-y-2">
          <div className="h-4 bg-bg-subtle rounded w-full" />
          <div className="h-4 bg-bg-subtle rounded w-5/6" />
          <div className="h-4 bg-bg-subtle rounded w-full" />
          <div className="h-4 bg-bg-subtle rounded w-4/6" />
        </div>

        {/* Prev / Next navigation skeleton */}
        <div className="flex justify-between items-center animate-pulse">
          <div className="h-10 bg-bg-subtle rounded-md w-28" />
          <div className="h-10 bg-bg-subtle rounded-md w-28" />
        </div>

      </div>
    </main>
  );
}
