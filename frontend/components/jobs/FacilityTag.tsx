interface FacilityTagProps {
  facilityName: string;
  size?: 'sm' | 'md';
}

export default function FacilityTag({ facilityName, size = 'sm' }: FacilityTagProps) {
  const sizeClasses = size === 'sm' 
    ? 'text-sm'
    : 'text-base';
  
  return (
    <div className={`flex items-center gap-1.5 text-[var(--color-text-secondary)] ${sizeClasses}`}>
      <svg
        className="w-4 h-4 flex-shrink-0"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
        aria-hidden="true"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"
        />
      </svg>
      <span className="truncate">{facilityName}</span>
    </div>
  );
}
