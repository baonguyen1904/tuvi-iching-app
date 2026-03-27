export default function ResultLoading() {
  return (
    <main
      id="main-content"
      className="min-h-screen bg-bg-primary px-4 py-8"
      role="status"
      aria-live="polite"
      aria-label="Đang tải kết quả..."
    >
      <div className="max-w-3xl mx-auto space-y-6">

        {/* Profile header skeleton */}
        <div className="bg-bg-surface rounded-[12px] border border-border shadow-md p-4 md:p-6 animate-pulse">
          <div className="flex items-start gap-4">
            <div className="w-12 h-12 rounded-full bg-bg-subtle flex-shrink-0" />
            <div className="flex-1 space-y-2">
              <div className="h-5 bg-bg-subtle rounded w-1/3" />
              <div className="h-4 bg-bg-subtle rounded w-1/2" />
              <div className="h-3 bg-bg-subtle rounded w-2/3" />
            </div>
          </div>
        </div>

        {/* Overview chart skeleton */}
        <div className="bg-bg-surface rounded-[12px] border border-border shadow-md p-4 md:p-6 animate-pulse">
          <div className="h-5 bg-bg-subtle rounded w-1/4 mb-4" />
          <div className="w-full h-64 bg-bg-subtle rounded-lg" />
        </div>

        {/* AI overview text skeleton */}
        <div className="bg-bg-surface rounded-[12px] border border-border shadow-md p-4 md:p-6 animate-pulse space-y-2">
          <div className="h-4 bg-bg-subtle rounded w-full" />
          <div className="h-4 bg-bg-subtle rounded w-5/6" />
          <div className="h-4 bg-bg-subtle rounded w-4/6" />
          <div className="h-4 bg-bg-subtle rounded w-5/6" />
          <div className="h-4 bg-bg-subtle rounded w-3/6" />
        </div>

        {/* 8 dimension cards grid skeleton */}
        <div>
          <div className="h-5 bg-bg-subtle rounded w-1/3 mb-4 animate-pulse" />
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {Array.from({ length: 8 }).map((_, i) => (
              <div
                key={i}
                className="bg-bg-surface rounded-[12px] border border-border shadow-md p-4 animate-pulse space-y-3"
              >
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg bg-bg-subtle" />
                  <div className="h-4 bg-bg-subtle rounded w-1/3" />
                </div>
                <div className="h-2 bg-bg-subtle rounded-full w-full" />
                <div className="h-3 bg-bg-subtle rounded w-2/3" />
              </div>
            ))}
          </div>
        </div>

      </div>
    </main>
  );
}
