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
    jobId: int                     # Accept as int.
    transactionId: int             # Now required
    fromNumber: str
    toNumber: str
    faxCallLength: int
    faxCallStart: int              # Unix timestamp.
    faxCallEnd: int                # Unix timestamp.
    faxTotalPages: int
    faxTransferredPages: int = Field(..., alias="faxReceivedPages")
    faxStatus: str
    message: str
    code: int
    direction: Optional[str] = None

    class Config:
        extra = "allow"  # Allow additional keys

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
    try:
        payload = FaxWebhookPayload(**payload_data)
    except Exception as e:
        logger.error("Payload validation error: %s", e)
        raise HTTPException(status_code=422, detail="Payload validation error: " + str(e))
    logger.info("Parsed payload: %s", payload.json())
    try:
        # Save metadata to the database.
        fax = FaxFile(
            job_id=str(payload.jobId),
            transaction_id=str(payload.transactionId),  # Always include transactionId
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
        # Trigger background task to download and process the fax.
        background_tasks.add_task(process_fax, str(payload.jobId), fax.id, payload.transactionId, payload.direction)
        return {"status": "success", "fax_id": fax.id}
    except Exception as e:
        logger.exception("Failed to process fax webhook")
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

async def process_fax(job_id: str, fax_record_id: int, transaction_id: int, direction: Optional[str] = None):
    """
    Background task that downloads the fax using the API,
    runs OCR, and updates the DB record.
    """
    try:
        from app.database.db import SessionLocal
        async with SessionLocal() as db:
            download_result = await asyncio.to_thread(download_fax, job_id, transaction_id, direction)
            if "error" in download_result:
                raise Exception(download_result.get("error"))
            file_path = download_result.get("file_path")
            if not file_path or not os.path.exists(file_path):
                raise Exception("Downloaded file not found")
            logger.info(f"Downloaded fax file from iFax: {file_path}")
            ocr_text = extract_text_from_pdf(file_path)
            logger.info("OCR processing complete.")
            with open(file_path, "rb") as f:
                pdf_content = f.read()
            fax = await db.get(FaxFile, fax_record_id)
            if fax:
                fax.file_path = os.path.abspath(file_path)
                fax.pdf_data = pdf_content
                fax.ocr_text = ocr_text
                await db.commit()
    except Exception as e:
        logger.exception("Failed to process fax download in background: %s", str(e))