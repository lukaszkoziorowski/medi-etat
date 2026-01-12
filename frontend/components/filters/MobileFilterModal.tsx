'use client';

import { useEffect } from 'react';
import { JobPositionCategory, POSITION_LABELS } from '@/lib/filterConfig';
import { SortOption } from '@/lib/sortUtils';
import { FilterState } from '@/lib/filterUtils';
import Button from '../ui/Button';
import GlobalSearch from './GlobalSearch';
import FilterPill from './FilterPill';

interface MobileFilterModalProps {
  isOpen: boolean;
  onClose: () => void;
  availableCities: string[];
  filterState: FilterState;
  sortOption: SortOption;
  resultCount: number;
  onPositionToggle: (position: JobPositionCategory) => void;
  onCityToggle: (city: string) => void;
  onSearchChange: (query: string) => void;
  onSortChange: (sort: SortOption) => void;
  onClear: () => void;
  onApply: () => void;
}

/**
 * Mobile filter modal with scrollable content
 */
export default function MobileFilterModal({
  isOpen,
  onClose,
  availableCities,
  filterState,
  sortOption,
  resultCount,
  onPositionToggle,
  onCityToggle,
  onSearchChange,
  onSortChange,
  onClear,
  onApply,
}: MobileFilterModalProps) {
  // Prevent body scroll when modal is open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [isOpen]);

  // Don't return null - keep in DOM for animation

  const hasActiveFilters =
    filterState.positions.length > 0 ||
    filterState.cities.length > 0 ||
    filterState.searchQuery.trim().length > 0;

  const allPositions = Object.values(JobPositionCategory);

  return (
    <div 
      className={`lg:hidden fixed inset-0 z-50 ${isOpen ? '' : 'pointer-events-none'}`}
    >
      {/* Backdrop */}
      <div
        className={`absolute inset-0 bg-black transition-opacity duration-300 ${
          isOpen ? 'opacity-50' : 'opacity-0'
        }`}
        onClick={onClose}
      />

      {/* Modal */}
      <div
        className={`absolute inset-0 flex flex-col bg-[var(--color-bg-primary)] transition-transform duration-300 ease-out ${
          isOpen ? 'translate-y-0' : 'translate-y-full'
        }`}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-[var(--color-border)] bg-[var(--color-surface)] flex-shrink-0">
          <button
            onClick={onClose}
            className="p-2 -ml-2 hover:bg-[var(--color-bg-secondary)] rounded-[var(--radius-md)] transition-colors"
            aria-label="Zamknij"
          >
            <svg
              className="w-6 h-6 text-[var(--color-text-primary)]"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
          <h2 className="text-lg font-semibold text-[var(--color-text-primary)]">
            Filtry
          </h2>
          {hasActiveFilters && (
            <Button onClick={onClear} variant="ghost" size="sm" className="text-red-600 hover:text-red-700">
              Wyczyść
            </Button>
          )}
          {!hasActiveFilters && <div className="w-16" />}
        </div>

        {/* Scrollable Content */}
        <div className="flex-1 overflow-y-auto">
          <div className="p-4 space-y-6">
            {/* Global Search */}
            <div>
              <GlobalSearch value={filterState.searchQuery} onChange={onSearchChange} />
            </div>

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

            {/* Position Filter */}
            <div>
              <label className="block text-sm font-medium text-[var(--color-text-primary)] mb-3">
                Stanowisko
              </label>
              <div className="flex flex-wrap gap-2">
                {allPositions.map((position) => {
                  const isSelected = filterState.positions.includes(position);
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

            {/* City Filter */}
            {availableCities.length > 0 && (
              <div>
                <label className="block text-sm font-medium text-[var(--color-text-primary)] mb-3">
                  Lokalizacja
                </label>
                <div className="flex flex-wrap gap-2">
                  {availableCities.map((city) => {
                    const isSelected = filterState.cities.includes(city);
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
        </div>

        {/* Footer with Apply Button */}
        <div className="p-4 border-t border-[var(--color-border)] bg-[var(--color-surface)] flex-shrink-0">
          <Button
            onClick={onApply}
            variant="primary"
            size="lg"
            className="w-full"
          >
            Pokaż {resultCount.toLocaleString('pl-PL')} ofert
          </Button>
        </div>
      </div>
    </div>
  );
}
