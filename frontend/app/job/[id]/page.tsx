import { notFound } from 'next/navigation';
import Link from 'next/link';
import Layout from '@/components/layout/Layout';
import RoleBadge from '@/components/jobs/RoleBadge';
import LocationTag from '@/components/jobs/LocationTag';
import Button from '@/components/ui/Button';
import { fetchJob } from '@/lib/api';

interface JobDetailPageProps {
  params: Promise<{ id: string }>;
}

export default async function JobDetailPage({ params }: JobDetailPageProps) {
  const { id } = await params;
  const jobId = parseInt(id);
  
  if (isNaN(jobId)) {
    notFound();
  }

  let job;
  try {
    job = await fetchJob(jobId);
  } catch (error) {
    notFound();
  }

  return (
    <Layout>
      <div className="mx-auto max-w-[var(--container-max-width)] px-[var(--container-padding)] py-8">
        <Link 
          href="/"
          className="inline-flex items-center text-sm text-[var(--color-text-secondary)] hover:text-[var(--color-primary)] mb-6 transition-colors"
        >
          ← Powrót do listy ofert
        </Link>

        <article className="bg-[var(--color-bg-primary)] border border-[var(--color-border)] rounded-[var(--radius-lg)] p-8">
          <div className="mb-6">
            <RoleBadge role={job.role} size="md" />
          </div>

          <h1 className="text-3xl font-bold text-[var(--color-text-primary)] mb-4">
            {job.title}
          </h1>

          <div className="space-y-3 mb-6">
            <div>
              <span className="text-sm font-medium text-[var(--color-text-secondary)]">Placówka: </span>
              <span className="text-[var(--color-text-primary)]">{job.facility_name}</span>
            </div>
            <div>
              <LocationTag city={job.city} size="md" />
            </div>
          </div>

          {job.description && (
            <div className="mb-8">
              <h2 className="text-lg font-semibold text-[var(--color-text-primary)] mb-3">
                Opis
              </h2>
              <div className="prose prose-sm max-w-none text-[var(--color-text-primary)] whitespace-pre-wrap">
                {job.description}
              </div>
            </div>
          )}

          <div className="border-t border-[var(--color-border)] pt-6 mt-6">
            <a
              href={job.source_url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block"
            >
              <Button variant="primary" size="lg">
                Zobacz ofertę na stronie źródłowej →
              </Button>
            </a>
            <p className="text-xs text-[var(--color-text-muted)] mt-2">
              Link otworzy się w nowej karcie
            </p>
          </div>
        </article>
      </div>
    </Layout>
  );
}

