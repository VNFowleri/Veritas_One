from fastapi import APIRouter, Request, Response
import logging
from app.services.twilio_fax import process_fax

router = APIRouter(prefix="/fax", tags=["Fax Processing"])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/twilio")
async def twilio_fax_webhook(request: Request):
    """
    Twilio calls this endpoint when a voice call is received.
    We check if it's a fax and redirect accordingly.
    """
    form_data = await request.form()
    call_sid = form_data.get("CallSid")  # Call SID for logging

    logger.info(f"📞 Incoming Twilio Call. CallSid={call_sid}, Data={form_data}")

    # **Since Twilio no longer supports the Receive verb, we must redirect**
    base_url = str(request.base_url).rstrip("/")
    process_url = f"{base_url}/fax/process"

    response_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Redirect method="POST">{process_url}</Redirect>
</Response>"""

    logger.info(f"✅ Twilio call received. Redirecting to: {process_url}")
    return Response(content=response_xml, media_type="text/xml")


@router.post("/process")
async def process_twilio_fax(request: Request):
    """
    Processes the final fax data sent by Twilio.
    """
    form_data = await request.form()

    # **1️⃣ Log the raw request data to troubleshoot**
    logger.info(f"📩 RAW Twilio fax request data: {form_data}")

    # **2️⃣ Check for missing fax data**
    fax_sid = form_data.get("FaxSid") or form_data.get("CallSid")  # Fallback to CallSid
    media_url = form_data.get("MediaUrl")  # This may still be missing

    if not fax_sid:
        logger.error("❌ ERROR: Twilio did not send a valid FaxSid or CallSid")
        return {"error": "Twilio did not send a valid FaxSid or CallSid"}

    if not media_url:
        logger.warning(f"⚠️ WARNING: No MediaUrl received for FaxSid: {fax_sid}")
        return Response(content='<Response><Reject/></Response>', media_type="text/xml")

    # **5️⃣ Log and process the fax**
    logger.info(f"📄 Processing fax: FaxSid={fax_sid}, MediaUrl={media_url}")
    return await process_fax(fax_sid, media_url)