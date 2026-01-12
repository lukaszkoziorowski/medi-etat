'use client';

import { JobPositionCategory, POSITION_LABELS } from '@/lib/filterConfig';
import { SortOption } from '@/lib/sortUtils';
import Button from '../ui/Button';
import GlobalSearch from './GlobalSearch';
import FilterPill from './FilterPill';

interface FiltersPanelProps {
  availableCities: string[];
  selectedPositions: JobPositionCategory[];
  selectedCities: string[];
  searchQuery: string;
  sortOption: SortOption;
  onPositionToggle: (position: JobPositionCategory) => void;
  onCityToggle: (city: string) => void;
  onSearchChange: (query: string) => void;
  onSortChange: (sort: SortOption) => void;
  onClear: () => void;
  isMobile?: boolean;
}

export default function FiltersPanel({
  availableCities,
  selectedPositions,
  selectedCities,
  searchQuery,
  sortOption,
  onPositionToggle,
  onCityToggle,
  onSearchChange,
  onSortChange,
  onClear,
  isMobile = false,
}: FiltersPanelProps) {
  const allPositions = Object.values(JobPositionCategory);
  const hasActiveFilters =
    selectedPositions.length > 0 ||
    selectedCities.length > 0 ||
    searchQuery.trim().length > 0;

  return (
    <aside className={`bg-transparent rounded-[var(--radius-lg)] p-0 ${isMobile ? 'mb-6' : ''}`}>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-semibold text-[var(--color-text-primary)]">Filtry</h2>
        {hasActiveFilters && (
          <Button onClick={onClear} variant="ghost" size="sm">
            Wyczyść
          </Button>
        )}
      </div>

      <div className="space-y-6">
        {/* Global Search */}
        <GlobalSearch value={searchQuery} onChange={onSearchChange} />

        {/* Sort Select */}
        <div>
          <label className="block text-sm font-medium text-[var(--color-text-primary)] mb-3">
            Sortuj wyniki
          </label>
          <div className="relative">
            <select
              value={sortOption}
              onChange={(e) => onSortChange(e.target.value as SortOption)}
              className="w-full pl-4 pr-10 py-2.5 border border-[var(--color-border)] rounded-[var(--radius-md)] bg-[var(--color-surface)] text-sm text-[var(--color-text-primary)] focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)] transition-all appearance-none"
            >
              <option value="recommended">Rekomendowane</option>
              <option value="a-z">A-Z</option>
              <option value="z-a">Z-A</option>
            </select>
            <div className="absolute inset-y-0 right-0 flex items-center pr-4 pointer-events-none">
              <svg
                className="w-4 h-4 text-[var(--color-text-secondary)]"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 9l-7 7-7-7"
                />
              </svg>
            </div>
          </div>
        </div>

        {/* Position Filter - Pill components */}
        <div>
          <label className="block text-sm font-medium text-[var(--color-text-primary)] mb-3">
            Stanowisko
          </label>
          <div className="flex flex-wrap gap-2">
            {allPositions.map((position) => {
              const isSelected = selectedPositions.includes(position);
              return (
                <FilterPill
                  key={position}
                  label={POSITION_LABELS[position]}
                  isSelected={isSelected}
                  onClick={() => onPositionToggle(position)}
                />
              );
            })}
          </div>
        </div>

        {/* City Filter - Pill components */}
        {availableCities.length > 0 && (
          <div>
            <label className="block text-sm font-medium text-[var(--color-text-primary)] mb-3">
              Lokalizacja
            </label>
            <div className="flex flex-wrap gap-2 max-h-64 overflow-y-auto">
              {availableCities.map((city) => {
                const isSelected = selectedCities.includes(city);
                return (
                  <FilterPill
                    key={city}
                    label={city}
                    isSelected={isSelected}
                    onClick={() => onCityToggle(city)}
                  />
                );
              })}
            </div>
          </div>
        )}
      </div>
    </aside>
  );
}

