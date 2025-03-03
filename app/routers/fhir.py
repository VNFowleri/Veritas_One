import os
import jwt  # PyJWT for signing JWTs
import requests
import datetime
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/fhir", tags=["Epic FHIR API"])

TOKEN_URL = "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token"
FHIR_BASE_URL = "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4"
CLIENT_ID = os.getenv("FHIR_CLIENT_ID")
PRIVATE_KEY_PATH = "private_key.pem"  # Make sure this exists!

def generate_jwt():
    """
    Creates a signed JWT for Epic OAuth authentication.
    """
    now = datetime.datetime.utcnow()
    payload = {
        "iss": CLIENT_ID,  # The app's client ID
        "sub": CLIENT_ID,  # The same client ID for Epic
        "aud": TOKEN_URL,  # Epic token endpoint
        "jti": "unique-jwt-id",  # Generate a unique JWT ID per request
        "exp": now + datetime.timedelta(minutes=5),  # Expiry in 5 minutes
        "iat": now,
        "nbf": now
    }

    # Load Private Key
    with open(PRIVATE_KEY_PATH, "r") as key_file:
        private_key = key_file.read()

    # Sign JWT using RS256
    signed_jwt = jwt.encode(payload, private_key, algorithm="RS256")

    return signed_jwt

def get_access_token():
    """
    Requests an OAuth access token from Epic using JWT authentication.
    """
    jwt_token = generate_jwt()

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "client_credentials",
        "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
        "client_assertion": jwt_token,
    }

    response = requests.post(TOKEN_URL, headers=headers, data=payload)

    print("🔹 Epic OAuth Response:", response.status_code, response.text)

    if response.status_code == 200:
        return response.json().get("access_token")

    raise HTTPException(status_code=response.status_code, detail=f"Failed to obtain access token: {response.text}")

# Fetch Patient Data from Epic
@router.get("/patient/{patient_id}")
def fetch_patient_data(patient_id: str):
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(f"{FHIR_BASE_URL}/Patient/{patient_id}", headers=headers)

    print("🔹 FHIR API Response Status:", response.status_code)
    print("🔹 FHIR API Response Body:", response.text)

    if response.status_code == 200:
        return response.json()

    raise HTTPException(status_code=response.status_code, detail=f"Failed to fetch patient data: {response.text}")