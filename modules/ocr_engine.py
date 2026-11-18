
import os
import pytesseract
import pymupdf
import cv2
import numpy as np

from PIL import Image

# Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_text_from_image(image_path):
    """Extract text from an image using OCR."""

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Unable to read image file.")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    processed = cv2.threshold(
        gray, 0, 255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    text = pytesseract.image_to_string(processed)

    return text.strip()


def extract_text_from_pdf(pdf_path):
    """Extract text from PDF, using OCR for scanned pages."""

    extracted_text = []

    with pymupdf.open(pdf_path) as document:
        for page in document:
            text = page.get_text().strip()

            if not text:
                pix = page.get_pixmap(dpi=200)
                image = Image.frombytes(
                    "RGB",
                    [pix.width, pix.height],
                    pix.samples
                )

                text = pytesseract.image_to_string(image)

            extracted_text.append(text)

    return "\n".join(extracted_text)


def extract_document_text(file_path):
    """Automatically identify document type."""

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    elif extension in [".png", ".jpg", ".jpeg", ".bmp", ".tiff"]:
        return extract_text_from_image(file_path)

    else:
        raise ValueError("Unsupported document format.")
