'use client';

import { useRouter, useSearchParams } from 'next/navigation';
import { JobPositionCategory } from '@/lib/filterConfig';
import { parseFiltersFromURL, buildFiltersURL } from '@/lib/filterUtils';
import { SortOption } from '@/lib/sortUtils';
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
  const sortOption = (searchParams.get('sort') as SortOption) || 'recommended';

  const updateFilters = (
    positions: JobPositionCategory[],
    cities: string[],
    search: string,
    sort: SortOption = 'recommended'
  ) => {
    const newFilters = {
      positions,
      cities,
      searchQuery: search,
    };

    const queryString = buildFiltersURL(newFilters);
    const params = new URLSearchParams(queryString);
    if (sort && sort !== 'recommended') {
      params.set('sort', sort);
    }
    
    const finalQuery = params.toString();
    router.push(finalQuery ? `/?${finalQuery}` : '/');
  };

  const handlePositionToggle = (position: JobPositionCategory) => {
    const newPositions = selectedPositions.includes(position)
      ? selectedPositions.filter((p) => p !== position)
      : [...selectedPositions, position];

    updateFilters(newPositions, selectedCities, searchQuery, sortOption);
  };

  const handleCityToggle = (city: string) => {
    const newCities = selectedCities.includes(city)
      ? selectedCities.filter((c) => c !== city)
      : [...selectedCities, city];

    updateFilters(selectedPositions, newCities, searchQuery, sortOption);
  };

  const handleSearchChange = (query: string) => {
    updateFilters(selectedPositions, selectedCities, query, sortOption);
  };

  const handleSortChange = (sort: SortOption) => {
    updateFilters(selectedPositions, selectedCities, searchQuery, sort);
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
      sortOption={sortOption}
      onPositionToggle={handlePositionToggle}
      onCityToggle={handleCityToggle}
      onSearchChange={handleSearchChange}
      onSortChange={handleSortChange}
      onClear={handleClear}
    />
  );
}

