import requests
import os
import logging
import base64

logger = logging.getLogger(__name__)

# Use the API token from your environment.
IFAX_ACCESS_TOKEN = os.getenv("IFAX_ACCESS_TOKEN")

def download_fax(job_id: str, transaction_id: int, direction: str = None):
    url = "https://api.ifaxapp.com/v1/customer/inbound/fax-download"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "accessToken": IFAX_ACCESS_TOKEN
    }
    # Build payload without 'direction' since the API sample doesn't include it.
    payload = {
        "jobId": str(job_id),
        "transactionId": str(transaction_id)
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        try:
            data = response.json()
        except Exception as e:
            logger.exception("Error parsing response JSON")
            return {"error": "Invalid response JSON", "status": response.status_code}
        logger.info("Download fax response JSON: %s", data)
        if data.get("status") == 1:
            file_data = data.get("data")
            if file_data:
                try:
                    fax_pdf = base64.b64decode(file_data)
                except Exception as e:
                    logger.exception("Error decoding PDF data from base64")
                    return {"error": "Failed to decode fax file", "status": response.status_code}
                received_faxes_dir = os.path.join(os.getcwd(), "received_faxes")
                os.makedirs(received_faxes_dir, exist_ok=True)
                file_path = os.path.join(received_faxes_dir, f"{job_id}.pdf")
                with open(file_path, "wb") as f:
                    f.write(fax_pdf)
                logger.info(f"Fax {job_id} downloaded and saved at {file_path}")
                return {"message": "Fax downloaded", "file_path": file_path}
            else:
                logger.error("No file data found in response")
                return {"error": "No file data found", "status": response.status_code}
        else:
            logger.error("Fax download failed: %s", data)
            return {"error": "Fax download failed", "status": response.status_code, "response": data}
    else:
        logger.error(f"Failed to download fax: {response.text}")
        return {"error": "Failed to download fax", "status": response.status_code}