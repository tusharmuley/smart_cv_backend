from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.services.email_service import EmailService

router = APIRouter(prefix="/email", tags=["Email"])


@router.post("/test-send")
async def test_send_email(
    recipient: str = Form(...),
    subject: str = Form(...),
    body: str = Form(...),
    resume: UploadFile = File(...),
):
    if resume.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF resumes are allowed.",
        )

    resume_bytes = await resume.read()

    if not resume_bytes:
        raise HTTPException(
            status_code=400,
            detail="Resume PDF cannot be empty.",
        )

    try:
        result = EmailService.send_email(
            recipient=recipient,
            subject=subject,
            body=body,
            resume_bytes=resume_bytes,
            resume_filename=resume.filename or "resume.pdf",
        )

        return {
            "message": "Test email sent successfully.",
            "data": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Email sending failed: {str(exc)}",
        ) from exc