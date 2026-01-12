'use client';

import { useEffect, useState, useMemo } from 'react';
import { JobOffer } from '@/types';
import { fetchJobs } from '@/lib/api';
import { getCategoryForRole } from '@/lib/filterConfig';
import { JobPositionCategory } from '@/lib/filterConfig';
import CategoryBadge from './CategoryBadge';
import LocationTag from './LocationTag';
import FacilityTag from './FacilityTag';
import SimilarJobCard from './SimilarJobCard';
import LocationMap from './LocationMap';
import Button from '../ui/Button';
import { enrichDescription, cleanDescription } from '@/lib/descriptionEnrichment';

interface JobDetailClientProps {
  job: JobOffer;
}

/**
 * Client component for job detail page
 * Handles fetching similar jobs and rendering the two-column layout
 */
export default function JobDetailClient({ job }: JobDetailClientProps) {
  const [allJobs, setAllJobs] = useState<JobOffer[]>([]);
  const [loadingSimilar, setLoadingSimilar] = useState(true);

  // Get job category for similarity matching
  const jobCategory = useMemo(() => {
    const baseCategory = getCategoryForRole(job.role);
    
    // Enhanced detection for physiotherapist (same logic as filterUtils)
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
  }, [job]);

  // Fetch all jobs to find similar ones
  useEffect(() => {
    const loadSimilarJobs = async () => {
      try {
        setLoadingSimilar(true);
        const jobsData = await fetchJobs({ limit: 1000 });
        setAllJobs(jobsData.results || []);
      } catch (err) {
        console.error('Error fetching similar jobs:', err);
      } finally {
        setLoadingSimilar(false);
      }
    };

    loadSimilarJobs();
  }, []);

  // Filter similar jobs: 
  // 1. Priority: same facility (company/location)
  // 2. Fallback: same category if not enough from same facility
  const similarJobs = useMemo(() => {
    // Helper function to get job category with enhanced detection
    const getJobCategory = (j: JobOffer): JobPositionCategory => {
      const baseCategory = getCategoryForRole(j.role);
      
      // Enhanced detection for physiotherapist
      if (baseCategory === JobPositionCategory.OTHER) {
        const title = (j.title || '').toLowerCase();
        const description = (j.description || '').toLowerCase();
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
    };

    // Filter out current job
    const otherJobs = allJobs.filter((j) => j.id !== job.id);
    
    // Priority 1: Same facility (company/location)
    const sameFacilityJobs = otherJobs.filter((j) => 
      j.facility_name === job.facility_name
    );
    
    // If we have enough from same facility, return them
    if (sameFacilityJobs.length >= 3) {
      return sameFacilityJobs.slice(0, 3);
    }
    
    // Priority 2: Same category (regardless of facility or city)
    const sameCategoryJobs = otherJobs.filter((j) => {
      const otherCategory = getJobCategory(j);
      return otherCategory === jobCategory;
    });
    
    // Combine: same facility first, then same category
    // Remove duplicates (jobs that appear in both lists)
    const combined = [...sameFacilityJobs];
    const facilityIds = new Set(sameFacilityJobs.map(j => j.id));
    
    for (const j of sameCategoryJobs) {
      if (!facilityIds.has(j.id) && combined.length < 3) {
        combined.push(j);
      }
    }
    
    return combined.slice(0, 3);
  }, [allJobs, job.id, job.facility_name, jobCategory]);

  // Enrich description if needed
  const enrichedDescription = useMemo(() => {
    return enrichDescription(job);
  }, [job]);

  // Clean description for display
  const displayDescription = useMemo(() => {
    if (!enrichedDescription) return null;
    return cleanDescription(enrichedDescription);
  }, [enrichedDescription]);

  return (
    <div>
      {/* Job Title - Above both columns */}
      <h1 className="text-3xl lg:text-4xl font-bold text-[var(--color-text-primary)] mb-6 leading-tight">
        {job.title}
      </h1>

      <div className="grid gap-8 lg:grid-cols-[1fr_320px]">
        {/* Left Column - Main Content */}
        <article className="min-w-0">
          {/* Key Information Section */}
          <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-2xl p-6 mb-8">
            <div className="space-y-4">
            <div className="flex items-center gap-3">
              <span className="text-sm font-medium text-[var(--color-text-secondary)] min-w-[100px]">
                Kategoria:
              </span>
              <CategoryBadge 
                role={job.role} 
                title={job.title}
                description={job.description}
                size="md" 
              />
            </div>
            
            <div className="flex items-center gap-3">
              <span className="text-sm font-medium text-[var(--color-text-secondary)] min-w-[100px]">
                Lokalizacja:
              </span>
              <LocationTag city={job.city} size="md" />
            </div>
            
            <div className="flex items-center gap-3">
              <span className="text-sm font-medium text-[var(--color-text-secondary)] min-w-[100px]">
                Placówka:
              </span>
              <FacilityTag facilityName={job.facility_name} size="md" />
            </div>
          </div>
        </div>

        {/* Job Description */}
        {displayDescription && (
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-[var(--color-text-primary)] mb-4">
              Opis stanowiska
            </h2>
            <div className="prose prose-base max-w-none text-[var(--color-text-primary)] leading-relaxed whitespace-pre-wrap">
              {displayDescription}
            </div>
          </div>
        )}

        {/* Location Map */}
        <LocationMap job={job} />

        {/* Additional Information Section */}
        {job.summary && job.summary !== job.description && (
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-[var(--color-text-primary)] mb-4">
              Dodatkowe informacje
            </h2>
            <div className="prose prose-base max-w-none text-[var(--color-text-secondary)] leading-relaxed">
              {job.summary}
            </div>
          </div>
        )}
        </article>

        {/* Right Column - Actions and Similar Jobs */}
        <aside className="lg:sticky lg:top-8 lg:h-fit space-y-6">
        {/* Primary Action Button */}
        <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-2xl p-6">
          <a
            href={job.source_url}
            target="_blank"
            rel="noopener noreferrer"
            className="block w-full"
          >
            <Button variant="primary" size="lg" className="w-full">
              Przejdź do oferty pracy
            </Button>
          </a>
          <p className="text-xs text-[var(--color-text-secondary)] mt-3 text-center">
            Link otworzy się w nowej karcie
          </p>
        </div>

        {/* Similar Job Offers */}
        {similarJobs.length > 0 && (
          <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-2xl p-6">
            <h3 className="text-lg font-semibold text-[var(--color-text-primary)] mb-4">
              Podobne oferty
            </h3>
            <div className="space-y-3">
              {similarJobs.map((similarJob) => (
                <SimilarJobCard key={similarJob.id} job={similarJob} />
              ))}
            </div>
          </div>
        )}

        {!loadingSimilar && similarJobs.length === 0 && (
          <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-2xl p-6">
            <h3 className="text-lg font-semibold text-[var(--color-text-primary)] mb-2">
              Podobne oferty
            </h3>
            <p className="text-sm text-[var(--color-text-secondary)]">
              Brak podobnych ofert w tej lokalizacji
            </p>
          </div>
        )}
        </aside>
      </div>
    </div>
  );
}
