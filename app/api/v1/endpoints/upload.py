from fastapi import APIRouter, File, HTTPException, UploadFile
from app.schemas.base import APIResponse
from app.schemas.upload import UploadResponseData
from app.services.pdf_service import PDFService
from app.utils.response import success_response
from app.core.logging import logger

router = APIRouter(prefix="/upload", tags=["Resume Upload"])


@router.post("/")
async def upload_resume(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    pdf_bytes = await file.read()

    resume_text = PDFService.extract_text(pdf_bytes)
    logger.info("Resume text extracted successfully.")
    logger.info("Upload API completed successfully.")
    return success_response(
        message="Resume uploaded successfully.",
        data=UploadResponseData(
            resume_text=resume_text
        )
    )