import pytesseract
from pdf2image import convert_from_path
import os

def run_ocr_on_pdf(pdf_path: str) -> str:
    """
    Extract text from a faxed PDF using Tesseract OCR.
    """
    images = convert_from_path(pdf_path)  # Convert PDF pages to images
    extracted_text = ""

    for img in images:
        extracted_text += pytesseract.image_to_string(img) + "\n"

    return extracted_text.strip()