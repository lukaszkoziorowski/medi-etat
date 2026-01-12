/**
 * Filter configuration and role mapping
 * 
 * This file defines the standardized filter categories and maps
 * backend MedicalRole values to these categories.
 */

import { MedicalRole } from '@/types';

/**
 * Standardized job position categories for filtering
 */
export enum JobPositionCategory {
  NURSE = 'nurse',
  MIDWIFE = 'midwife',
  PHYSIOTHERAPIST = 'physiotherapist',
  OTHER = 'other',
}

/**
 * Display labels for position categories
 */
export const POSITION_LABELS: Record<JobPositionCategory, string> = {
  [JobPositionCategory.NURSE]: 'Pielęgniarka',
  [JobPositionCategory.MIDWIFE]: 'Położna',
  [JobPositionCategory.PHYSIOTHERAPIST]: 'Fizjoterapeuta',
  [JobPositionCategory.OTHER]: 'Inne',
};

/**
 * Maps backend MedicalRole to standardized position categories
 * 
 * This mapping is configurable and extensible. If a role cannot
 * be confidently matched, it should map to OTHER.
 */
export const ROLE_TO_CATEGORY_MAP: Record<MedicalRole, JobPositionCategory> = {
  [MedicalRole.PIELĘGNIARKA]: JobPositionCategory.NURSE,
  [MedicalRole.POŁOŻNA]: JobPositionCategory.MIDWIFE,
  [MedicalRole.LEKARZ]: JobPositionCategory.OTHER, // Doctors map to Other for now
  [MedicalRole.RATOWNIK]: JobPositionCategory.OTHER, // Paramedics map to Other
  [MedicalRole.INNY]: JobPositionCategory.OTHER,
};

/**
 * Maps a MedicalRole to its standardized category
 */
export function getCategoryForRole(role: MedicalRole): JobPositionCategory {
  return ROLE_TO_CATEGORY_MAP[role] || JobPositionCategory.OTHER;
}

/**
 * Get all available position categories
 */
export function getAllPositionCategories(): JobPositionCategory[] {
  return Object.values(JobPositionCategory);
}
