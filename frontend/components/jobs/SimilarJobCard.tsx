import Link from 'next/link';
import { JobOffer } from '@/types';
import CategoryBadge from './CategoryBadge';
import LocationTag from './LocationTag';

interface SimilarJobCardProps {
  job: JobOffer;
}

/**
 * Compact job card for similar jobs section
 */
export default function SimilarJobCard({ job }: SimilarJobCardProps) {
  const summary = job.summary || job.description || null;
  const displaySummary = summary 
    ? (summary.length > 80 ? summary.substring(0, 80) + '...' : summary)
    : null;

  return (
    <Link href={`/job/${job.id}`} className="block">
      <article className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-2xl p-4 hover:border-[var(--color-primary)] hover:shadow-sm transition-all duration-200">
        <div className="mb-2">
          <CategoryBadge 
            role={job.role} 
            title={job.title}
            description={job.description}
            size="sm" 
          />
        </div>
        
        <h3 className="text-sm font-semibold text-[var(--color-text-primary)] mb-2 line-clamp-2 leading-tight">
          {job.title}
        </h3>
        
        <div className="mb-2">
          <LocationTag city={job.city} size="sm" />
        </div>
        
        {displaySummary && (
          <p className="text-xs text-[var(--color-text-secondary)] line-clamp-2 leading-relaxed">
            {displaySummary}
          </p>
        )}
      </article>
    </Link>
  );
}
