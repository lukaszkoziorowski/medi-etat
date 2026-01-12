import Link from 'next/link';
import { JobOffer } from '@/types';
import CategoryBadge from './CategoryBadge';
import LocationTag from './LocationTag';
import FacilityTag from './FacilityTag';

interface JobCardProps {
  job: JobOffer;
}

/**
 * JobCard - Purely presentational component for displaying job offers.
 * 
 * Displays:
 * - Category badge (nurse, midwife, physiotherapist, other)
 * - Job title (prominent)
 * - Meta information row (city + facility)
 * - Summary preview (concise, stored in database)
 * 
 * All data comes from props - no business logic or data generation.
 */
export default function JobCard({ job }: JobCardProps) {
  // Use summary if available, otherwise fallback to description (for backward compatibility)
  const summary = job.summary || job.description || null;
  const displaySummary = summary 
    ? (summary.length > 150 ? summary.substring(0, 150) + '...' : summary)
    : null;

  return (
    <div className="h-full block group relative">
      <Link href={`/job/${job.id}`} className="h-full block">
        <article className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-2xl p-6 cursor-pointer h-full flex flex-col transition-all duration-300 ease-out hover:scale-[1.02] hover:shadow-lg hover:shadow-gray-200/60">
        
        {/* Category Badge */}
        <div className="mb-4">
          <CategoryBadge 
            role={job.role} 
            title={job.title}
            description={job.description}
            size="sm" 
          />
        </div>
        
        {/* Job Title - Large and Prominent */}
        <h3 className="text-xl font-semibold text-[var(--color-text-primary)] mb-4 line-clamp-2 leading-tight">
          {job.title}
        </h3>
        
        {/* Meta Information Row - City and Facility */}
        <div className="flex flex-col gap-2 mb-4">
          <LocationTag city={job.city} size="sm" />
          <FacilityTag facilityName={job.facility_name} size="sm" />
        </div>
        
        {/* Summary Preview */}
        {displaySummary && (
          <p className="text-[var(--color-text-secondary)] text-sm leading-relaxed line-clamp-3 mb-0 flex-grow">
            {displaySummary}
          </p>
        )}
        </article>
      </Link>
      
      {/* External Link Button - appears on hover, positioned outside Link to avoid nesting */}
      {job.source_url && (
        <a
          href={job.source_url}
          target="_blank"
          rel="noopener noreferrer"
          className="absolute top-4 right-4 w-8 h-8 rounded-full border border-gray-300 bg-white flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-200 hover:bg-gray-50 hover:border-gray-400 z-10"
          aria-label="Otwórz źródło oferty"
        >
          <svg
            className="w-4 h-4 text-gray-600"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
            />
          </svg>
        </a>
      )}
    </div>
  );
}

