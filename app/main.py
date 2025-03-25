# app/main.py

from dotenv import load_dotenv
load_dotenv()  # Load .env file as early as possible

import os
import logging
from fastapi import FastAPI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Validate that required environment variables are set
IFAX_ACCESS_TOKEN = os.getenv("IFAX_ACCESS_TOKEN")
if not IFAX_ACCESS_TOKEN:
    logger.error("❌ ERROR: IFAX_ACCESS_TOKEN is missing. Set IFAX_ACCESS_TOKEN in your .env file.")
    raise Exception("Missing IFAX_ACCESS_TOKEN in environment variables.")

# Import routers only after environment variables are loaded
from app.routers import fax, ifax

# Initialize FastAPI app
app = FastAPI()

# Include routers with desired prefixes.
# Ensure that in app/routers/ifax.py, the route is defined as "@router.post('/receive')"
app.include_router(fax.router, prefix="/fax")
app.include_router(ifax.router, prefix="/ifax")

# Health-check endpoint
@app.get("/")
async def read_root():
    return {"message": "Veritas One API is running"}

# Run the server when executing this file directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)