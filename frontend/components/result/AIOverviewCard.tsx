import { Sparkles } from 'lucide-react';

interface Props {
  summary: string | null;
}

export default function AIOverviewCard({ summary }: Props) {
  return (
    <div className="bg-bg-surface border border-border rounded-[12px] p-4 mt-4">
      <div className="flex items-center gap-2">
        <Sparkles className="w-[18px] h-[18px] text-accent flex-shrink-0" />
        <h2 className="text-heading-sm font-semibold text-text-primary">
          Tổng quan vận mệnh
        </h2>
      </div>

      <div className="mt-3">
        {summary ? (
          <p className="text-body text-text-secondary leading-relaxed">{summary}</p>
        ) : (
          <div className="flex flex-col gap-2">
            <div className="h-4 bg-bg-subtle rounded animate-pulse" />
            <div className="h-4 bg-bg-subtle rounded animate-pulse" />
            <div className="h-2.5 w-3/4 bg-bg-subtle rounded animate-pulse" />
          </div>
        )}
      </div>
    </div>
  );
}
