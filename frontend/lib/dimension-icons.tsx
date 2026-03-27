import {
  Briefcase,
  TrendingUp,
  Heart,
  Activity,
  Home,
  BookOpen,
  Baby,
  Compass,
  type LucideIcon,
} from 'lucide-react';
import type { DimensionKey } from '@/lib/constants';

/**
 * Maps dimension keys to their corresponding Lucide icon components.
 * DIMENSION_ICONS in constants.ts stores string names; this file provides
 * the actual React components for use in JSX.
 */
export const DIMENSION_ICON_COMPONENTS: Record<DimensionKey, LucideIcon> = {
  su_nghiep: Briefcase,
  tien_bac: TrendingUp,
  hon_nhan: Heart,
  suc_khoe: Activity,
  dat_dai: Home,
  hoc_tap: BookOpen,
  con_cai: Baby,
  van_menh: Compass,
};
