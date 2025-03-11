from fastapi import APIRouter, Query, HTTPException
import requests
import os

router = APIRouter(prefix="/ifax", tags=["iFax Integration"])

# iFax API Key (make sure to set this in your environment)
IFAX_API_KEY = os.getenv("IFAX_API_KEY")

@router.post("/send")
def send_fax(fax_number: str = Query(..., description="Recipient Fax Number"), file_path: str = Query(..., description="Path to PDF")):
    """
    Sends a fax using the iFax API.
    """
    if not IFAX_API_KEY:
        raise HTTPException(status_code=500, detail="iFax API key is missing. Set IFAX_API_KEY in your environment.")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=400, detail=f"File does not exist: {file_path}")

    url = "https://api.ifaxapp.com/send-fax"
    headers = {
        "Authorization": f"Bearer {IFAX_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "fax_number": fax_number,
        "file_url": f"http://your-server-url/{file_path}"  # Replace with actual accessible URL
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return {"message": "Fax sent successfully", "fax_number": fax_number, "file": file_path}
    else:
        return {"error": "Failed to send fax", "status": response.status_code, "response": response.text}