from sqlalchemy import Column, Integer, String, Boolean
from app.database.db import Base

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    dob = Column(String, nullable=False)
    consent_status = Column(Boolean, default=False)