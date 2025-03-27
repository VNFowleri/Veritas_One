# app/models/imaging.py

from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.db import Base
from sqlalchemy.sql import func

class ImagingReport(Base):
    __tablename__ = "imaging"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)

    # A description of the imaging findings, e.g. "Chest X-ray shows no infiltrates"
    description = Column(Text, nullable=True)

    # The date/time the imaging study was performed
    date_of_study = Column(DateTime(timezone=True), nullable=True)

    # Optional reference to the fax from which the imaging was extracted
    source_fax_id = Column(Integer, ForeignKey("fax_files.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    patient = relationship("Patient", backref="imaging_reports")
    fax_file = relationship("FaxFile", backref="imaging_reports", foreign_keys=[source_fax_id])