# app/models/fax_file.py

from sqlalchemy import Column, Integer, String, DateTime, Text, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.db import Base

class FaxFile(Base):
    __tablename__ = "fax_files"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=True)  # FK
    job_id = Column(String, nullable=False)
    transaction_id = Column(String, nullable=False)
    sender = Column(String, nullable=False)
    receiver = Column(String, nullable=False)
    received_time = Column(DateTime, default=datetime.utcnow)
    file_path = Column(String, nullable=False)
    pdf_data = Column(LargeBinary, nullable=True)
    ocr_text = Column(Text, nullable=True)

    patient = relationship("Patient", backref="faxes")
