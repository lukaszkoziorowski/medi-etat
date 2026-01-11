import Button from './Button';

interface EmptyStateProps {
  message?: string;
  actionLabel?: string;
  onAction?: () => void;
}

export default function EmptyState({ 
  message = 'Brak ofert pracy', 
  actionLabel = 'Wyczyść filtry',
  onAction 
}: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <div className="text-6xl mb-4">🔍</div>
      <h3 className="text-xl font-semibold text-[var(--color-text-primary)] mb-2">
        {message}
      </h3>
      <p className="text-[var(--color-text-secondary)] mb-6 max-w-md">
        Spróbuj zmienić kryteria wyszukiwania lub wyczyść filtry, aby zobaczyć wszystkie oferty.
      </p>
      {onAction && (
        <Button onClick={onAction} variant="outline">
          {actionLabel}
        </Button>
      )}
    </div>
  );
}

