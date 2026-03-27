'use client';

import { useEffect } from 'react';
import Link from 'next/link';

interface ErrorProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function ProcessingError({ error, reset }: ErrorProps) {
  useEffect(() => {
    console.error('[ProcessingError]', error);
  }, [error]);

  return (
    <main id="main-content" className="min-h-screen bg-bg-primary flex items-center justify-center px-4">
      <div className="text-center max-w-md">
        <h2 className="text-xl font-semibold text-text-primary mb-2">
          Lỗi trong quá trình xử lý
        </h2>
        <p className="text-text-secondary mb-6">
          Đã xảy ra lỗi trong quá trình tính toán và luận giải. Vui lòng thử lại.
        </p>
        <div className="flex gap-3 justify-center">
          <button
            onClick={reset}
            className="bg-accent text-white rounded-md px-5 py-2.5 text-sm font-medium hover:bg-accent-hover transition-colors"
          >
            Thử lại
          </button>
          <Link
            href="/form"
            className="bg-transparent border border-border text-text-primary rounded-md px-5 py-2.5 text-sm font-medium hover:bg-bg-subtle transition-colors"
          >
            Nhập lại thông tin
          </Link>
        </div>
      </div>
    </main>
  );
}
