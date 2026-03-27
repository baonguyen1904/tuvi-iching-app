import Link from 'next/link';

export default function NotFound() {
  return (
    <main id="main-content" className="min-h-screen bg-bg-primary flex items-center justify-center px-4">
      <div className="text-center max-w-md">
        <p className="text-6xl font-bold text-accent mb-4">404</p>
        <h1 className="text-2xl font-semibold text-text-primary mb-2">
          Trang không tồn tại
        </h1>
        <p className="text-text-secondary mb-6">
          Trang này không tồn tại hoặc đã bị xóa.
        </p>
        <Link
          href="/"
          className="inline-block bg-accent text-white rounded-md px-5 py-2.5 text-sm font-medium hover:bg-accent-hover transition-colors"
        >
          Về trang chủ
        </Link>
      </div>
    </main>
  );
}
