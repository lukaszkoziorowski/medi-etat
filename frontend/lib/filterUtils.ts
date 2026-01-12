/**
 * Filter utilities for job offer filtering
 * 
 * Implements:
 * - OR logic within the same filter group (e.g., Nurse OR Physiotherapist)
 * - AND logic across different filter groups (e.g., (Nurse OR Physiotherapist) AND Gdańsk)
 * - Global search across title and description
 */

import { JobOffer, MedicalRole } from '@/types';
import { JobPositionCategory, getCategoryForRole } from './filterConfig';

export interface FilterState {
  positions: JobPositionCategory[];
  cities: string[];
  searchQuery: string;
}

/**
 * Get the position category for a job, with enhanced detection
 * for roles that might be in the "INNY" category but should be
 * classified differently (e.g., physiotherapist)
 */
function getJobPositionCategory(job: JobOffer): JobPositionCategory {
  const baseCategory = getCategoryForRole(job.role);
  
  // Enhanced detection: check title/description for physiotherapist
  // even if role is "INNY"
  if (baseCategory === JobPositionCategory.OTHER) {
    const title = (job.title || '').toLowerCase();
    const description = (job.description || '').toLowerCase();
    const text = `${title} ${description}`;
    
    // Check for physiotherapist keywords
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
 * Check if a job offer matches the position filter
 * Uses OR logic: job matches if its category is in the selected positions
 */
function matchesPositionFilter(
  job: JobOffer,
  selectedPositions: JobPositionCategory[]
): boolean {
  if (selectedPositions.length === 0) {
    return true; // No filter = show all
  }

  const jobCategory = getJobPositionCategory(job);
  return selectedPositions.includes(jobCategory);
}

/**
 * Check if a job offer matches the city filter
 * Uses OR logic: job matches if its city is in the selected cities
 */
function matchesCityFilter(job: JobOffer, selectedCities: string[]): boolean {
  if (selectedCities.length === 0) {
    return true; // No filter = show all
  }

  return selectedCities.includes(job.city);
}

/**
 * Check if a job offer matches the search query
 * Searches in title and description (case-insensitive)
 */
function matchesSearchQuery(job: JobOffer, searchQuery: string): boolean {
  if (!searchQuery.trim()) {
    return true; // No search = show all
  }

  const query = searchQuery.toLowerCase().trim();
  const title = (job.title || '').toLowerCase();
  const description = (job.description || '').toLowerCase();

  return title.includes(query) || description.includes(query);
}

/**
 * Filter job offers based on filter state
 * 
 * Logic:
 * - OR within groups: (position1 OR position2) AND (city1 OR city2)
 * - AND across groups: positions AND cities AND search
 */
export function filterJobs(jobs: JobOffer[], filters: FilterState): JobOffer[] {
  return jobs.filter((job) => {
    const matchesPosition = matchesPositionFilter(job, filters.positions);
    const matchesCity = matchesCityFilter(job, filters.cities);
    const matchesSearch = matchesSearchQuery(job, filters.searchQuery);

    // AND logic across filter groups
    return matchesPosition && matchesCity && matchesSearch;
  });
}

/**
 * Parse filter state from URL search params
 */
export function parseFiltersFromURL(
  searchParams: URLSearchParams
): Partial<FilterState> {
  const positions = searchParams.getAll('position') as JobPositionCategory[];
  const cities = searchParams.getAll('city');
  const searchQuery = searchParams.get('search') || '';

  return {
    positions: positions.length > 0 ? positions : [],
    cities: cities.length > 0 ? cities : [],
    searchQuery,
  };
}

/**
 * Build URL search params from filter state
 */
export function buildFiltersURL(filters: FilterState): string {
  const params = new URLSearchParams();

  filters.positions.forEach((position) => {
    params.append('position', position);
  });

  filters.cities.forEach((city) => {
    params.append('city', city);
  });

  if (filters.searchQuery.trim()) {
    params.set('search', filters.searchQuery.trim());
  }

  return params.toString();
}
