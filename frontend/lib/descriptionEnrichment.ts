/**
 * Description enrichment utilities
 * 
 * Generates meaningful job descriptions when original content is insufficient.
 * Keeps descriptions factual, neutral, and helpful without speculation.
 */

import { JobOffer, MedicalRole } from '@/types';
import { JobPositionCategory, getCategoryForRole, POSITION_LABELS } from './filterConfig';

/**
 * Check if a description is sufficient (has meaningful content)
 */
function isDescriptionSufficient(description: string | null | undefined): boolean {
  if (!description) return false;
  
  const trimmed = description.trim();
  
  // Minimum length threshold
  if (trimmed.length < 50) return false;
  
  // Check if it's just placeholder text or very generic
  const genericPatterns = [
    /^oferta pracy$/i,
    /^zobacz szczegóły$/i,
    /^czytaj więcej$/i,
    /^więcej informacji$/i,
  ];
  
  if (genericPatterns.some(pattern => pattern.test(trimmed))) {
    return false;
  }
  
  return true;
}

/**
 * Analyze facility type from facility name
 */
function analyzeFacilityType(facilityName: string): string {
  const name = facilityName.toLowerCase();
  
  if (name.includes('szpital') || name.includes('hospital')) {
    return 'szpital';
  }
  if (name.includes('przychodnia') || name.includes('przychodni')) {
    return 'przychodnia';
  }
  if (name.includes('klinika') || name.includes('clinic')) {
    return 'klinika';
  }
  if (name.includes('centrum') || name.includes('center')) {
    return 'centrum';
  }
  if (name.includes('zakład') || name.includes('oddział')) {
    return 'oddział';
  }
  
  return 'placówka medyczna';
}

/**
 * Get role-specific context for description generation
 */
function getRoleContext(role: MedicalRole, category: JobPositionCategory): string {
  const roleLabels: Record<JobPositionCategory, string> = {
    [JobPositionCategory.NURSE]: 'pielęgniarskiej',
    [JobPositionCategory.MIDWIFE]: 'położniczej',
    [JobPositionCategory.PHYSIOTHERAPIST]: 'fizjoterapii',
    [JobPositionCategory.OTHER]: 'medycznej',
  };
  
  return roleLabels[category] || 'medycznej';
}

/**
 * Generate an enriched description when original is insufficient
 */
export function enrichDescription(job: JobOffer): string {
  // If description is sufficient, return it (cleaned)
  if (isDescriptionSufficient(job.description)) {
    return job.description!.trim();
  }
  
  // Generate description based on available information
  const category = getCategoryForRole(job.role);
  const categoryLabel = POSITION_LABELS[category];
  const facilityType = analyzeFacilityType(job.facility_name);
  const roleContext = getRoleContext(job.role, category);
  
  // Build description parts
  const parts: string[] = [];
  
  // Opening statement
  parts.push(
    `Oferta pracy na stanowisku ${categoryLabel.toLowerCase()} w ${facilityType} ${job.facility_name} w ${job.city}.`
  );
  
  // Role-specific context
  if (category === JobPositionCategory.NURSE) {
    parts.push(
      'Stanowisko wymaga odpowiednich kwalifikacji zawodowych oraz doświadczenia w opiece nad pacjentami.'
    );
  } else if (category === JobPositionCategory.MIDWIFE) {
    parts.push(
      'Stanowisko wymaga kwalifikacji położniczych oraz doświadczenia w opiece nad kobietami w ciąży i noworodkami.'
    );
  } else if (category === JobPositionCategory.PHYSIOTHERAPIST) {
    parts.push(
      'Stanowisko wymaga kwalifikacji fizjoterapeutycznych oraz doświadczenia w prowadzeniu terapii i rehabilitacji.'
    );
  } else {
    parts.push(
      'Stanowisko wymaga odpowiednich kwalifikacji zawodowych oraz doświadczenia w pracy w sektorze opieki zdrowotnej.'
    );
  }
  
  // Facility context
  if (facilityType === 'szpital') {
    parts.push(
      `Praca w ${facilityType}u oferuje możliwość pracy w zróżnicowanym środowisku medycznym z dostępem do nowoczesnego sprzętu i specjalistycznych oddziałów.`
    );
  } else if (facilityType === 'przychodnia') {
    parts.push(
      `Praca w ${facilityType}i oferuje możliwość pracy w środowisku ambulatoryjnym z bezpośrednim kontaktem z pacjentami.`
    );
  } else {
    parts.push(
      `Praca w ${facilityType}i oferuje możliwość rozwoju zawodowego w profesjonalnym środowisku medycznym.`
    );
  }
  
  // Closing statement
  parts.push(
    'Szczegółowe informacje dotyczące wymagań, zakresu obowiązków oraz procesu rekrutacji dostępne są na stronie źródłowej oferty.'
  );
  
  return parts.join(' ');
}

/**
 * Clean and format an existing description for better readability
 */
export function cleanDescription(description: string): string {
  if (!description) return '';
  
  let cleaned = description.trim();
  
  // Remove excessive whitespace
  cleaned = cleaned.replace(/\s+/g, ' ');
  
  // Remove excessive line breaks (more than 2 consecutive)
  cleaned = cleaned.replace(/\n{3,}/g, '\n\n');
  
  // Ensure proper spacing after periods
  cleaned = cleaned.replace(/\.([A-Z])/g, '. $1');
  
  return cleaned;
}
