import pdfplumber


def extract_text_from_pdf(file) -> str:
    """
    Extract raw text from an uploaded PDF resume.

    Args:
        file: Uploaded PDF file from FastAPI.

    Returns:
        Extracted text as a string.

    Raises:
        ValueError: If the PDF has no readable text.
    """

    text = ""

    try:
        with pdfplumber.open(file.file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

    except Exception as e:
        raise ValueError(f"Could not read PDF file: {str(e)}")

    cleaned_text = text.strip()

    if not cleaned_text:
        raise ValueError(
            "No readable text found in the PDF. The resume may be scanned or image-based."
        )

    return cleaned_text