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
    <Link href={`/job/${job.id}`} className="h-full block">
      <article className="bg-[var(--color-bg-primary)] border border-[var(--color-border)] rounded-[var(--radius-lg)] p-6 hover:shadow-lg transition-shadow cursor-pointer h-full flex flex-col">
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
  );
}

