import type { BirthInput, ProfileData, ProfileStatus, Feedback } from '@/lib/types';

if (!process.env.NEXT_PUBLIC_API_URL) {
  console.warn('[TuViAI] NEXT_PUBLIC_API_URL is not set. Falling back to http://localhost:8000.');
}
const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';
const FETCH_TIMEOUT_MS = 30_000;

async function fetchAPI<T>(path: string, options?: RequestInit): Promise<T> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);
  try {
    const res = await fetch(`${API_BASE}${path}`, {
      ...options, signal: controller.signal,
      headers: { 'Content-Type': 'application/json', ...options?.headers },
    });
    if (!res.ok) {
      const error = await res.json().catch(() => ({}));
      throw new Error((error as { detail?: string }).detail ?? `HTTP ${res.status}`);
    }
    return res.json() as Promise<T>;
  } catch (err) {
    if (err instanceof Error && err.name === 'AbortError') {
      throw new Error('Yêu cầu quá thời gian. Vui lòng thử lại.');
    }
    throw err;
  } finally { clearTimeout(timeoutId); }
}

export const generateProfile = (input: BirthInput) =>
  fetchAPI<{ profileId: string; status: string }>('/api/generate', { method: 'POST', body: JSON.stringify(input) });

export const getProfileStatus = (id: string) =>
  fetchAPI<ProfileStatus>(`/api/profile/${id}/status`);

export const getProfile = (id: string) =>
  fetchAPI<ProfileData>(`/api/profile/${id}`, { cache: 'force-cache' });

export const submitFeedback = (feedback: Feedback) =>
  fetchAPI<void>('/api/feedback', { method: 'POST', body: JSON.stringify(feedback) });
