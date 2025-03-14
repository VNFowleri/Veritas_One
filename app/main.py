from fastapi import FastAPI
from dotenv import load_dotenv
import os
import logging
from app.routers import fax, ifax  # Now we have both fax and ifax routers

# Load environment variables from .env
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Verify if iFax API token is loaded correctly
ifax_token = os.getenv("IFAX_ACCESS_TOKEN")
if not ifax_token:
    logger.error("❌ ERROR: iFax API access token is missing. Set IFAX_ACCESS_TOKEN in .env.")
    raise ValueError("iFax API access token is missing. Set IFAX_ACCESS_TOKEN.")

logger.info(f"✅ Loaded iFax API Access Token: {ifax_token[:6]}****")  # Only show first 6 characters for security

# Initialize FastAPI app
app = FastAPI()

# Include the routers
app.include_router(fax.router)
app.include_router(ifax.router)  # This line registers the iFax endpoints

@app.get("/")
def root():
    return {"message": "Veritas One API is running!"}