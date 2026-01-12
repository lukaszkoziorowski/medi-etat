import { notFound } from 'next/navigation';
import Link from 'next/link';
import Layout from '@/components/layout/Layout';
import JobDetailClient from '@/components/jobs/JobDetailClient';
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

        <JobDetailClient job={job} />
      </div>
    </Layout>
  );
}
