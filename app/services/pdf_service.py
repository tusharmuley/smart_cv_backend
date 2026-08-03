import fitz


class PDFService:
    """Service for extracting text from PDF files."""

    @staticmethod
    def extract_text(file_bytes: bytes) -> str:
        document = fitz.open(stream=file_bytes, filetype="pdf")

        text = ""

        for page in document:
            text += page.get_text()

        document.close()

        return text.strip()