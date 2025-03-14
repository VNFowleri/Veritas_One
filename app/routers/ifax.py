from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File, Form
import os
import shutil
import logging
from sqlalchemy.orm import Session
from app.database.db import SessionLocal, FaxFile
from app.utils.ocr import extract_text_from_pdf
from datetime import datetime

# Define FastAPI router
router = APIRouter(prefix="/ifax", tags=["iFax Integration"])

logger = logging.getLogger(__name__)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/receive")
async def receive_fax(
    job_id: str = Form(...),
    transaction_id: str = Form(...),
    sender: str = Form(None),
    receiver: str = Form(None),
    received_time: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Webhook endpoint for iFax to send received faxes.
    The fax file is uploaded as part of a multipart request.
    """

    received_faxes_dir = os.path.join(os.getcwd(), "received_faxes")
    os.makedirs(received_faxes_dir, exist_ok=True)

    file_path = os.path.join(received_faxes_dir, f"{job_id}.pdf")

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        logger.info(f"Saved fax PDF: {file_path}")
    except Exception as e:
        logger.error(f"Error saving fax PDF: {e}")
        raise HTTPException(status_code=500, detail="Failed to save received fax.")

    # Perform OCR
    raw_text = extract_text_from_pdf(file_path)

    # Store in database
    fax_entry = FaxFile(
        job_id=job_id,
        transaction_id=transaction_id,
        sender=sender,
        receiver=receiver,
        received_time=datetime.strptime(received_time, "%Y-%m-%d %H:%M:%S"),
        file_path=file_path,
        raw_text=raw_text,
    )

    try:
        db.add(fax_entry)
        db.commit()
        db.refresh(fax_entry)
    except Exception as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error while saving fax.")

    return {"message": "Fax received and stored", "job_id": job_id, "file_path": file_path}