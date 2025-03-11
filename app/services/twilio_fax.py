import requests
import os
import traceback
import logging
from fastapi import Request, Response
from twilio.rest import Client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Directory to store faxes
FAX_STORAGE_PATH = "./received_faxes"
os.makedirs(FAX_STORAGE_PATH, exist_ok=True)

# Twilio Credentials (set in environment variables)
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


async def process_fax(request: Request):
    """
    Handles the final fax data sent by Twilio.
    If MediaUrl is missing, fetches the recording manually.
    """
    try:
        form_data = await request.form()
        logger.info(f"📩 FULL Twilio request data: {form_data}")

        fax_sid = form_data.get("FaxSid") or form_data.get("CallSid")
        media_url = form_data.get("MediaUrl")

        if not fax_sid:
            logger.error("❌ ERROR: Missing FaxSid or CallSid in Twilio request")
            return {"error": "Missing FaxSid/CallSid in request"}

        # **If MediaUrl is missing, retrieve it manually**
        if not media_url:
            logger.warning(f"⚠️ WARNING: No MediaUrl received for FaxSid: {fax_sid}. Fetching manually...")
            media_url = get_fax_recording_url(fax_sid)

        if not media_url:
            logger.error(f"❌ ERROR: Still no MediaUrl found for FaxSid: {fax_sid}")
            return {"error": "Could not retrieve MediaUrl"}

        # Define file save path
        file_path = os.path.join(FAX_STORAGE_PATH, f"{fax_sid}.pdf")

        # Attempt to download the fax
        saved_path = download_twilio_fax(media_url, file_path)
        logger.info(f"✅ Successfully saved fax: {saved_path}")

        return {"message": "Fax received and saved", "fax_id": fax_sid, "file_path": saved_path}

    except Exception as e:
        error_details = traceback.format_exc()
        logger.error(f"❌ INTERNAL SERVER ERROR: {str(e)}\n{error_details}")
        return {"error": "Internal Server Error", "details": error_details}


def get_fax_recording_url(call_sid: str) -> str:
    """
    Retrieves the recording URL for a given CallSid from Twilio.
    """
    try:
        # Fetch the recording list for this call
        recordings = twilio_client.recordings.list(call_sid=call_sid)

        if not recordings:
            logger.error(f"❌ No recordings found for CallSid: {call_sid}")
            return None

        # Assume the latest recording is the fax
        recording_url = f"https://api.twilio.com{recordings[0].uri.replace('.json', '.wav')}"
        logger.info(f"🎤 Retrieved recording URL: {recording_url}")
        return recording_url

    except Exception as e:
        logger.error(f"❌ ERROR: Failed to retrieve recording for CallSid {call_sid}: {e}")
        return None


def download_twilio_fax(fax_url: str, save_path: str) -> str:
    """
    Downloads a Twilio fax PDF and saves it to the given path.
    """
    logger.info(f"⬇️ Attempting to download fax from: {fax_url}")

    try:
        response = requests.get(fax_url, timeout=15)  # Set timeout to prevent hangs

        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
            logger.info(f"✅ Successfully saved fax to {save_path}")
            return save_path
        else:
            logger.error(f"❌ Failed to download fax. Status: {response.status_code}, Response: {response.text}")
            raise Exception(f"Failed to download fax. HTTP {response.status_code}")

    except Exception as e:
        error_message = f"❌ Exception in download_twilio_fax: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_message)
        raise