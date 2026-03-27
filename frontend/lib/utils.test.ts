import { describe, it, expect } from 'vitest';
import { preprocessInterpretation } from './utils';

describe('preprocessInterpretation', () => {
  it('wraps ▲ with emerald span', () => {
    expect(preprocessInterpretation('▲ tốt')).toBe('<span class="text-emerald-600 font-medium">▲</span> tốt');
  });
  it('wraps ▼ with amber span', () => {
    expect(preprocessInterpretation('▼ kém')).toBe('<span class="text-amber-600 font-medium">▼</span> kém');
  });
  it('handles both markers', () => {
    const result = preprocessInterpretation('▲ thuận ▼ cần chú ý');
    expect(result).toContain('text-emerald-600');
    expect(result).toContain('text-amber-600');
  });
  it('returns unchanged when no markers', () => {
    expect(preprocessInterpretation('Bình thường')).toBe('Bình thường');
  });
});

describe('score normalisation', () => {
  const norm = (s: number) => ((s + 20) / 40) * 100;
  it('-20 → 0', () => expect(norm(-20)).toBe(0));
  it('0 → 50', () => expect(norm(0)).toBe(50));
  it('20 → 100', () => expect(norm(20)).toBe(100));
  it('8.7 → ~71.75', () => expect(norm(8.7)).toBeCloseTo(71.75));
});
