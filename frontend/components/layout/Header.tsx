import Link from 'next/link';
import Image from 'next/image';

export default function Header() {
  return (
    <header className="border-b border-[var(--color-border)] bg-[var(--color-bg-primary)]">
      <div className="mx-auto max-w-[var(--container-max-width)] px-[var(--container-padding)] py-4">
        <div className="flex items-center justify-between">
          <Link href="/" className="flex items-center hover:opacity-80 transition-opacity">
            <Image
              src="/logo.svg"
              alt="Medietat"
              width={110}
              height={20}
              className="h-5 w-auto"
              priority
            />
          </Link>
        </div>
      </div>
    </header>
  );
}

