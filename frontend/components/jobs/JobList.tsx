import { JobOffer } from '@/types';
import JobCard from './JobCard';
import LoadingState from '../ui/LoadingState';
import EmptyState from '../ui/EmptyState';

interface JobListProps {
  jobs: JobOffer[];
  loading?: boolean;
  emptyMessage?: string;
}

export default function JobList({ jobs, loading, emptyMessage }: JobListProps) {
  if (loading) {
    return <LoadingState />;
  }

  if (jobs.length === 0) {
    return <EmptyState message={emptyMessage || 'Brak ofert pracy spełniających kryteria'} />;
  }

  return (
    <div>
      <div className="mb-6">
        <p className="text-[var(--color-text-secondary)] text-sm">
          Znaleziono <span className="font-semibold text-[var(--color-text-primary)]">{jobs.length}</span> ofert
        </p>
      </div>
      
      <div className="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-3 auto-rows-fr">
        {jobs.map((job) => (
          <JobCard key={job.id} job={job} />
        ))}
      </div>
    </div>
  );
}

