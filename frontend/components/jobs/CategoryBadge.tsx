import { JobPositionCategory, getCategoryForRole, POSITION_LABELS } from '@/lib/filterConfig';
import { JobOffer, MedicalRole } from '@/types';

interface CategoryBadgeProps {
  role: MedicalRole;
  title?: string; // Optional: for enhanced physiotherapist detection
  description?: string | null; // Optional: for enhanced physiotherapist detection
  size?: 'sm' | 'md';
}

export default function CategoryBadge({ role, title, description, size = 'sm' }: CategoryBadgeProps) {
  let category = getCategoryForRole(role);
  
  // Enhanced detection: check title/description for physiotherapist
  // even if role is "INNY" (same logic as filterUtils)
  if (category === JobPositionCategory.OTHER && (title || description)) {
    const text = `${title || ''} ${description || ''}`.toLowerCase();
    if (
      text.includes('fizjoterapeuta') ||
      text.includes('fizjoterapeutka') ||
      text.includes('fizjoterapeut') ||
      text.includes('physiotherapist')
    ) {
      category = JobPositionCategory.PHYSIOTHERAPIST;
    }
  }
  
  const label = POSITION_LABELS[category];
  
  // Color mapping for categories
  const categoryColors: Record<JobPositionCategory, string> = {
    [JobPositionCategory.NURSE]: 'bg-blue-100 text-blue-800 border-blue-200',
    [JobPositionCategory.MIDWIFE]: 'bg-pink-100 text-pink-800 border-pink-200',
    [JobPositionCategory.PHYSIOTHERAPIST]: 'bg-green-100 text-green-800 border-green-200',
    [JobPositionCategory.OTHER]: 'bg-gray-100 text-gray-800 border-gray-200',
  };
  
  const sizeClasses = size === 'sm' 
    ? 'text-xs px-2 py-1'
    : 'text-sm px-3 py-1.5';
  
  return (
    <span
      className={`inline-flex items-center font-medium rounded-[var(--radius-md)] border ${categoryColors[category]} ${sizeClasses}`}
    >
      {label}
    </span>
  );
}
