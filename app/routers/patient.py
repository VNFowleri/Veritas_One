from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime
from datetime import date
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.db import get_db
from app.models.patient import Patient  # <-- import the model from above

router = APIRouter()  # <-- We must define an APIRouter object

# Input model for creating a patient
class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    # replace line below with "email: Optional[EmailStr] = None" to require real emails
    email: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[str] = None  # expecting "YYYY-MM-DD"

# Output model for returning patient data
class PatientOut(BaseModel):
    id: int
    uuid: uuid.UUID
    first_name: str
    last_name: str
    email: Optional[str]
    phone: Optional[str]
    date_of_birth: Optional[date] = None

    class Config:
        orm_mode = True

@router.post("/", response_model=PatientOut)
async def create_patient(
    patient_in: PatientCreate,
    db: AsyncSession = Depends(get_db)
):
    # Convert date_of_birth to a date object if provided
    dob = None
    if patient_in.date_of_birth:
        try:
            dob = datetime.datetime.strptime(patient_in.date_of_birth, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="date_of_birth must be YYYY-MM-DD")

    # Create and save to DB
    new_patient = Patient(
        first_name=patient_in.first_name,
        last_name=patient_in.last_name,
        email=patient_in.email,
        phone=patient_in.phone,
        date_of_birth=dob,
    )

    db.add(new_patient)
    await db.commit()
    await db.refresh(new_patient)

    return new_patient

@router.get("/{patient_identifier}", response_model=PatientOut)
async def get_patient(
    patient_identifier: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve patient by either ID (int) or UUID (string).
    """
    # Attempt integer
    if patient_identifier.isdigit():
        query = select(Patient).where(Patient.id == int(patient_identifier))
    else:
        # Attempt UUID
        try:
            patient_uuid = uuid.UUID(patient_identifier)
            query = select(Patient).where(Patient.uuid == patient_uuid)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid identifier")

    result = await db.execute(query)
    patient = result.scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    return patient