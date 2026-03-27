import { CheckCircle2, Loader2 } from 'lucide-react';

type ApiStep =
  | 'scraping_cohoc'
  | 'scraping_tuvivn'
  | 'scoring'
  | 'ai_generating'
  | 'completed'
  | 'failed'
  | string;

interface Props {
  step: ApiStep;
}

function getStepStatus(
  uiStepIndex: number,
  apiStep: ApiStep
): 'completed' | 'in-progress' | 'pending' {
  const mapping: Record<string, number> = {
    scraping_cohoc: 0,
    scraping_tuvivn: 0,
    scoring: 1,
    ai_generating: 2,
    completed: 3,
  };

  const currentUiStep = mapping[apiStep] ?? 0;

  if (uiStepIndex < currentUiStep) return 'completed';
  if (uiStepIndex === currentUiStep) return 'in-progress';
  return 'pending';
}

const STEPS = [
  'Đang lấy lá số...',
  'Đang tính toán điểm số...',
  'Đang phân tích vận mệnh...',
  'Hoàn tất!',
];

export default function StepIndicator({ step }: Props) {
  const resolvedStep = step === 'completed' ? 'completed' : step;

  return (
    <ol role="list" aria-label="Các bước xử lý" className="flex flex-col gap-3 max-w-[280px] mx-auto">
      {STEPS.map((label, i) => {
        const status =
          resolvedStep === 'completed'
            ? 'completed'
            : getStepStatus(i, resolvedStep);

        return (
          <li key={i} className="flex items-center gap-3" aria-current={status === 'in-progress' ? 'step' : undefined}>
            {/* Status icon */}
            <div className="w-6 h-6 flex-shrink-0 flex items-center justify-center">
              {status === 'completed' ? (
                <CheckCircle2 className="w-5 h-5 text-alert-positive" />
              ) : status === 'in-progress' ? (
                <Loader2 className="w-[18px] h-[18px] text-accent animate-spin" />
              ) : (
                <div className="w-4 h-4 rounded-full border-2 border-border mx-auto" />
              )}
            </div>

            {/* Label */}
            <span
              className={
                status === 'pending'
                  ? 'text-body text-text-tertiary'
                  : 'text-body font-medium text-text-primary'
              }
            >
              {label}
            </span>
          </li>
        );
      })}
    </ol>
  );
}
