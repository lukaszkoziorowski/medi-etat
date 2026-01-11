'use client';

import { useRouter, useSearchParams } from 'next/navigation';
import { MedicalRole } from '@/types';
import FiltersPanel from './FiltersPanel';

interface FiltersPanelClientProps {
  roles: MedicalRole[];
  cities: string[];
}

export default function FiltersPanelClient({ roles, cities }: FiltersPanelClientProps) {
  const router = useRouter();
  const searchParams = useSearchParams();
  
  const selectedRole = searchParams.get('role') as MedicalRole | null;
  const selectedCity = searchParams.get('city');

  const updateFilters = (newRole: MedicalRole | null, newCity: string | null) => {
    const params = new URLSearchParams();
    
    if (newRole) {
      params.set('role', newRole);
    }
    if (newCity) {
      params.set('city', newCity);
    }
    
    const queryString = params.toString();
    router.push(queryString ? `/?${queryString}` : '/');
  };

  const handleRoleChange = (role: MedicalRole | null) => {
    updateFilters(role, selectedCity);
  };

  const handleCityChange = (city: string | null) => {
    updateFilters(selectedRole, city);
  };

  const handleClear = () => {
    router.push('/');
  };

  return (
    <FiltersPanel
      roles={roles}
      selectedRole={selectedRole}
      cities={cities}
      selectedCity={selectedCity}
      onRoleChange={handleRoleChange}
      onCityChange={handleCityChange}
      onClear={handleClear}
    />
  );
}

