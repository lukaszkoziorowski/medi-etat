'use client';

import { useEffect, useState, useMemo } from 'react';
import { useSearchParams } from 'next/navigation';
import FiltersPanelClient from '@/components/filters/FiltersPanelClient';
import JobList from '@/components/jobs/JobList';
import LoadingState from '@/components/ui/LoadingState';
import { fetchJobs } from '@/lib/api';
import { filterJobs, parseFiltersFromURL, FilterState } from '@/lib/filterUtils';
import { JobOffer } from '@/types';

export default function JobsPageClient() {
  const [allJobs, setAllJobs] = useState<JobOffer[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const searchParams = useSearchParams();

  // Fetch all jobs on mount
  useEffect(() => {
    let cancelled = false;
    
    async function loadJobs() {
      try {
        setLoading(true);
        setError(null);
        console.log('Fetching jobs...');
        const jobsData = await fetchJobs({ limit: 1000 });
        console.log('Jobs fetched:', jobsData);
        
        if (!cancelled) {
          setAllJobs(jobsData.results || []);
        }
      } catch (err) {
        if (!cancelled) {
          const errorMessage = err instanceof Error ? err.message : 'Nie udało się załadować ofert pracy';
          setError(errorMessage);
          console.error('Error fetching jobs:', err);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadJobs();
    
    return () => {
      cancelled = true;
    };
  }, []);

  // Parse filters from URL - updates when URL changes
  const filterState: FilterState = useMemo(() => {
    try {
      const parsed = parseFiltersFromURL(searchParams);
      return {
        positions: parsed.positions || [],
        cities: parsed.cities || [],
        searchQuery: parsed.searchQuery || '',
      };
    } catch (err) {
      console.error('Error parsing filters:', err);
      return {
        positions: [],
        cities: [],
        searchQuery: '',
      };
    }
  }, [searchParams]);

  // Extract unique cities from all jobs
  const availableCities = useMemo(() => {
    return Array.from(new Set(allJobs.map((j) => j.city))).sort();
  }, [allJobs]);

  // Apply client-side filtering
  const filteredJobs = useMemo(() => {
    if (loading) return [];
    return filterJobs(allJobs, filterState);
  }, [allJobs, filterState, loading]);

  if (loading) {
    return <LoadingState />;
  }

  if (error) {
    return (
      <div className="mx-auto max-w-[var(--container-max-width)] px-[var(--container-padding)] py-8">
        <div className="text-center text-red-500 mb-4">{error}</div>
        <div className="text-center text-sm text-gray-500">
          Make sure the backend API is running on http://localhost:8000
        </div>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-[var(--container-max-width)] px-[var(--container-padding)] py-8">
      <div className="grid gap-8 lg:grid-cols-[280px_1fr]">
        <div className="lg:sticky lg:top-8 lg:h-fit">
          <FiltersPanelClient cities={availableCities} />
        </div>

        <div>
          <JobList
            jobs={filteredJobs}
            emptyMessage="Brak ofert pracy spełniających wybrane kryteria"
          />
        </div>
      </div>
    </div>
  );
}
