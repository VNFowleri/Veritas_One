import requests
import os
import logging

logger = logging.getLogger(__name__)

IFAX_API_KEY = os.getenv("IFAX_API_KEY")


def fetch_received_faxes(number_id: str, order_id: str, start_date: str, end_date: str):
    """
    Fetches a list of received faxes from iFax API.
    """
    url = "https://api.ifaxapp.com/v1/customer/inbound/fax-list"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "accessToken": IFAX_API_KEY
    }
    payload = {
        "numberId": number_id,
        "orderId": order_id,
        "startDate": start_date,
        "endDate": end_date
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Failed to fetch faxes: {response.text}")
        return {"error": "Failed to fetch faxes", "status": response.status_code, "response": response.text}


def download_fax(job_id: str, transaction_id: str):
    """
    Downloads a received fax from iFax API.
    """
    url = "https://api.ifaxapp.com/v1/customer/inbound/fax-download"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "accessToken": IFAX_API_KEY
    }
    payload = {
        "jobId": job_id,
        "transactionId": transaction_id
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        pdf_data = data.get("data")

        if pdf_data:
            received_faxes_dir = os.path.join(os.getcwd(), "received_faxes")
            os.makedirs(received_faxes_dir, exist_ok=True)

            file_path = os.path.join(received_faxes_dir, f"{job_id}.pdf")
            with open(file_path, "wb") as f:
                f.write(bytes.fromhex(pdf_data))

            logger.info(f"Fax {job_id} downloaded and saved at {file_path}")
            return {"message": "Fax downloaded", "file_path": file_path}

    logger.error(f"Failed to download fax: {response.text}")
    return {"error": "Failed to download fax", "status": response.status_code}