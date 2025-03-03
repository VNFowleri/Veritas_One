from fastapi import APIRouter

router = APIRouter(prefix="/patient", tags=["patient"])

@router.get("/{patient_id}")
def get_patient(patient_id: str):
    return {"patient_id": patient_id, "message": "Patient data retrieved!"}