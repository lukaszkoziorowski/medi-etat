'use client';

import { useState, useEffect, useRef } from 'react';
import { useDebounce } from '@/hooks/useDebounce';

interface GlobalSearchProps {
  value: string;
  onChange: (query: string) => void;
  placeholder?: string;
}

export default function GlobalSearch({
  value,
  onChange,
  placeholder = 'Szukaj w tytułach i opisach...',
}: GlobalSearchProps) {
  const [localValue, setLocalValue] = useState(value || '');
  const debouncedValue = useDebounce(localValue, 300);
  const onChangeRef = useRef(onChange);
  const isExternalUpdate = useRef(false);

  // Keep onChange ref updated
  useEffect(() => {
    onChangeRef.current = onChange;
  }, [onChange]);

  // Notify parent of debounced value changes (only if it's a user input, not external update)
  useEffect(() => {
    if (!isExternalUpdate.current) {
      onChangeRef.current(debouncedValue);
    }
  }, [debouncedValue]);

  // Sync with external value changes (e.g., when filters are cleared)
  useEffect(() => {
    if (value !== localValue) {
      isExternalUpdate.current = true;
      setLocalValue(value || '');
      // Reset flag after state update
      setTimeout(() => {
        isExternalUpdate.current = false;
      }, 0);
    }
  }, [value]);

  return (
    <div className="mb-6">
      <input
        type="text"
        value={localValue}
        onChange={(e) => {
          setLocalValue(e.target.value);
          isExternalUpdate.current = false;
        }}
        placeholder={placeholder}
        className="w-full px-4 py-2.5 border border-[var(--color-border)] rounded-[var(--radius-md)] bg-[var(--color-surface)] text-sm text-[var(--color-text-primary)] placeholder:text-[var(--color-text-secondary)] focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)] transition-all"
      />
    </div>
  );
}
