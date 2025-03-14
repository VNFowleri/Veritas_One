import pytesseract
from pdf2image import convert_from_path
import os
import logging

logger = logging.getLogger(__name__)

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts text from a PDF using OCR.
    """
    if not os.path.exists(pdf_path):
        logger.error(f"PDF file not found: {pdf_path}")
        return ""

    try:
        images = convert_from_path(pdf_path)
        all_text = []
        for page_num, img in enumerate(images, start=1):
            logger.info(f"Processing page {page_num} for OCR...")
            text = pytesseract.image_to_string(img)
            all_text.append(text)
        return "\n".join(all_text)
    except Exception as e:
        logger.exception(f"Failed OCR on PDF: {pdf_path}. Error: {e}")
        return ""