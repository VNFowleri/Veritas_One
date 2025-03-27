# app/main.py

from dotenv import load_dotenv
load_dotenv()  # Load .env file as early as possible

import os
import logging
from fastapi import FastAPI

# 1) Import your routers
#    Make sure "patient.py" is inside "app/routers", containing "router = APIRouter()"
from app.routers import ifax, patient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Validate required environment variables
IFAX_ACCESS_TOKEN = os.getenv("IFAX_ACCESS_TOKEN")
if not IFAX_ACCESS_TOKEN:
    logger.error("❌ ERROR: IFAX_ACCESS_TOKEN is missing. Set it in your .env file.")
    raise Exception("Missing IFAX_ACCESS_TOKEN in environment variables.")

# 2) Initialize FastAPI
app = FastAPI()

# 3) Include existing routers (e.g., iFax)
app.include_router(ifax.router, prefix="/ifax")

# 4) Include the patient router
#    The 'router' object must be defined in "app/routers/patient.py"
app.include_router(
    patient.router,   # <--- from "app/routers/patient"
    prefix="/patient",
    tags=["Patient"]
)

# Simple health-check endpoint
@app.get("/")
async def read_root():
    return {"message": "Veritas One API is running"}

# Run the server when executing this file directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)