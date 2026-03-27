interface AlertBadgeProps {
  type: 'positive' | 'negative';
  count: number;
  label?: string;
}

export default function AlertBadge({ type, count, label }: AlertBadgeProps) {
  if (type === 'positive') {
    const text = label ?? (count > 1 ? `${count} cơ hội` : 'Cơ hội');
    const ariaLabel = `${count} cơ hội tích cực: ${label ?? 'cơ hội'}`;
    return (
      <span
        className="bg-alert-positive-bg border border-alert-positive-bdr text-emerald-700 px-2 py-0.5 rounded-full text-caption font-medium"
        aria-label={ariaLabel}
      >
        <span aria-hidden="true">{'\u25B2'}</span> {text}
      </span>
    );
  }

  const text = label ?? `${count} cần chú ý`;
  const ariaLabel = `${count} điểm cần thận trọng: ${label ?? 'cần chú ý'}`;
  return (
    <span
      className="bg-alert-negative-bg border border-alert-negative-bdr text-amber-700 px-2 py-0.5 rounded-full text-caption font-medium"
      aria-label={ariaLabel}
    >
      <span aria-hidden="true">{'\u25BC'}</span> {text}
    </span>
  );
}
