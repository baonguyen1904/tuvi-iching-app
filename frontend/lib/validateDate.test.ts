import { describe, it, expect } from 'vitest';

function validateDate(date: Date | undefined): string | undefined {
  const currentYear = new Date().getFullYear();
  if (!date) return 'Vui lòng chọn ngày sinh.';
  const year = date.getFullYear();
  if (year < 1920 || year > currentYear) {
    return `Ngày sinh phải từ năm 1920 đến ${currentYear}.`;
  }
  return undefined;
}

describe('validateDate', () => {
  const currentYear = new Date().getFullYear();

  it('returns error when date is undefined', () => {
    expect(validateDate(undefined)).toBe('Vui lòng chọn ngày sinh.');
  });

  it('returns error for year before 1920', () => {
    const result = validateDate(new Date(1919, 0, 1));
    expect(result).toContain('1920');
  });

  it('returns error for year after currentYear', () => {
    const result = validateDate(new Date(currentYear + 1, 0, 1));
    expect(result).toContain(String(currentYear));
  });

  it('returns undefined for valid year 1994', () => {
    expect(validateDate(new Date(1994, 6, 19))).toBeUndefined();
  });

  it('returns undefined for year 1920 (boundary)', () => {
    expect(validateDate(new Date(1920, 0, 1))).toBeUndefined();
  });

  it('returns undefined for currentYear (boundary)', () => {
    expect(validateDate(new Date(currentYear, 0, 1))).toBeUndefined();
  });
});
