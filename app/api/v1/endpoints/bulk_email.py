import io
import re
from typing import List

import pandas as pd
from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.services.email_service import EmailService

router = APIRouter(prefix="/bulk-email", tags=["Bulk Email"])

MAX_RECIPIENTS = 50
MAX_FILE_BYTES = 2 * 1024 * 1024  # 2 MB
MAX_RESUME_BYTES = 5 * 1024 * 1024  # 5 MB; adjust if needed

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def parse_recipients(file_bytes: bytes, filename: str) -> List[str]:
    """Read email addresses from a CSV or Excel file with an email column."""
    suffix = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""
    try:
        if suffix == "csv":
            df = pd.read_csv(io.BytesIO(file_bytes), dtype=str)
        elif suffix in {"xlsx", "xls"}:
            # .xlsx supported by openpyxl; legacy .xls may need xlrd.
            df = pd.read_excel(io.BytesIO(file_bytes), dtype=str)
        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type. Upload .csv or .xlsx.",
            )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Could not read recipient file: {exc}",
        ) from exc

    if df.empty or len(df.columns) == 0:
        raise HTTPException(status_code=400, detail="Recipient file is empty.")

    # Accept common column names; if there is only one column, use it.
    normalized = {
        str(col).strip().lower().replace("_", " ").replace("-", " "): col
        for col in df.columns
    }
    candidate_names = {
        "email", "email address", "email id", "e mail", "e mail address"
    }
    selected = next(
        (normalized[name] for name in candidate_names if name in normalized),
        df.columns[0] if len(df.columns) == 1 else None,
    )
    if selected is None:
        raise HTTPException(
            status_code=400,
            detail="Could not identify email column. Use a column named 'email'.",
        )

    found = []
    invalid = []
    seen = set()
    for value in df[selected].dropna().astype(str):
        email = value.strip().strip("<>").strip()
        if not email:
            continue
        if not EMAIL_RE.match(email):
            invalid.append(email)
            continue
        key = email.casefold()
        if key not in seen:
            seen.add(key)
            found.append(email)

    if invalid:
        # Report invalid rows rather than silently attempting to send to them.
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Invalid email address(es) found. Fix the file and retry.",
                "invalid_emails": invalid[:20],
                "invalid_count": len(invalid),
            },
        )
    if not found:
        raise HTTPException(status_code=400, detail="No valid email addresses found.")
    if len(found) > MAX_RECIPIENTS:
        raise HTTPException(
            status_code=400,
            detail=f"Found {len(found)} unique recipients; maximum is {MAX_RECIPIENTS}.",
        )
    return found


@router.post("/send")
async def send_bulk_email(
    recipients_file: UploadFile = File(...),
    subject: str = Form(..., min_length=1, max_length=200),
    body: str = Form(..., min_length=1, max_length=10000),
    resume: UploadFile = File(...),
):
    """Send a separate email with the same subject/body and PDF to each recipient."""
    filename = (recipients_file.filename or "").lower()
    if not (filename.endswith(".csv") or filename.endswith(".xlsx")):
        raise HTTPException(
            status_code=400,
            detail="Upload a .csv or .xlsx recipient file.",
        )

    recipient_bytes = await recipients_file.read()
    if len(recipient_bytes) > MAX_FILE_BYTES:
        raise HTTPException(status_code=413, detail="Recipient file must be 2 MB or smaller.")

    resume_filename = resume.filename or "resume.pdf"
    if not resume_filename.lower().endswith(".pdf") or resume.content_type not in {
        "application/pdf", "application/octet-stream"
    }:
        raise HTTPException(status_code=400, detail="Resume must be a PDF file.")

    resume_bytes = await resume.read()
    if not resume_bytes:
        raise HTTPException(status_code=400, detail="Resume PDF cannot be empty.")
    if len(resume_bytes) > MAX_RESUME_BYTES:
        raise HTTPException(status_code=413, detail="Resume PDF must be 5 MB or smaller.")

    recipients = parse_recipients(recipient_bytes, filename)

    # Confirm the recipient list, subject and body in the UI before calling this endpoint.
    results = []
    for recipient in recipients:
        try:
            result = EmailService.send_email(
                recipient=recipient,
                subject=subject.strip(),
                body=body,
                resume_bytes=resume_bytes,
                resume_filename=resume_filename,
            )
            results.append({
                "recipient": recipient,
                "status": "sent",
                "message_id": result.get("message_id"),
            })
        except Exception as exc:
            # Continue with remaining recipients if one message fails.
            results.append({
                "recipient": recipient,
                "status": "failed",
                "error": str(exc)[:300],
            })

    sent_count = sum(item["status"] == "sent" for item in results)
    failed_count = len(results) - sent_count
    return {
        "message": "Bulk email attempt completed.",
        "total": len(results),
        "sent": sent_count,
        "failed": failed_count,
        "results": results,
    }
