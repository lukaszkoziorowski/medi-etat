'use client';

import { useRouter, useSearchParams } from 'next/navigation';
import { JobPositionCategory } from '@/lib/filterConfig';
import { parseFiltersFromURL, buildFiltersURL } from '@/lib/filterUtils';
import FiltersPanel from './FiltersPanel';

interface FiltersPanelClientProps {
  cities: string[];
}

export default function FiltersPanelClient({ cities }: FiltersPanelClientProps) {
  const router = useRouter();
  const searchParams = useSearchParams();

  // Parse current filter state from URL
  const currentFilters = parseFiltersFromURL(searchParams);
  const selectedPositions = currentFilters.positions || [];
  const selectedCities = currentFilters.cities || [];
  const searchQuery = currentFilters.searchQuery || '';

  const updateFilters = (
    positions: JobPositionCategory[],
    cities: string[],
    search: string
  ) => {
    const newFilters = {
      positions,
      cities,
      searchQuery: search,
    };

    const queryString = buildFiltersURL(newFilters);
    router.push(queryString ? `/?${queryString}` : '/');
  };

  const handlePositionToggle = (position: JobPositionCategory) => {
    const newPositions = selectedPositions.includes(position)
      ? selectedPositions.filter((p) => p !== position)
      : [...selectedPositions, position];

    updateFilters(newPositions, selectedCities, searchQuery);
  };

  const handleCityToggle = (city: string) => {
    const newCities = selectedCities.includes(city)
      ? selectedCities.filter((c) => c !== city)
      : [...selectedCities, city];

    updateFilters(selectedPositions, newCities, searchQuery);
  };

  const handleSearchChange = (query: string) => {
    updateFilters(selectedPositions, selectedCities, query);
  };

  const handleClear = () => {
    router.push('/');
  };

  return (
    <FiltersPanel
      availableCities={cities}
      selectedPositions={selectedPositions}
      selectedCities={selectedCities}
      searchQuery={searchQuery}
      onPositionToggle={handlePositionToggle}
      onCityToggle={handleCityToggle}
      onSearchChange={handleSearchChange}
      onClear={handleClear}
    />
  );
}

