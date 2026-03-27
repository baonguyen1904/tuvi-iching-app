import { describe, it, expect } from 'vitest';
import { normalize } from '../OverviewRadarChart';

describe('normalize (score normalization)', () => {
  it('maps -20 to 0', () => {
    expect(normalize(-20)).toBe(0);
  });

  it('maps 0 to 50', () => {
    expect(normalize(0)).toBe(50);
  });

  it('maps +20 to 100', () => {
    expect(normalize(20)).toBe(100);
  });

  it('clamps below -20 to 0', () => {
    expect(normalize(-30)).toBe(0);
  });

  it('clamps above +20 to 100', () => {
    expect(normalize(30)).toBe(100);
  });

  it('maps +10 to 75', () => {
    expect(normalize(10)).toBe(75);
  });

  it('maps -10 to 25', () => {
    expect(normalize(-10)).toBe(25);
  });
});
