'use client';

import { useEffect, useState } from 'react';
import JobList from '@/components/jobs/JobList';
import LoadingState from '@/components/ui/LoadingState';
import { fetchJobs } from '@/lib/api';
import { JobOffer } from '@/types';

/**
 * Simplified version for debugging
 */
export default function JobsPageClientSimple() {
  const [allJobs, setAllJobs] = useState<JobOffer[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadJobs() {
      try {
        console.log('Simple: Fetching jobs...');
        const jobsData = await fetchJobs({ limit: 100 });
        console.log('Simple: Jobs fetched:', jobsData);
        setAllJobs(jobsData.results || []);
        setError(null);
      } catch (err) {
        console.error('Simple: Error:', err);
        setError(err instanceof Error ? err.message : 'Failed to load');
      } finally {
        setLoading(false);
      }
    }

    loadJobs();
  }, []);

  if (loading) {
    return <LoadingState />;
  }

  if (error) {
    return (
      <div className="p-8">
        <div className="text-red-500">Error: {error}</div>
        <div className="mt-4 text-sm text-gray-500">
          Make sure the backend is running on http://localhost:8000
        </div>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-[var(--container-max-width)] px-[var(--container-padding)] py-8">
      <div className="mb-4">
        <h1 className="text-2xl font-bold">Jobs ({allJobs.length})</h1>
      </div>
      <JobList jobs={allJobs} />
    </div>
  );
}
