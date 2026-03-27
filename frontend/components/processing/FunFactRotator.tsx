'use client';

import { useEffect, useState } from 'react';
import { FUN_FACTS } from '@/lib/constants';

export default function FunFactRotator() {
  const [index, setIndex] = useState(0);
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    const interval = setInterval(() => {
      // Fade out
      setVisible(false);
      setTimeout(() => {
        setIndex((prev) => (prev + 1) % FUN_FACTS.length);
        // Fade in
        setVisible(true);
      }, 300);
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="mt-12 max-w-[320px] mx-auto text-center">
      <div className="bg-bg-subtle rounded-[12px] px-5 py-4">
        <p className="text-caption text-text-tertiary font-medium mb-1">Bạn có biết?</p>
        <p
          className="text-body-sm text-text-secondary transition-opacity duration-300"
          style={{ opacity: visible ? 1 : 0 }}
        >
          {FUN_FACTS[index]}
        </p>
      </div>
    </div>
  );
}
