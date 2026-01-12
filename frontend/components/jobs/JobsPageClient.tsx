'use client';

import { useEffect, useState, useMemo } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import FiltersPanelClient from '@/components/filters/FiltersPanelClient';
import MobileFilterButton from '@/components/filters/MobileFilterButton';
import MobileFilterModal from '@/components/filters/MobileFilterModal';
import JobList from '@/components/jobs/JobList';
import LoadingState from '@/components/ui/LoadingState';
import { fetchJobs } from '@/lib/api';
import { filterJobs, parseFiltersFromURL, buildFiltersURL, FilterState } from '@/lib/filterUtils';
import { sortJobs, SortOption } from '@/lib/sortUtils';
import { JobOffer } from '@/types';
import { JobPositionCategory } from '@/lib/filterConfig';

export default function JobsPageClient() {
  const [allJobs, setAllJobs] = useState<JobOffer[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isMobileModalOpen, setIsMobileModalOpen] = useState(false);
  const searchParams = useSearchParams();
  const router = useRouter();

  // Function to load jobs (can be called from outside)
  const loadJobs = async () => {
    try {
      setLoading(true);
      setError(null);
      console.log('Fetching jobs...');
      const jobsData = await fetchJobs({ limit: 1000 });
      console.log('Jobs fetched:', jobsData);
      
      setAllJobs(jobsData.results || []);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Nie udało się załadować ofert pracy';
      setError(errorMessage);
      console.error('Error fetching jobs:', err);
    } finally {
      setLoading(false);
    }
  };

  // Fetch all jobs on mount
  useEffect(() => {
    loadJobs();
  }, []);

  // Listen for custom refresh event to refetch jobs
  useEffect(() => {
    const handleRefresh = () => {
      loadJobs();
    };

    window.addEventListener('jobs-refresh', handleRefresh);
    
    return () => {
      window.removeEventListener('jobs-refresh', handleRefresh);
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

  // Get sort option from URL
  const sortOption: SortOption = useMemo(() => {
    const sort = searchParams.get('sort') as SortOption;
    return sort || 'recommended';
  }, [searchParams]);

  // Extract unique cities from all jobs
  const availableCities = useMemo(() => {
    return Array.from(new Set(allJobs.map((j) => j.city))).sort();
  }, [allJobs]);

  // Apply client-side filtering and sorting
  const filteredJobs = useMemo(() => {
    if (loading) return [];
    const filtered = filterJobs(allJobs, filterState);
    return sortJobs(filtered, sortOption);
  }, [allJobs, filterState, sortOption, loading]);

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

  // Mobile filter handlers - update URL immediately
  const handleMobilePositionToggle = (position: JobPositionCategory) => {
    const newPositions = filterState.positions.includes(position)
      ? filterState.positions.filter((p) => p !== position)
      : [...filterState.positions, position];
    
    const newFilters = {
      positions: newPositions,
      cities: filterState.cities,
      searchQuery: filterState.searchQuery,
    };
    const queryString = buildFiltersURL(newFilters);
    const params = new URLSearchParams(queryString);
    if (sortOption !== 'recommended') {
      params.set('sort', sortOption);
    }
    router.push(params.toString() ? `/?${params.toString()}` : '/');
  };

  const handleMobileCityToggle = (city: string) => {
    const newCities = filterState.cities.includes(city)
      ? filterState.cities.filter((c) => c !== city)
      : [...filterState.cities, city];
    
    const newFilters = {
      positions: filterState.positions,
      cities: newCities,
      searchQuery: filterState.searchQuery,
    };
    const queryString = buildFiltersURL(newFilters);
    const params = new URLSearchParams(queryString);
    if (sortOption !== 'recommended') {
      params.set('sort', sortOption);
    }
    router.push(params.toString() ? `/?${params.toString()}` : '/');
  };

  const handleMobileSearchChange = (query: string) => {
    const newFilters = {
      positions: filterState.positions,
      cities: filterState.cities,
      searchQuery: query,
    };
    const queryString = buildFiltersURL(newFilters);
    const params = new URLSearchParams(queryString);
    if (sortOption !== 'recommended') {
      params.set('sort', sortOption);
    }
    router.push(params.toString() ? `/?${params.toString()}` : '/');
  };

  const handleMobileSortChange = (sort: SortOption) => {
    const queryString = buildFiltersURL(filterState);
    const params = new URLSearchParams(queryString);
    if (sort !== 'recommended') {
      params.set('sort', sort);
    }
    router.push(params.toString() ? `/?${params.toString()}` : '/');
  };

  const handleMobileClear = () => {
    router.push('/');
  };

  const handleMobileApply = () => {
    setIsMobileModalOpen(false);
  };

  return (
    <>
      <div className="mx-auto max-w-[var(--container-max-width)] px-[var(--container-padding)] py-8 pb-24 lg:pb-8">
        <div className="grid gap-8 lg:grid-cols-[280px_1fr]">
          {/* Desktop Filters - Hidden on mobile */}
          <div className="hidden lg:block lg:sticky lg:top-8 lg:h-fit">
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

      {/* Mobile Filter Button - Sticky Bottom */}
      <MobileFilterButton
        filterState={filterState}
        resultCount={filteredJobs.length}
        onClick={() => setIsMobileModalOpen(true)}
      />

      {/* Mobile Filter Modal */}
      <MobileFilterModal
        isOpen={isMobileModalOpen}
        onClose={() => setIsMobileModalOpen(false)}
        availableCities={availableCities}
        filterState={filterState}
        sortOption={sortOption}
        resultCount={filteredJobs.length}
        onPositionToggle={handleMobilePositionToggle}
        onCityToggle={handleMobileCityToggle}
        onSearchChange={handleMobileSearchChange}
        onSortChange={handleMobileSortChange}
        onClear={handleMobileClear}
        onApply={handleMobileApply}
      />
    </>
  );
}
