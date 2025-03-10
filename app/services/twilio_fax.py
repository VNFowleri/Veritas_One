import requests
import os
import logging
from fastapi import Response

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Directory to store faxes
FAX_STORAGE_PATH = "./received_faxes"
os.makedirs(FAX_STORAGE_PATH, exist_ok=True)

async def process_fax(fax_sid: str, media_url: str):
    """
    Handles the final fax data sent by Twilio after the fax transmission is complete.
    Downloads and saves the fax as a PDF.
    """
    logger.info(f"📄 Processing received fax: FaxSid={fax_sid}, MediaUrl={media_url}")

    file_path = os.path.join(FAX_STORAGE_PATH, f"{fax_sid}.pdf")

    try:
        saved_path = download_twilio_fax(media_url, file_path)
        logger.info(f"✅ Successfully saved fax: {saved_path}")
        return {"message": "Fax received and saved", "fax_id": fax_sid, "file_path": saved_path}
    except Exception as e:
        logger.error(f"❌ Failed to download fax: {e}")
        return {"error": "Failed to download fax"}

def download_twilio_fax(fax_url: str, save_path: str) -> str:
    """
    Downloads a Twilio fax PDF and saves it to the given path.
    """
    response = requests.get(fax_url)

    if response.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(response.content)
        return save_path
    else:
        raise Exception(f"Failed to download fax. Status code: {response.status_code}")