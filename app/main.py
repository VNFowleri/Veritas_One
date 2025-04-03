from dotenv import load_dotenv
load_dotenv()

import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <-- Add this

from app.routers import ifax, patient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

IFAX_ACCESS_TOKEN = os.getenv("IFAX_ACCESS_TOKEN")
if not IFAX_ACCESS_TOKEN:
    logger.error("❌ ERROR: IFAX_ACCESS_TOKEN is missing. Set it in your .env file.")
    raise Exception("Missing IFAX_ACCESS_TOKEN in environment variables.")

app = FastAPI()

# ✅ Add CORS middleware here
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://veritasone.net"],  # or ["*"] for local dev/testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ifax.router, prefix="/ifax")
app.include_router(patient.router, prefix="/patient", tags=["Patient"])

@app.get("/")
async def read_root():
    return {"message": "Veritas One API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)