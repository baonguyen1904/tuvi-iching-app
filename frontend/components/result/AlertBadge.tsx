interface AlertBadgeProps {
  type: 'positive' | 'negative';
  count: number;
  label?: string;
}

export default function AlertBadge({ type, count, label }: AlertBadgeProps) {
  if (type === 'positive') {
    const text = label ?? (count > 1 ? `\u25B2 ${count} cơ hội` : '\u25B2 Cơ hội');
    return (
      <span className="bg-alert-positive-bg border border-alert-positive-bdr text-emerald-700 px-2 py-0.5 rounded-full text-caption font-medium">
        {text}
      </span>
    );
  }

  const text = label ?? `\u25BC ${count} cần chú ý`;
  return (
    <span className="bg-alert-negative-bg border border-alert-negative-bdr text-amber-700 px-2 py-0.5 rounded-full text-caption font-medium">
      {text}
    </span>
  );
}
