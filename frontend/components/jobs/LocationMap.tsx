'use client';

import { JobOffer } from '@/types';

interface LocationMapProps {
  job: JobOffer;
}

/**
 * Location map widget showing the medical facility location
 * Uses Google Maps Embed API via iframe
 */
export default function LocationMap({ job }: LocationMapProps) {
  // Construct search query for Google Maps
  const searchQuery = encodeURIComponent(`${job.facility_name}, ${job.city}, Polska`);
  const searchUrl = `https://www.google.com/maps/search/?api=1&query=${searchQuery}`;
  
  // Google Maps embed URL (works without API key for basic embeds)
  // Using the embed endpoint with place search
  const embedUrl = `https://www.google.com/maps/embed/v1/place?key=AIzaSyBFw0Qbyq9zTFTd-tUY6d-s6U4uY3Y&q=${searchQuery}`;
  
  // Fallback: Use a direct Google Maps URL that can be embedded
  // Note: Google Maps embed may require API key for production use
  // For now, using a search-based embed approach
  const mapEmbedUrl = `https://maps.google.com/maps?q=${searchQuery}&output=embed`;
  
  return (
    <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-2xl p-6 mb-8">
      <h2 className="text-xl font-semibold text-[var(--color-text-primary)] mb-4">
        Lokalizacja
      </h2>
      
      <div className="relative w-full h-64 rounded-[var(--radius-md)] overflow-hidden border border-[var(--color-border)] mb-4">
        <iframe
          width="100%"
          height="100%"
          style={{ border: 0 }}
          loading="lazy"
          allowFullScreen
          referrerPolicy="no-referrer-when-downgrade"
          src={mapEmbedUrl}
          title={`Lokalizacja ${job.facility_name}`}
          className="w-full h-full"
        />
      </div>
      
      <div className="flex items-center gap-2 text-sm text-[var(--color-text-secondary)]">
        <svg
          className="w-4 h-4 flex-shrink-0"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
          />
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
          />
        </svg>
        <span>{job.facility_name}, {job.city}</span>
      </div>
      
      <a
        href={searchUrl}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-flex items-center gap-2 text-sm text-[var(--color-primary)] hover:text-[var(--color-primary-dark)] mt-3 transition-colors"
      >
        <span>Otwórz w Google Maps</span>
        <svg
          className="w-4 h-4"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
          />
        </svg>
      </a>
    </div>
  );
}
