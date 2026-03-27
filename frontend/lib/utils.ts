import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function preprocessInterpretation(text: string): string {
  return text
    .replace(/▲/g, '<span class="text-emerald-600 font-medium">▲</span>')
    .replace(/▼/g, '<span class="text-amber-600 font-medium">▼</span>');
}
