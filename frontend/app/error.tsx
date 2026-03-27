'use client';

import { useEffect } from 'react';
import Link from 'next/link';

interface ErrorProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function GlobalError({ error, reset }: ErrorProps) {
  useEffect(() => {
    console.error('[GlobalError]', error);
  }, [error]);

  return (
    <main id="main-content" className="min-h-screen bg-bg-primary flex items-center justify-center px-4">
      <div className="text-center max-w-md">
        <h1 className="text-2xl font-semibold text-text-primary mb-2">
          Đã xảy ra lỗi
        </h1>
        <p className="text-text-secondary mb-6">
          Đã xảy ra lỗi không mong muốn. Vui lòng thử lại hoặc quay về trang chủ.
        </p>
        <div className="flex gap-3 justify-center">
          <button
            onClick={reset}
            className="bg-accent text-white rounded-md px-5 py-2.5 text-sm font-medium hover:bg-accent-hover transition-colors"
          >
            Thử lại
          </button>
          <Link
            href="/"
            className="bg-transparent border border-border text-text-primary rounded-md px-5 py-2.5 text-sm font-medium hover:bg-bg-subtle transition-colors"
          >
            Về trang chủ
          </Link>
        </div>
      </div>
    </main>
  );
}
