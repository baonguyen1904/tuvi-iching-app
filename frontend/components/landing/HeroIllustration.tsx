export default function HeroIllustration() {
  return (
    <svg
      width="280" height="280"
      viewBox="0 0 280 280"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-label="Biểu đồ tử vi trực quan"
      role="img"
      className="w-[220px] h-[220px] sm:w-[280px] sm:h-[280px]"
    >
      {/* Concentric circles */}
      <circle cx="140" cy="140" r="120" stroke="#E5E7EB" strokeWidth="1" />
      <circle cx="140" cy="140" r="90"  stroke="#E5E7EB" strokeWidth="1" />
      <circle cx="140" cy="140" r="60"  stroke="#BFDBFE" strokeWidth="1.5" />
      <circle cx="140" cy="140" r="30"  stroke="#2563EB" strokeWidth="2" />

      {/* Node dots at compass points on outer circle */}
      <circle cx="140" cy="20"  r="5" fill="#2563EB" />
      <circle cx="260" cy="140" r="5" fill="#2563EB" />
      <circle cx="140" cy="260" r="5" fill="#2563EB" />
      <circle cx="20"  cy="140" r="5" fill="#2563EB" />

      {/* Node dots at 45deg points on mid circle */}
      <circle cx="203.6" cy="76.4"  r="4" fill="#BFDBFE" />
      <circle cx="203.6" cy="203.6" r="4" fill="#BFDBFE" />
      <circle cx="76.4"  cy="203.6" r="4" fill="#BFDBFE" />
      <circle cx="76.4"  cy="76.4"  r="4" fill="#BFDBFE" />

      {/* Spokes */}
      <line x1="140" y1="20"  x2="140" y2="260" stroke="#E5E7EB" strokeWidth="1" strokeDasharray="4 4" />
      <line x1="20"  y1="140" x2="260" y2="140" stroke="#E5E7EB" strokeWidth="1" strokeDasharray="4 4" />

      {/* Center dot */}
      <circle cx="140" cy="140" r="6" fill="#2563EB" />
    </svg>
  );
}
