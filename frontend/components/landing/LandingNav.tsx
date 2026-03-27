'use client';
import { useState, useEffect } from 'react';
import Link from 'next/link';

export default function LandingNav() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 8);
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <nav
      className={`sticky top-0 z-50 h-14 flex items-center justify-between px-4
        bg-[rgba(250,250,250,0.9)] backdrop-blur-sm transition-colors duration-150
        ${scrolled ? 'border-b border-border' : 'border-b border-transparent'}`}
    >
      <span className="font-semibold text-text-primary text-sm">TuVi AI</span>
      <Link
        href="/form"
        className="bg-accent hover:bg-accent-hover text-white text-sm font-medium
          px-4 py-1.5 rounded-md transition-colors duration-100 h-9 flex items-center"
      >
        Xem luận giải
      </Link>
    </nav>
  );
}
