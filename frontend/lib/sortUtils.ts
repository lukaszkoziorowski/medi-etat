/**
 * Sorting utilities for job offers
 */

import { JobOffer } from '@/types';
import { JobPositionCategory, getCategoryForRole } from './filterConfig';

export type SortOption = 'recommended' | 'a-z' | 'z-a';

/**
 * Get the position category for a job (with enhanced detection for physiotherapist)
 */
function getJobPositionCategory(job: JobOffer): JobPositionCategory {
  const baseCategory = getCategoryForRole(job.role);
  
  // Enhanced detection: check title/description for physiotherapist
  if (baseCategory === JobPositionCategory.OTHER) {
    const title = (job.title || '').toLowerCase();
    const description = (job.description || '').toLowerCase();
    const text = `${title} ${description}`;
    
    if (
      text.includes('fizjoterapeuta') ||
      text.includes('fizjoterapeutka') ||
      text.includes('fizjoterapeut') ||
      text.includes('physiotherapist')
    ) {
      return JobPositionCategory.PHYSIOTHERAPIST;
    }
  }
  
  return baseCategory;
}

/**
 * Get sort order for recommended sorting
 * Lower number = higher priority
 */
function getRecommendedSortOrder(category: JobPositionCategory): number {
  const order: Record<JobPositionCategory, number> = {
    [JobPositionCategory.MIDWIFE]: 1,      // Położna - first
    [JobPositionCategory.NURSE]: 2,         // Pielęgniarka - second
    [JobPositionCategory.PHYSIOTHERAPIST]: 3, // Fizjoterapeuta - third
    [JobPositionCategory.OTHER]: 4,         // Inne - last
  };
  return order[category] || 4;
}

/**
 * Sort job offers based on the selected sort option
 */
export function sortJobs(jobs: JobOffer[], sortOption: SortOption): JobOffer[] {
  const sorted = [...jobs];
  
  switch (sortOption) {
    case 'recommended':
      sorted.sort((a, b) => {
        const categoryA = getJobPositionCategory(a);
        const categoryB = getJobPositionCategory(b);
        
        const orderA = getRecommendedSortOrder(categoryA);
        const orderB = getRecommendedSortOrder(categoryB);
        
        // First sort by category order
        if (orderA !== orderB) {
          return orderA - orderB;
        }
        
        // Then sort alphabetically by title within the same category
        return a.title.localeCompare(b.title, 'pl', { sensitivity: 'base' });
      });
      break;
      
    case 'a-z':
      sorted.sort((a, b) => {
        return a.title.localeCompare(b.title, 'pl', { sensitivity: 'base' });
      });
      break;
      
    case 'z-a':
      sorted.sort((a, b) => {
        return b.title.localeCompare(a.title, 'pl', { sensitivity: 'base' });
      });
      break;
  }
  
  return sorted;
}
