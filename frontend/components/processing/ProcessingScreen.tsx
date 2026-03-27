'use client';

import { useEffect, useRef, useState } from 'react';
import { useRouter } from 'next/navigation';
import { AlertTriangle } from 'lucide-react';
import { getProfileStatus, generateProfile } from '@/lib/api';
import { ProfileStatus } from '@/lib/types';
import StepIndicator from './StepIndicator';
import FunFactRotator from './FunFactRotator';

const POLL_INTERVAL = 2000;
const TIMEOUT_MS = 120000;

interface Props {
  profileId: string;
}

export default function ProcessingScreen({ profileId }: Props) {
  const router = useRouter();
  const [currentStatus, setCurrentStatus] = useState<ProfileStatus | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isRetrying, setIsRetrying] = useState(false);
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const retryCount = useRef(0);

  useEffect(() => {
    const startTime = Date.now();

    const poll = async () => {
      if (Date.now() - startTime > TIMEOUT_MS) {
        setError('Quá thời gian chờ. Vui lòng thử lại.');
        return;
      }

      try {
        const status = await getProfileStatus(profileId);
        setCurrentStatus(status);

        if (status.status === 'completed') {
          router.push(`/result/${profileId}`);
          return;
        }

        if (status.status === 'failed') {
          setError(status.message || 'Có lỗi xảy ra.');
          return;
        }

        timeoutRef.current = setTimeout(poll, POLL_INTERVAL);
      } catch {
        retryCount.current++;
        if (retryCount.current >= 3) {
          setError('Mất kết nối. Vui lòng thử lại.');
        } else {
          timeoutRef.current = setTimeout(poll, POLL_INTERVAL);
        }
      }
    };

    poll();

    return () => {
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
    };
  }, [profileId, router]);

  const handleRetry = async () => {
    setIsRetrying(true);
    try {
      const lastInput = sessionStorage.getItem('tuvi_last_input');
      if (lastInput) {
        const result = await generateProfile(JSON.parse(lastInput));
        router.push(`/processing/${result.profileId}`);
      } else {
        router.push('/form');
      }
    } catch {
      router.push('/form');
    } finally {
      setIsRetrying(false);
    }
  };

  const aiProgress = currentStatus?.aiProgress ?? 0;
  const step = currentStatus?.step ?? 'scraping_cohoc';

  return (
    <div id="main-content" className="bg-bg-primary min-h-screen flex flex-col items-center justify-center px-4 py-16">
      <div className="max-w-[400px] w-full text-center">
        {/* Pulsing animation */}
        <div className="flex gap-2 justify-center mb-10">
          {[0, 160, 320].map((delay) => (
            <div
              key={delay}
              className="w-2.5 h-2.5 bg-accent rounded-full"
              style={{ animation: `pulse-dot 1.2s ease-in-out infinite ${delay}ms` }}
            />
          ))}
        </div>

        {/* Step indicator */}
        <StepIndicator step={step} />

        {/* Progress text */}
        <div className="mt-6 text-center">
          {error ? (
            <div className="flex flex-col items-center">
              <AlertTriangle className="w-6 h-6 text-amber-500 mb-3" />
              <p className="text-body text-text-primary font-medium">
                Có lỗi xảy ra trong quá trình xử lý.
              </p>
              <p className="text-body-sm text-text-secondary mt-1">{error}</p>
              <button
                onClick={handleRetry}
                disabled={isRetrying}
                className="mt-4 px-6 py-2 bg-accent text-white rounded-[8px] text-body font-medium hover:bg-accent/90 disabled:opacity-50 transition-colors"
              >
                {isRetrying ? 'Đang thử lại...' : 'Thử lại'}
              </button>
            </div>
          ) : step === 'ai_generating' ? (
            <>
              <p className="text-body-sm text-text-secondary">
                {aiProgress}/8 lĩnh vực đã được phân tích
              </p>
              <div className="w-[200px] h-1 bg-bg-subtle rounded-full mx-auto mt-2 overflow-hidden">
                <div
                  className="h-full bg-accent rounded-full transition-[width] duration-300 ease-in-out"
                  style={{ width: `${(aiProgress / 8) * 100}%` }}
                />
              </div>
            </>
          ) : (
            <p className="text-body-sm text-text-secondary">
              {currentStatus?.message ?? 'Đang khởi tạo...'}
            </p>
          )}
        </div>

        {/* Fun fact rotator */}
        {!error && <FunFactRotator />}
      </div>
    </div>
  );
}
