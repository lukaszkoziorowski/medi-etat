'use client';

import { JobPositionCategory, POSITION_LABELS } from '@/lib/filterConfig';
import Button from '../ui/Button';
import GlobalSearch from './GlobalSearch';
import FilterPill from './FilterPill';

interface FiltersPanelProps {
  availableCities: string[];
  selectedPositions: JobPositionCategory[];
  selectedCities: string[];
  searchQuery: string;
  onPositionToggle: (position: JobPositionCategory) => void;
  onCityToggle: (city: string) => void;
  onSearchChange: (query: string) => void;
  onClear: () => void;
  isMobile?: boolean;
}

export default function FiltersPanel({
  availableCities,
  selectedPositions,
  selectedCities,
  searchQuery,
  onPositionToggle,
  onCityToggle,
  onSearchChange,
  onClear,
  isMobile = false,
}: FiltersPanelProps) {
  const allPositions = Object.values(JobPositionCategory);
  const hasActiveFilters =
    selectedPositions.length > 0 ||
    selectedCities.length > 0 ||
    searchQuery.trim().length > 0;

  return (
    <aside className={`bg-[var(--color-bg-secondary)] rounded-[var(--radius-lg)] p-6 ${isMobile ? 'mb-6' : ''}`}>
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

