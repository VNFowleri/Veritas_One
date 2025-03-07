from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
import os
from app.database.db import SessionLocal, FaxFile, DeidentifiedFile
from app.utils.ocr import run_ocr_on_pdf
from app.utils.deid import basic_deidentify
from app.services.twilio_fax import download_twilio_fax

router = APIRouter(prefix="/fax", tags=["Fax Processing"])

UPLOAD_FOLDER = "./uploads"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/upload")
async def upload_manual_fax(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Manually uploads a PDF, runs OCR, de-identifies, and stores results.
    """
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # Save file
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # OCR Processing
    extracted_text = run_ocr_on_pdf(file_path)

    # Save raw text
    fax_record = FaxFile(file_path=file_path, raw_text=extracted_text)
    db.add(fax_record)
    db.commit()
    db.refresh(fax_record)

    # De-identification
    deidentified_text = basic_deidentify(extracted_text)
    deid_record = DeidentifiedFile(fax_file_id=fax_record.id, deidentified_text=deidentified_text)
    db.add(deid_record)
    db.commit()

    return {"message": "Fax processed", "fax_id": fax_record.id}


@router.post("/twilio")
async def receive_fax_from_twilio(fax_url: str, twilio_fax_id: str, db: Session = Depends(get_db)):
    """
    Receives a Twilio webhook request and downloads the fax.
    """
    file_path = os.path.join(UPLOAD_FOLDER, f"{twilio_fax_id}.pdf")
    try:
        # Download the fax
        saved_path = download_twilio_fax(fax_url, file_path)

        # OCR Processing
        extracted_text = run_ocr_on_pdf(saved_path)

        # Save raw text
        fax_record = FaxFile(twilio_fax_id=twilio_fax_id, file_path=saved_path, raw_text=extracted_text)
        db.add(fax_record)
        db.commit()
        db.refresh(fax_record)

        # De-identification
        deidentified_text = basic_deidentify(extracted_text)
        deid_record = DeidentifiedFile(fax_file_id=fax_record.id, deidentified_text=deidentified_text)
        db.add(deid_record)
        db.commit()

        return {"message": "Fax received and processed", "fax_id": fax_record.id}

    except Exception as e:
        return {"error": str(e)}