'use client';

import { useState } from 'react';
import Button from '../ui/Button';

interface RefreshResult {
  status: 'success' | 'partial' | 'failed';
  sources_processed: number;
  sources_failed: number;
  new_offers: number;
  updated_offers: number;
  inactivated_offers: number;
  errors: Array<{ source: string; message: string }>;
}

export default function RefreshButton() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<RefreshResult | null>(null);

  const handleRefresh = async () => {
    setLoading(true);
    setResult(null);

    try {
      const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${API_BASE_URL}/api/admin/refresh`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: RefreshResult = await response.json();
      setResult(data);

      // Trigger jobs refresh event instead of full page reload
      if (data.status === 'success' || data.status === 'partial') {
        // Dispatch custom event to trigger jobs refetch
        window.dispatchEvent(new CustomEvent('jobs-refresh'));
      }
    } catch (error) {
      setResult({
        status: 'failed',
        sources_processed: 0,
        sources_failed: 0,
        new_offers: 0,
        updated_offers: 0,
        inactivated_offers: 0,
        errors: [{ source: 'system', message: error instanceof Error ? error.message : 'Unknown error' }],
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative">
      <Button
        onClick={handleRefresh}
        disabled={loading}
        variant="primary"
        size="sm"
      >
        {loading ? 'Odświeżanie...' : 'Odśwież oferty'}
      </Button>

      {result && (
        <div className="absolute top-full left-0 mt-2 p-4 bg-[var(--color-bg-primary)] border border-[var(--color-border)] rounded-[var(--radius-lg)] shadow-lg z-50 min-w-[300px]">
          <div className="mb-2">
            <strong className="text-sm font-semibold text-[var(--color-text-primary)]">
              Status: {result.status === 'success' ? '✅ Sukces' : result.status === 'partial' ? '⚠️ Częściowy sukces' : '❌ Błąd'}
            </strong>
          </div>
          
          <div className="text-xs text-[var(--color-text-secondary)] space-y-1">
            <div>Źródeł przetworzonych: {result.sources_processed}</div>
            <div>Źródeł z błędami: {result.sources_failed}</div>
            <div>Nowych ofert: {result.new_offers}</div>
            <div>Zaktualizowanych: {result.updated_offers}</div>
            <div>Dezaktywowanych: {result.inactivated_offers}</div>
          </div>

          {result.errors.length > 0 && (
            <div className="mt-2 pt-2 border-t border-[var(--color-border)]">
              <div className="text-xs font-semibold text-[var(--color-text-primary)] mb-1">Błędy:</div>
              {result.errors.map((error, idx) => (
                <div key={idx} className="text-xs text-red-600">
                  {error.source}: {error.message}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

