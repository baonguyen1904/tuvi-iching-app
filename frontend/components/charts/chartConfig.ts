export const CHART_COLORS = {
  duong: '#2563EB',
  am:    '#F59E0B',
  tb:    '#9CA3AF',
} as const;

export const CHART_DEFAULTS = {
  margin: { top: 16, right: 8, bottom: 8, left: -16 },
  animationDuration: 600,
  animationEasing: 'ease-out' as const,
  strokeWidth: 2,
  dotRadius: 0,
  activeDotRadius: 4,
} as const;

export const tooltipStyle = {
  backgroundColor: '#FFFFFF',
  border: '1px solid #E5E7EB',
  borderRadius: '8px',
  fontSize: '13px',
  boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
  padding: '8px 12px',
};

export const axisStyle = {
  tick: { fill: '#9CA3AF', fontSize: 11 },
  line: { stroke: '#E5E7EB' },
};
