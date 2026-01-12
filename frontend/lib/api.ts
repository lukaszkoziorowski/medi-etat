/**
 * API client for fetching job offers
 */

import { JobsResponse, JobOffer, MedicalRole } from '@/types';

// Use environment variable for API URL (set in Vercel) or default to localhost for development
// Note: NEXT_PUBLIC_* variables are embedded at build time in Next.js
let API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Remove trailing slash if present to avoid double slashes
API_BASE_URL = API_BASE_URL.replace(/\/+$/, '');

// Log the API URL being used (for debugging)
if (typeof window !== 'undefined') {
  console.log('API Base URL:', API_BASE_URL);
}

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
  // Ensure we don't have double slashes
  const url = `${API_BASE_URL}/api/jobs${queryString ? `?${queryString}` : ''}`.replace(/([^:]\/)\/+/g, '$1');
  
  console.log('Fetching from URL:', url);
  
  const response = await fetch(url, {
    cache: 'no-store',
    headers: {
      'Content-Type': 'application/json',
    },
    mode: 'cors',  // Explicitly enable CORS
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
  // Ensure no double slashes
  const url = `${API_BASE_URL}/api/jobs/${id}`.replace(/([^:]\/)\/+/g, '$1');
  const response = await fetch(url, {
    cache: 'no-store',
  });

  if (!response.ok) {
    throw new Error('Failed to fetch job');
  }

  return response.json();
}

