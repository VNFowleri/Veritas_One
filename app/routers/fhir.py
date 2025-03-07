import os
import time
import jwt  # PyJWT for signing JWTs
import requests
import uuid
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException

# ✅ Load environment variables from .env
load_dotenv()

router = APIRouter(prefix="/fhir", tags=["Epic FHIR API"])

# ✅ Epic FHIR API URLs & Credentials
FHIR_CLIENT_ID = os.getenv("FHIR_CLIENT_ID")
TOKEN_URL = os.getenv("FHIR_TOKEN_URL", "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token")
FHIR_API_URL = os.getenv("FHIR_API_URL", "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4")
PRIVATE_KEY_PATH = os.getenv("PRIVATE_KEY_PATH", "private_key.pem")

# ✅ Enforce RS256 for JWT signing
JWT_ALGORITHM = "RS256"  # Epic requires RS256 for static public key auth
JWT_EXPIRATION_MINUTES = min(int(os.getenv("JWT_EXPIRATION_MINUTES", 5)), 5)  # Ensure max 5 mins


def generate_jwt():
    """
    Generate a valid JWT for Epic authentication.
    """
    now = int(time.time())

    payload = {
        "iss": FHIR_CLIENT_ID,
        "sub": FHIR_CLIENT_ID,
        "aud": TOKEN_URL,
        "jti": str(uuid.uuid4()),  # Unique token ID
        "exp": now + JWT_EXPIRATION_MINUTES * 60,  # Expiration (≤5 mins)
        "iat": now,
        "nbf": now
    }

    # Load Private Key
    try:
        with open(PRIVATE_KEY_PATH, "r") as key_file:
            private_key = key_file.read()
    except Exception as e:
        raise Exception(f"Failed to load private key: {str(e)}")

    try:
        # Sign JWT using RS256
        signed_jwt = jwt.encode(payload, private_key, algorithm=JWT_ALGORITHM)
        return signed_jwt.strip()  # Ensure it's clean with no whitespace
    except Exception as e:
        raise Exception(f"JWT signing failed: {str(e)}")


def get_access_token():
    """
    Requests an OAuth access token from Epic using JWT authentication.
    """
    jwt_token = generate_jwt()

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    payload = {
        "grant_type": "client_credentials",
        "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
        "client_assertion": jwt_token,
    }

    print("🔹 Sending OAuth Request with JWT...")  # ✅ Debugging

    response = requests.post(TOKEN_URL, headers=headers, data=payload)

    print("🔹 Epic OAuth Response Status:", response.status_code)
    print("🔹 Epic OAuth Response Body:", response.text)

    if response.status_code == 200:
        return response.json().get("access_token")

    elif response.status_code == 429:
        raise HTTPException(
            status_code=429, detail="Epic API rate limit exceeded. Try again later."
        )

    raise HTTPException(status_code=response.status_code, detail=f"Failed to obtain access token: {response.text}")


@router.get("/patient/{patient_id}")
def fetch_patient_data(patient_id: str):
    """
    Fetch patient data from Epic FHIR API using an OAuth access token.
    """
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(f"{FHIR_API_URL}/Patient/{patient_id}", headers=headers)

    print("🔹 FHIR API Response Status:", response.status_code)
    print("🔹 FHIR API Response Body:", response.text)

    if response.status_code == 200:
        return response.json()

    raise HTTPException(status_code=response.status_code, detail=f"Failed to fetch patient data: {response.text}")


if __name__ == "__main__":
    print(generate_jwt())  # ✅ Only prints once when running the script