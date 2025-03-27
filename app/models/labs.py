from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.db import Base
from sqlalchemy.sql import func

class LabResult(Base):
    __tablename__ = "labs"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    test_name = Column(String, nullable=False)          # e.g., "Hemoglobin"
    result_value = Column(Float, nullable=True)         # e.g., 13.5
    result_unit = Column(String, nullable=True)         # e.g., "g/dL"

    # CHANGED: Using DateTime for date_collected, which can store date + time
    date_collected = Column(DateTime(timezone=True), nullable=True)

    # If referencing a fax where this lab was found
    source_fax_id = Column(Integer, ForeignKey("fax_files.id"), nullable=True)

    # CHANGED: Track creation time with server default, consistent with patient table
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # relationships
    patient = relationship("Patient", backref="lab_results")
    fax_file = relationship("FaxFile", backref="lab_results", foreign_keys=[source_fax_id])
