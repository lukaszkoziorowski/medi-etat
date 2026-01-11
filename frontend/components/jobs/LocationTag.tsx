interface LocationTagProps {
  city: string;
  size?: 'sm' | 'md';
}

export default function LocationTag({ city, size = 'md' }: LocationTagProps) {
  const sizeStyles = size === 'sm' ? 'text-xs' : 'text-sm';
  
  return (
    <span className={`inline-flex items-center gap-1 text-[var(--color-text-secondary)] ${sizeStyles}`}>
      <span>📍</span>
      <span>{city}</span>
    </span>
  );
}

