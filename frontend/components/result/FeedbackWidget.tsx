'use client';

import { useState, useRef } from 'react';
import { ThumbsUp, ThumbsDown, CheckCircle2, AlertTriangle } from 'lucide-react';
import { submitFeedback } from '@/lib/api';

// B10: profileId passed as prop — do NOT read from URL params
interface FeedbackWidgetProps {
  profileId: string;
}

type FeedbackState = 'idle' | 'positive' | 'negative' | 'expanded' | 'submitted' | 'error';

export default function FeedbackWidget({ profileId }: FeedbackWidgetProps) {
  const [state, setState] = useState<FeedbackState>('idle');
  const [comment, setComment] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  // Track vote in a ref to preserve it after state transitions
  const voteRef = useRef<'positive' | 'negative' | null>(null);

  const handleVote = (vote: 'positive' | 'negative') => {
    voteRef.current = vote;
    setState('expanded');
  };

  const handleSubmit = async () => {
    setIsSubmitting(true);
    try {
      // I6: Catch API errors and set 'error' state
      await submitFeedback({
        profileId,
        helpful: voteRef.current === 'positive',
        comment,
      });
      setState('submitted');
    } catch {
      setState('error');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="mt-12 mb-8 text-center">
      {state === 'idle' && (
        <>
          <p className="text-body text-text-secondary mb-4">
            Luận giải này có ích cho bạn không?
          </p>
          <div className="flex justify-center gap-3">
            <button
              onClick={() => handleVote('positive')}
              className="flex items-center gap-2 px-4 py-2 border border-border rounded-[8px] text-body text-text-secondary hover:border-accent-border hover:text-text-primary transition-colors"
            >
              <ThumbsUp className="w-4 h-4" />
              Có
            </button>
            <button
              onClick={() => handleVote('negative')}
              className="flex items-center gap-2 px-4 py-2 border border-border rounded-[8px] text-body text-text-secondary hover:border-accent-border hover:text-text-primary transition-colors"
            >
              <ThumbsDown className="w-4 h-4" />
              Không
            </button>
          </div>
        </>
      )}

      {state === 'expanded' && (
        <>
          <p className="text-body-sm text-text-secondary mb-3">
            Cảm ơn! Bạn muốn chia sẻ thêm không?
          </p>
          <textarea
            rows={3}
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder="Chia sẻ suy nghĩ (không bắt buộc)..."
            className="w-full max-w-sm border border-border rounded-[8px] px-3 py-2 text-body text-text-primary bg-bg-surface resize-none focus:outline-none focus:border-accent-border transition-colors"
          />
          <button
            onClick={handleSubmit}
            disabled={isSubmitting}
            className="block w-full max-w-sm mx-auto mt-2 py-2 bg-accent text-white rounded-[8px] text-body font-medium hover:bg-accent/90 disabled:opacity-50 transition-colors"
          >
            {isSubmitting ? 'Đang gửi...' : 'Gửi phản hồi'}
          </button>
          <button
            onClick={() => setState('submitted')}
            className="block w-full text-sm text-text-tertiary mt-1 hover:text-text-secondary transition-colors"
          >
            Bỏ qua
          </button>
        </>
      )}

      {state === 'submitted' && (
        <div className="flex flex-col items-center gap-2">
          <CheckCircle2 className="w-6 h-6 text-alert-positive" />
          <p className="text-body text-text-secondary">Cảm ơn bạn đã phản hồi!</p>
        </div>
      )}

      {/* I6: Error state */}
      {state === 'error' && (
        <div className="flex flex-col items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-amber-500" />
          <p className="text-body-sm text-text-secondary">
            Gửi thất bại, vui lòng thử lại.
          </p>
          <button
            onClick={() => setState('expanded')}
            className="px-4 py-2 border border-border rounded-[8px] text-body text-text-secondary hover:border-accent-border transition-colors"
          >
            Thử lại
          </button>
        </div>
      )}
    </div>
  );
}
