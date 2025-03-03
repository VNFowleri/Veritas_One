import os
import requests
from fastapi import APIRouter, HTTPException

# 🔹 Epic FHIR Sandbox Credentials
FHIR_BASE_URL = "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4"
TOKEN_URL = "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token"
CLIENT_ID = os.getenv("FHIR_CLIENT_ID", "your-client-id")  # Ensure it is set in env vars

router = APIRouter(prefix="/fhir/patient", tags=["FHIR Patient"])

# 🔹 OAuth2 Token Request
def get_access_token():
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {"grant_type": "client_credentials", "client_id": CLIENT_ID}

    response = requests.post(TOKEN_URL, headers=headers, data=payload)

    print("🔹 OAuth Response Status:", response.status_code)
    print("🔹 OAuth Response Body:", response.text)

    if response.status_code == 200:
        return response.json().get("access_token")

    raise HTTPException(status_code=response.status_code, detail=f"Failed to obtain access token: {response.text}")

# 🔹 Fetch Patient Data from Epic's FHIR Sandbox
def fetch_patient_data(patient_id: str):
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(f"{FHIR_BASE_URL}/Patient/{patient_id}", headers=headers)

    print("🔹 FHIR API Response Status:", response.status_code)
    print("🔹 FHIR API Response Body:", response.text)

    if response.status_code == 200:
        return response.json()

    raise HTTPException(status_code=response.status_code, detail=f"Failed to fetch patient data: {response.text}")

# 🔹 FastAPI Endpoints
@router.get("/{patient_id}")
def get_fhir_patient(patient_id: str):
    return fetch_patient_data(patient_id)

@router.get("/")
def get_default_patient():
    return fetch_patient_data("erXuFYUfucBZaryVksYEcMg3")  # Default test patient