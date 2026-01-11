import { Suspense } from 'react';
import Layout from '@/components/layout/Layout';
import LoadingState from '@/components/ui/LoadingState';
import JobsPageClient from '@/components/jobs/JobsPageClient';

export default function HomePage() {
  return (
    <Layout>
      <Suspense fallback={<LoadingState />}>
        <JobsPageClient />
      </Suspense>
    </Layout>
  );
}
