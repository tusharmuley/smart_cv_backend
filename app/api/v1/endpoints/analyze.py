from fastapi import APIRouter, HTTPException

from app.ai.gemini_service import GeminiService
from app.core.config import settings
from app.core.logging import logger
from app.schemas.analyze import AnalyzeRequest, AnalyzeResponse
from app.utils.response import success_response

router = APIRouter(
    prefix="/analyze",
    tags=["Resume Analysis"]
)


@router.post("/")
async def analyze_resume(request: AnalyzeRequest):

    try:
        result = GeminiService.analyze_resume(
            resume_text=request.resume_text,
            job_description=request.job_description,
        )
    except Exception as exc:
        logger.exception("Gemini resume analysis failed")
        error_text = str(exc)
        if "UNAUTHENTICATED" in error_text or "ACCESS_TOKEN_TYPE_UNSUPPORTED" in error_text:
            detail = "The configured Google API key is invalid. Add a valid Gemini API key to smart_cv_backend/.env and restart the backend."
        elif settings.DEBUG:
            detail = f"AI provider error: {error_text}"
        else:
            detail = "The AI analysis service is temporarily unavailable."
        raise HTTPException(status_code=502, detail=detail) from exc

    return success_response(
        message="Resume analyzed successfully.",
        data=AnalyzeResponse(**result),
    )
