'use client';

import { JobPositionCategory, POSITION_LABELS } from '@/lib/filterConfig';
import Button from '../ui/Button';
import GlobalSearch from './GlobalSearch';

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

        {/* Position Filter - Multi-select checkboxes */}
        <div>
          <label className="block text-sm font-medium text-[var(--color-text-primary)] mb-3">
            Stanowisko
          </label>
          <div className="space-y-2">
            {allPositions.map((position) => {
              const isChecked = selectedPositions.includes(position);
              return (
                <label
                  key={position}
                  className="flex items-center cursor-pointer hover:bg-[var(--color-bg-primary)] p-2 rounded transition-colors"
                >
                  <input
                    type="checkbox"
                    checked={isChecked}
                    onChange={() => onPositionToggle(position)}
                    className="mr-2 w-4 h-4 text-[var(--color-primary)] border-[var(--color-border)] rounded focus:ring-[var(--color-primary)]"
                  />
                  <span className="text-sm text-[var(--color-text-secondary)]">
                    {POSITION_LABELS[position]}
                  </span>
                </label>
              );
            })}
          </div>
        </div>

        {/* City Filter - Multi-select checkboxes */}
        {availableCities.length > 0 && (
          <div>
            <label className="block text-sm font-medium text-[var(--color-text-primary)] mb-3">
              Lokalizacja
            </label>
            <div className="space-y-2 max-h-64 overflow-y-auto">
              {availableCities.map((city) => {
                const isChecked = selectedCities.includes(city);
                return (
                  <label
                    key={city}
                    className="flex items-center cursor-pointer hover:bg-[var(--color-bg-primary)] p-2 rounded transition-colors"
                  >
                    <input
                      type="checkbox"
                      checked={isChecked}
                      onChange={() => onCityToggle(city)}
                      className="mr-2 w-4 h-4 text-[var(--color-primary)] border-[var(--color-border)] rounded focus:ring-[var(--color-primary)]"
                    />
                    <span className="text-sm text-[var(--color-text-secondary)]">{city}</span>
                  </label>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </aside>
  );
}

