export default function ProcessingLoading() {
  return (
    <main
      id="main-content"
      className="min-h-screen bg-bg-primary flex items-center justify-center px-4"
      role="status"
      aria-live="polite"
      aria-label="Đang chuẩn bị..."
    >
      <div className="text-center">
        {/* Pulsing dots -- matches ProcessingAnimation (I8) */}
        <div className="flex items-center justify-center gap-2 mb-4">
          <span
            className="w-3 h-3 rounded-full bg-accent animate-pulse"
            style={{ animationDelay: '0ms' }}
          />
          <span
            className="w-3 h-3 rounded-full bg-accent animate-pulse"
            style={{ animationDelay: '160ms' }}
          />
          <span
            className="w-3 h-3 rounded-full bg-accent animate-pulse"
            style={{ animationDelay: '320ms' }}
          />
        </div>
        <p className="text-sm text-text-secondary">Đang chuẩn bị...</p>
      </div>
    </main>
  );
}
