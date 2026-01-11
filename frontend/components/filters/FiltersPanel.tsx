'use client';

import { MedicalRole } from '@/types';
import Button from '../ui/Button';

interface FiltersPanelProps {
  roles: MedicalRole[];
  selectedRole: MedicalRole | null;
  cities: string[];
  selectedCity: string | null;
  onRoleChange: (role: MedicalRole | null) => void;
  onCityChange: (city: string | null) => void;
  onClear: () => void;
  isMobile?: boolean;
}

export default function FiltersPanel({
  roles,
  selectedRole,
  cities,
  selectedCity,
  onRoleChange,
  onCityChange,
  onClear,
  isMobile = false,
}: FiltersPanelProps) {
  const hasActiveFilters = selectedRole !== null || selectedCity !== null;

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
        {/* Role Filter */}
        <div>
          <label className="block text-sm font-medium text-[var(--color-text-primary)] mb-3">
            Stanowisko
          </label>
          <div className="space-y-2">
            <label className="flex items-center cursor-pointer">
              <input
                type="radio"
                name="role"
                checked={selectedRole === null}
                onChange={() => onRoleChange(null)}
                className="mr-2"
              />
              <span className="text-sm text-[var(--color-text-secondary)]">Wszystkie</span>
            </label>
            {roles.map((role) => (
              <label key={role} className="flex items-center cursor-pointer">
                <input
                  type="radio"
                  name="role"
                  checked={selectedRole === role}
                  onChange={() => onRoleChange(role)}
                  className="mr-2"
                />
                <span className="text-sm text-[var(--color-text-secondary)]">{role}</span>
              </label>
            ))}
          </div>
        </div>

        {/* City Filter */}
        {cities.length > 0 && (
          <div>
            <label className="block text-sm font-medium text-[var(--color-text-primary)] mb-3">
              Lokalizacja
            </label>
            <select
              value={selectedCity || ''}
              onChange={(e) => onCityChange(e.target.value || null)}
              className="w-full px-3 py-2 border border-[var(--color-border)] rounded-[var(--radius-md)] bg-[var(--color-bg-primary)] text-sm text-[var(--color-text-primary)] focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]"
            >
              <option value="">Wszystkie miasta</option>
              {cities.map((city) => (
                <option key={city} value={city}>
                  {city}
                </option>
              ))}
            </select>
          </div>
        )}
      </div>
    </aside>
  );
}

