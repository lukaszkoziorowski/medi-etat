"""
Database models for Medietat job offers.
"""
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MedicalRole(str, Enum):
    """Medical role taxonomy for job offers."""
    LEKARZ = "Lekarz"
    PIELĘGNIARKA = "Pielęgniarka / Pielęgniarz"
    POŁOŻNA = "Położna"
    RATOWNIK = "Ratownik medyczny"
    INNY = "Inny personel medyczny"


class JobOffer(Base):
    """Job offer model."""
    __tablename__ = "job_offers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, index=True)
    facility_name = Column(String(255), nullable=False, index=True)
    city = Column(String(100), nullable=False, index=True)  # For future location filtering
    role = Column(SQLEnum(MedicalRole), nullable=False, index=True)
    description = Column(Text, nullable=True)
    source_url = Column(String(1000), unique=True, nullable=False, index=True)
    scraped_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<JobOffer(id={self.id}, title='{self.title[:50]}...', facility='{self.facility_name}', city='{self.city}')>"

