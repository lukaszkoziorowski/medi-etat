'use client';

import { useState } from 'react';
import { FilterState } from '@/lib/filterUtils';

interface MobileFilterButtonProps {
  filterState: FilterState;
  resultCount: number;
  onClick: () => void;
}

/**
 * Sticky mobile filter button that appears at the bottom of the viewport
 */
export default function MobileFilterButton({
  filterState,
  resultCount,
  onClick,
}: MobileFilterButtonProps) {
  const hasActiveFilters =
    filterState.positions.length > 0 ||
    filterState.cities.length > 0 ||
    filterState.searchQuery.trim().length > 0;

  const filterCount =
    filterState.positions.length + filterState.cities.length + (filterState.searchQuery.trim() ? 1 : 0);

  return (
    <>
      {/* Gradient overlay */}
      <div 
        className="lg:hidden fixed bottom-0 left-0 right-0 z-30 pointer-events-none"
        style={{
          height: '120px',
          background: 'linear-gradient(358deg, rgba(255, 255, 255, 1) 0%, rgba(255, 255, 255, 0) 100%)',
        }}
      />
      
      {/* Button container */}
      <div className="lg:hidden fixed bottom-0 left-0 right-0 z-40 p-4">
        <button
          onClick={onClick}
          className="w-full bg-[var(--color-button-surface)] text-[var(--color-button-text)] py-3 px-4 rounded-[var(--radius-md)] font-medium flex items-center justify-between hover:opacity-90 transition-opacity shadow-lg"
        >
        <div className="flex items-center gap-2">
          <svg
            className="w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"
            />
          </svg>
          <span>Filtry</span>
          {hasActiveFilters && (
            <span className="bg-[var(--color-button-text)] text-[var(--color-button-surface)] text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center">
              {filterCount}
            </span>
          )}
        </div>
        <span className="text-sm opacity-90">
          Pokaż {resultCount.toLocaleString('pl-PL')} ofert
        </span>
        </button>
      </div>
    </>
  );
}
