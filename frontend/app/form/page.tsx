import type { Metadata } from 'next';
import Link from 'next/link';
import { ChevronLeft } from 'lucide-react';
import BirthInputForm from '@/components/form/BirthInputForm';

export const metadata: Metadata = {
  title: 'Nhập thông tin — TuVi AI',
  description: 'Nhập ngày giờ sinh để nhận luận giải tử vi cá nhân hóa.',
};

export default function FormPage() {
  return (
    <div id="main-content" className="min-h-screen bg-bg-primary">
      {/* Fixed header */}
      <header className="fixed top-0 left-0 right-0 h-14 z-10
        bg-bg-surface border-b border-border flex items-center px-4">
        <Link
          href="/"
          className="flex items-center gap-1 text-sm text-text-secondary hover:text-text-primary
            transition-colors duration-100 px-2 py-1.5 rounded-md hover:bg-bg-subtle"
        >
          <ChevronLeft size={16} />
          Trang chủ
        </Link>
        <span className="absolute left-1/2 -translate-x-1/2 font-semibold text-sm text-text-primary">
          TuVi AI
        </span>
      </header>

      {/* Form content */}
      <div className="flex flex-col items-center justify-center px-4 py-12 pt-[80px]">
        <div className="max-w-[480px] w-full bg-bg-surface border border-border
          rounded-[12px] shadow-md p-4 sm:p-6">
          <BirthInputForm />
        </div>
      </div>
    </div>
  );
}
