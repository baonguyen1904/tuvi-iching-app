import Link from 'next/link';
import { ChevronLeft } from 'lucide-react';
import ShareButton from '@/components/result/ShareButton';

interface Props {
  profileId: string;
}

export default function DetailHeader({ profileId }: Props) {
  return (
    <header className="sticky top-0 z-40 h-14 bg-bg-surface border-b border-border">
      <div className="max-w-3xl mx-auto px-4 h-full flex items-center justify-between">
        <Link
          href={`/result/${profileId}`}
          className="flex items-center gap-1.5 text-body text-text-secondary hover:text-text-primary transition-colors"
        >
          <ChevronLeft className="w-4 h-4" />
          Tổng quan
        </Link>
        <ShareButton />
      </div>
    </header>
  );
}
