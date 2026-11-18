
import re


def clean_text(text):
    """Normalize extracted OCR text."""
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_information(text):
    """Extract important fields from document text."""

    text = clean_text(text)

    information = {
        "name": None,
        "date_of_birth": None,
        "document_id": None,
        "phone": None,
        "email": None,
        "gender": None,
        "address": None
    }

    # Extract name
    name_match = re.search(
        r"(?:Name|Full Name)\s*[:\-]\s*([A-Za-z ]+?)(?=\s+(?:DOB|Date of Birth|Gender|Address|ID|Phone)|$)",
        text,
        re.IGNORECASE
    )

    if name_match:
        information["name"] = name_match.group(1).strip()

    # Extract date of birth
    dob_match = re.search(
        r"(?:DOB|Date of Birth|Birth Date)\s*[:\-]?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{4})",
        text,
        re.IGNORECASE
    )

    if dob_match:
        information["date_of_birth"] = dob_match.group(1)

    # Extract document ID
    id_match = re.search(
        r"(?:Document ID|ID Number|ID No|ID)\s*[:\-]?\s*([A-Z0-9-]{4,25})",
        text,
        re.IGNORECASE
    )

    if id_match:
        information["document_id"] = id_match.group(1)

    # Extract phone number
    phone_match = re.search(
        r"(?:Phone|Mobile|Contact)\s*[:\-]?\s*(\+?\d[\d\s-]{8,15})",
        text,
        re.IGNORECASE
    )

    if phone_match:
        information["phone"] = phone_match.group(1).strip()

    # Extract email
    email_match = re.search(
        r"[\w.+-]+@[\w-]+\.[\w.-]+",
        text
    )

    if email_match:
        information["email"] = email_match.group(0)

    # Extract gender
    gender_match = re.search(
        r"(?:Gender|Sex)\s*[:\-]?\s*(Male|Female|Other)",
        text,
        re.IGNORECASE
    )

    if gender_match:
        information["gender"] = gender_match.group(1).capitalize()

    # Extract address
    address_match = re.search(
        r"Address\s*[:\-]\s*(.*?)(?=\s+(?:Phone|Mobile|Email|Gender|DOB|ID)\s*[:\-]|$)",
        text,
        re.IGNORECASE
    )

    if address_match:
        information["address"] = address_match.group(1).strip()

    return information
