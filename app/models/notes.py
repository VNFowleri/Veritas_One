# app/models/notes.py

from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.db import Base
from sqlalchemy.sql import func

class ClinicalNote(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    # Link this note to a patient
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)

    # The main note text extracted from OCR or entered by a user
    note_text = Column(Text, nullable=False)

    # Optionally store the date/time associated with the note (e.g., encounter date).
    note_date = Column(DateTime(timezone=True), nullable=True)

    # If this note came from a fax, reference that fax
    source_fax_id = Column(Integer, ForeignKey("fax_files.id"), nullable=True)

    # Standard creation timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    patient = relationship("Patient", backref="notes")
    fax_file = relationship("FaxFile", backref="notes", foreign_keys=[source_fax_id])