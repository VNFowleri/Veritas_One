from fastapi import APIRouter, Request, Response
import logging
from app.services.twilio_fax import process_fax

router = APIRouter(prefix="/fax", tags=["Fax Processing"])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/twilio")
async def twilio_fax_webhook(request: Request):
    """
    Twilio calls this endpoint when a fax is received.
    We respond with TwiML instructing Twilio to accept the fax.
    """
    base_url = str(request.base_url).rstrip("/")  # Ensure no trailing slash
    process_url = f"{base_url}/fax/process"

    response_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Receive action="{process_url}" method="POST" />
</Response>"""

    logger.info(f"✅ Twilio webhook received. Responding with TwiML to forward to: {process_url}")
    return Response(content=response_xml.strip(), media_type="application/xml")

@router.post("/process")
async def process_twilio_fax(request: Request):
    """
    Processes the final fax data sent by Twilio after the fax transmission is complete.
    """
    form_data = await request.form()
    logger.info(f"📩 Received fax processing request: {form_data}")

    fax_sid = form_data.get("FaxSid")
    media_url = form_data.get("MediaUrl")

    if not media_url:
        logger.error(f"❌ No MediaUrl received for FaxSid: {fax_sid}")
        return Response(content='<Response><Reject/></Response>', media_type="application/xml")

    logger.info(f"📄 Processing fax: FaxSid={fax_sid}, MediaUrl={media_url}")
    return await process_fax(request)