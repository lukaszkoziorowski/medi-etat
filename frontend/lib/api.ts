/**
 * API client for fetching job offers
 */

import { JobsResponse, JobOffer, MedicalRole } from '@/types';

// Use environment variable for API URL (set in Vercel) or default to localhost for development
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function fetchJobs(params?: {
  role?: MedicalRole | null;
  limit?: number;
  offset?: number;
}): Promise<JobsResponse> {
  const searchParams = new URLSearchParams();
  
  if (params?.role) {
    searchParams.append('role', params.role);
  }
  if (params?.limit) {
    searchParams.append('limit', params.limit.toString());
  }
  if (params?.offset) {
    searchParams.append('offset', params.offset.toString());
  }

  const queryString = searchParams.toString();
  const url = `${API_BASE_URL}/api/jobs${queryString ? `?${queryString}` : ''}`;
  
  console.log('Fetching from URL:', url);
  
  const response = await fetch(url, {
    cache: 'no-store',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  console.log('Response status:', response.status, response.statusText);

  if (!response.ok) {
    const errorText = await response.text();
    console.error('API Error:', errorText);
    throw new Error(`Failed to fetch jobs: ${response.status} ${response.statusText}`);
  }

  const data = await response.json();
  console.log('API Response:', data);
  return data;
}

export async function fetchJob(id: number): Promise<JobOffer> {
  const response = await fetch(`${API_BASE_URL}/api/jobs/${id}`, {
    cache: 'no-store',
  });

  if (!response.ok) {
    throw new Error('Failed to fetch job');
  }

  return response.json();
}

