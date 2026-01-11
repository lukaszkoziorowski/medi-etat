import { MedicalRole } from '@/types';

interface RoleBadgeProps {
  role: MedicalRole;
  size?: 'sm' | 'md' | 'lg';
  variant?: 'solid' | 'outline';
}

const roleColors: Record<MedicalRole, string> = {
  [MedicalRole.LEKARZ]: 'var(--color-role-lekarz)',
  [MedicalRole.PIELĘGNIARKA]: 'var(--color-role-pielegniarka)',
  [MedicalRole.POŁOŻNA]: 'var(--color-role-polozna)',
  [MedicalRole.RATOWNIK]: 'var(--color-role-ratownik)',
  [MedicalRole.INNY]: 'var(--color-role-inny)',
};

const sizeStyles = {
  sm: 'px-2 py-0.5 text-xs',
  md: 'px-2.5 py-1 text-sm',
  lg: 'px-3 py-1.5 text-base',
};

export default function RoleBadge({ role, size = 'md', variant = 'solid' }: RoleBadgeProps) {
  const color = roleColors[role];
  
  const styles = variant === 'solid'
    ? { backgroundColor: color, color: 'white' }
    : { 
        borderColor: color, 
        color: color, 
        borderWidth: '1px',
        backgroundColor: 'transparent'
      };
  
  return (
    <span
      className={`inline-flex items-center rounded-[var(--radius-full)] font-medium ${sizeStyles[size]}`}
      style={styles}
    >
      {role}
    </span>
  );
}

