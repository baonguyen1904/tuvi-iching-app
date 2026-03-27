import Link from 'next/link';
import ShareButton from './ShareButton';

interface Props {
  profileId: string;
}

export default function ResultHeader({ profileId: _profileId }: Props) {
  return (
    <header className="sticky top-0 z-40 h-14 bg-bg-surface border-b border-border">
      <div className="max-w-3xl mx-auto px-4 h-full flex items-center justify-between">
        <Link href="/" className="text-sm font-semibold text-text-primary">
          TuVi AI
        </Link>
        <ShareButton />
      </div>
    </header>
  );
}
