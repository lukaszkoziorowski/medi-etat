import Link from 'next/link';

export default function Header() {
  return (
    <header className="border-b border-[var(--color-border)] bg-[var(--color-bg-primary)]">
      <div className="mx-auto max-w-[var(--container-max-width)] px-[var(--container-padding)] py-4">
        <Link href="/" className="text-2xl font-bold text-[var(--color-text-primary)] hover:text-[var(--color-primary)] transition-colors">
          Medietat
        </Link>
        <p className="text-sm text-[var(--color-text-secondary)] mt-1">
          Oferty pracy dla personelu medycznego
        </p>
      </div>
    </header>
  );
}

