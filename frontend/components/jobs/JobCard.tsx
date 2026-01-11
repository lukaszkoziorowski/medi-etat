import Link from 'next/link';
import { JobOffer } from '@/types';
import RoleBadge from './RoleBadge';
import LocationTag from './LocationTag';

interface JobCardProps {
  job: JobOffer;
}

export default function JobCard({ job }: JobCardProps) {
  const description = job.description 
    ? (job.description.length > 150 ? job.description.substring(0, 150) + '...' : job.description)
    : null;

  return (
    <Link href={`/job/${job.id}`}>
      <article className="bg-[var(--color-bg-primary)] border border-[var(--color-border)] rounded-[var(--radius-lg)] p-6 hover:shadow-lg transition-shadow cursor-pointer">
        <div className="flex items-start justify-between mb-3">
          <RoleBadge role={job.role} size="sm" />
        </div>
        
        <h3 className="text-xl font-semibold text-[var(--color-text-primary)] mb-2 line-clamp-2">
          {job.title}
        </h3>
        
        <p className="text-[var(--color-text-secondary)] text-sm mb-2">
          {job.facility_name}
        </p>
        
        <div className="flex items-center gap-4 mb-3">
          <LocationTag city={job.city} size="sm" />
        </div>
        
        {description && (
          <p className="text-[var(--color-text-secondary)] text-sm line-clamp-2 mt-3">
            {description}
          </p>
        )}
        
        <div className="mt-4 pt-4 border-t border-[var(--color-border-light)]">
          <span className="text-sm text-[var(--color-primary)] font-medium">
            Zobacz szczegóły →
          </span>
        </div>
      </article>
    </Link>
  );
}

