import { Suspense } from 'react';
import Layout from '@/components/layout/Layout';
import FiltersPanelClient from '@/components/filters/FiltersPanelClient';
import JobList from '@/components/jobs/JobList';
import LoadingState from '@/components/ui/LoadingState';
import { fetchJobs } from '@/lib/api';
import { MedicalRole } from '@/types';

interface HomePageProps {
  searchParams: Promise<{ role?: string; city?: string }>;
}

async function JobsContent({ searchParams }: HomePageProps) {
  const params = await searchParams;
  const role = params.role as MedicalRole | undefined;
  const city = params.city;

  const jobsData = await fetchJobs({
    role: role || null,
    limit: 100,
  });

  // Extract unique roles and cities from jobs
  const availableRoles = Array.from(new Set(jobsData.results.map(j => j.role)));
  const availableCities = Array.from(new Set(jobsData.results.map(j => j.city))).sort();

  // Filter by city on client side (since backend doesn't support it yet)
  const filteredJobs = city
    ? jobsData.results.filter(job => job.city === city)
    : jobsData.results;

  return (
    <div className="mx-auto max-w-[var(--container-max-width)] px-[var(--container-padding)] py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-[var(--color-text-primary)] mb-2">
          Oferty pracy dla personelu medycznego
        </h1>
        <p className="text-[var(--color-text-secondary)]">
          Znajdź pracę w placówkach medycznych w Polsce
        </p>
      </div>

      <div className="grid gap-8 lg:grid-cols-[280px_1fr]">
        <div className="lg:sticky lg:top-8 lg:h-fit">
          <FiltersPanelClient
            roles={availableRoles}
            cities={availableCities}
          />
        </div>

        <div>
          <JobList 
            jobs={filteredJobs} 
            emptyMessage="Brak ofert pracy spełniających wybrane kryteria"
          />
        </div>
      </div>
    </div>
  );
}

export default function HomePage({ searchParams }: HomePageProps) {
  return (
    <Layout>
      <Suspense fallback={<LoadingState />}>
        <JobsContent searchParams={searchParams} />
      </Suspense>
    </Layout>
  );
}
