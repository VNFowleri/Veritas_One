# app/routers/ifax.py

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Request
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import os
import asyncio
import logging
from app.database import get_db
from app.models.fax_file import FaxFile
from app.utils.ocr import extract_text_from_pdf
from app.services.ifax_service import download_fax
from pydantic import BaseModel, Field
from typing import Optional
import json

router = APIRouter()
logger = logging.getLogger(__name__)


class FaxWebhookPayload(BaseModel):
    jobId: int
    transactionId: int
    fromNumber: str
    toNumber: str
    faxCallLength: int
    faxCallStart: int
    faxCallEnd: int
    faxTotalPages: int
    faxTransferredPages: int = Field(..., alias="faxReceivedPages")
    faxStatus: str
    message: str
    code: int
    direction: Optional[str] = None

    class Config:
        extra = "allow"


@router.post("/receive")
async def receive_fax(
        request: Request,
        background_tasks: BackgroundTasks,
        db: AsyncSession = Depends(get_db)
):
    # Log raw request for debugging.
    raw_body = await request.body()
    logger.info("Raw request body: %s", raw_body)
    try:
        payload_data = await request.json()
    except Exception as e:
        logger.error("Failed to parse JSON: %s", e)
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    # Validate payload using Pydantic
    try:
        payload = FaxWebhookPayload(**payload_data)
    except Exception as e:
        logger.error("Payload validation error: %s", e)
        raise HTTPException(status_code=422, detail="Payload validation error: " + str(e))

    logger.info("Parsed payload: %s", payload.json())

    try:
        # Save metadata to the database (initially no patient_id, no OCR).
        fax = FaxFile(
            job_id=str(payload.jobId),
            transaction_id=str(payload.transactionId),
            sender=payload.fromNumber,
            receiver=payload.toNumber,
            received_time=datetime.utcfromtimestamp(payload.faxCallStart),
            file_path="",
            pdf_data=b"",
            ocr_text="",
        )
        db.add(fax)
        await db.commit()
        await db.refresh(fax)

        # Trigger background task to download and process the fax (OCR, match patient, parse data, etc.)
        background_tasks.add_task(process_fax, str(payload.jobId), fax.id, payload.transactionId, payload.direction)

        return {"status": "success", "fax_id": fax.id}

    except Exception as e:
        logger.exception("Failed to process fax webhook")
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def process_fax(job_id: str, fax_record_id: int, transaction_id: int, direction: Optional[str] = None):
    """
    Background task that downloads the fax using the API,
    runs OCR, and updates the DB record (including matching a patient).
    """
    try:
        from app.database.db import SessionLocal
        from sqlalchemy.future import select
        from app.models.patient import Patient
        # OPTIONAL: if you have labs/notes/imaging models, import them
        # from app.models.labs import LabResult
        # from app.models.notes import ClinicalNote
        # from app.models.imaging import ImagingReport

        async with SessionLocal() as db:
            # 1) Download fax PDF
            download_result = await asyncio.to_thread(download_fax, job_id, transaction_id, direction)
            if "error" in download_result:
                raise Exception(download_result.get("error"))
            file_path = download_result.get("file_path")
            if not file_path or not os.path.exists(file_path):
                raise Exception("Downloaded file not found")
            logger.info(f"Downloaded fax file from iFax: {file_path}")

            # 2) Run OCR
            ocr_text = extract_text_from_pdf(file_path)
            logger.info("OCR processing complete.")

            # 3) Read PDF content (binary)
            with open(file_path, "rb") as f:
                pdf_content = f.read()

            # 4) Update the fax record with path, PDF data, and OCR text
            fax = await db.get(FaxFile, fax_record_id)
            if fax:
                fax.file_path = os.path.abspath(file_path)
                fax.pdf_data = pdf_content
                fax.ocr_text = ocr_text
                db.add(fax)
                await db.commit()
                await db.refresh(fax)

            # 5) Attempt to match patient by name + DOB from OCR
            #    (You'll need a small function to parse these from the text)
            first_name, last_name, dob = parse_name_and_dob(ocr_text)
            if first_name and last_name and dob:
                result = await db.execute(
                    select(Patient).where(
                        Patient.first_name == first_name,
                        Patient.last_name == last_name,
                        Patient.date_of_birth == dob
                    )
                )
                matched_patient = result.scalar_one_or_none()

                if matched_patient and fax:
                    fax.patient_id = matched_patient.id
                    db.add(fax)
                    await db.commit()
                    logger.info(f"Fax {fax.id} matched to patient {matched_patient.id}")

                    # 6) (Optional) parse structured data from OCR and save to labs/notes/imaging
                    # parse_and_store_structured_data(fax, matched_patient, db)

            # Done!
    except Exception as e:
        logger.exception("Failed to process fax download in background: %s", str(e))


#
# Helper function to parse name & DOB from OCR text
#
def parse_name_and_dob(ocr_text: str):
    """
    Minimal example to parse lines like:
      Name: Brandon Gaston
      DOB: 1992-06-28
    Adjust to match your OCR text patterns.
    """
    import re
    from datetime import datetime

    # Basic regex. If the OCR text has "Name: John Smith" or "Patient Name: John Smith", etc.
    name_pattern = re.search(r"Name:\s*([A-Za-z]+)\s+([A-Za-z]+)", ocr_text)
    dob_pattern = re.search(r"DOB:\s*(\d{4}-\d{2}-\d{2})", ocr_text)

    first_name, last_name, dob_date = None, None, None

    if name_pattern:
        first_name = name_pattern.group(1)
        last_name = name_pattern.group(2)

    if dob_pattern:
        dob_str = dob_pattern.group(1)
        dob_date = datetime.strptime(dob_str, "%Y-%m-%d").date()

    return first_name, last_name, dob_date

# OPTIONAL: parse labs, notes, imaging from OCR and store them.
# def parse_and_store_structured_data(fax: FaxFile, patient: Patient, db: AsyncSession):
#     # e.g. parse lab results, imaging findings, etc.
#     pass