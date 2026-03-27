'use client';

import { Share2 } from 'lucide-react';
import { toast } from 'sonner';

export default function ShareButton() {
  async function handleShare() {
    const url = window.location.href;
    try {
      await navigator.clipboard.writeText(url);
      toast.success('Đã copy link!', { duration: 3000 });
    } catch {
      // I1: Fallback for browsers without Clipboard API (HTTP context, older Safari)
      try {
        const textarea = document.createElement('textarea');
        textarea.value = url;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        toast.success('Đã copy link!', { duration: 3000 });
      } catch {
        toast.error('Không thể copy. Hãy copy link thủ công.', { duration: 5000 });
      }
    }
  }

  return (
    <button
      onClick={handleShare}
      className="flex items-center gap-2 text-body text-text-secondary hover:text-text-primary transition-colors px-2 py-1 rounded"
    >
      <Share2 className="w-4 h-4" />
      <span>Chia sẻ</span>
    </button>
  );
}
