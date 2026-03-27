'use client';

import { useEffect } from 'react';
import Link from 'next/link';

interface ErrorProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function DimensionError({ error, reset }: ErrorProps) {
  useEffect(() => {
    console.error('[DimensionError]', error);
  }, [error]);

  return (
    <main id="main-content" className="min-h-screen bg-bg-primary flex items-center justify-center px-4">
      <div className="text-center max-w-md">
        <h2 className="text-xl font-semibold text-text-primary mb-2">
          Không thể tải lĩnh vực này
        </h2>
        <p className="text-text-secondary mb-6">
          Không thể tải thông tin lĩnh vực. Vui lòng thử lại hoặc quay về tổng quan.
        </p>
        <div className="flex gap-3 justify-center">
          <button
            onClick={reset}
            className="bg-accent text-white rounded-md px-5 py-2.5 text-sm font-medium hover:bg-accent-hover transition-colors"
          >
            Thử lại
          </button>
          <Link
            href=".."
            className="bg-transparent border border-border text-text-primary rounded-md px-5 py-2.5 text-sm font-medium hover:bg-bg-subtle transition-colors"
          >
            Về tổng quan
          </Link>
        </div>
      </div>
    </main>
  );
}
