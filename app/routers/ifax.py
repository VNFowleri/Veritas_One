import requests
import os
import logging
from fastapi import APIRouter, Query, HTTPException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# iFax API details
IFAX_API_URL = "https://api.ifaxapp.com/v1/fax/send"
IFAX_ACCESS_TOKEN = os.getenv("IFAX_ACCESS_TOKEN")  # Set this in your environment variables

router = APIRouter(prefix="/ifax", tags=["iFax"])

@router.post("/send")
async def send_fax(fax_number: str = Query(..., description="Recipient fax number"),
                   file_path: str = Query(..., description="Path to the PDF file")):
    """
    Sends a fax using the iFax API.
    """
    if not os.path.exists(file_path):
        raise HTTPException(status_code=400, detail=f"File does not exist: {file_path}")

    if not IFAX_ACCESS_TOKEN:
        raise HTTPException(status_code=500, detail="iFax API access token is missing. Set IFAX_ACCESS_TOKEN.")

    headers = {
        "Authorization": f"Bearer {IFAX_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "recipient": fax_number
    }

    files = {
        "file": open(file_path, "rb")
    }

    response = requests.post(IFAX_API_URL, headers=headers, data=data, files=files)

    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"❌ Failed to send fax. Response: {response.text}")
        raise HTTPException(status_code=response.status_code, detail=response.text)