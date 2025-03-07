import requests
import os


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