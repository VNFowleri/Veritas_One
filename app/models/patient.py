import uuid
from sqlalchemy import Column, String, Integer, Date, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from app.database.db import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    # A system-wide unique identifier, often used for de-identification references.
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    # CHANGED: Removed unique=True for email and phone for easier testing
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)

    date_of_birth = Column(Date, nullable=True)

    # Keep creation timestamp with DB server default
    created_at = Column(DateTime(timezone=True), server_default=func.now())