export default function Footer() {
  return (
    <footer className="border-t border-[var(--color-border)] bg-[var(--color-bg-secondary)] mt-auto">
      <div className="mx-auto max-w-[var(--container-max-width)] px-[var(--container-padding)] py-6">
        <p className="text-sm text-[var(--color-text-secondary)] text-center">
          © {new Date().getFullYear()} Medietat. Oferty pracy dla personelu medycznego w Polsce.
        </p>
      </div>
    </footer>
  );
}

