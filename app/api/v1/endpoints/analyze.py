from fastapi import APIRouter

from app.ai.gemini_service import GeminiService
from app.schemas.analyze import AnalyzeRequest, AnalyzeResponse
from app.utils.response import success_response

router = APIRouter(
    prefix="/analyze",
    tags=["Resume Analysis"]
)


@router.post("/")
async def analyze_resume(request: AnalyzeRequest):

    result = GeminiService.analyze_resume(
        resume_text=request.resume_text,
        job_description=request.job_description,
    )

    return success_response(
        message="Resume analyzed successfully.",
        data=AnalyzeResponse(**result),
    )