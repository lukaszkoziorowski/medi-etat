interface LoadingStateProps {
  message?: string;
}

export default function LoadingState({ message = 'Ładowanie ofert...' }: LoadingStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[var(--color-primary)] mb-4"></div>
      <p className="text-[var(--color-text-secondary)]">{message}</p>
    </div>
  );
}

