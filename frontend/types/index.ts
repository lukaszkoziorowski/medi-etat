/**
 * TypeScript types matching backend models
 */

export enum MedicalRole {
  LEKARZ = "Lekarz",
  PIELĘGNIARKA = "Pielęgniarka / Pielęgniarz",
  POŁOŻNA = "Położna",
  RATOWNIK = "Ratownik medyczny",
  INNY = "Inny personel medyczny",
}

export interface JobOffer {
  id: number;
  title: string;
  facility_name: string;
  city: string;
  role: MedicalRole;
  description: string | null;
  summary: string | null;
  source_url: string;
  created_at: string;
  scraped_at?: string;
}

export interface JobsResponse {
  total: number;
  limit: number;
  offset: number;
  results: JobOffer[];
}

