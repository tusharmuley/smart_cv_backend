
import base64
from email.message import EmailMessage
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


BASE_DIR = Path(__file__).resolve().parents[2]

CREDENTIALS_FILE = BASE_DIR / "credentials.json"
TOKEN_FILE = BASE_DIR / "token.json"

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


class EmailService:
    """Send emails through the user's Gmail account."""

    @staticmethod
    def get_gmail_service():
        credentials = None

        if TOKEN_FILE.exists():
            credentials = Credentials.from_authorized_user_file(
                str(TOKEN_FILE),
                SCOPES,
            )

        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())

        if not credentials or not credentials.valid:
            if not CREDENTIALS_FILE.exists():
                raise FileNotFoundError(
                    f"OAuth credentials not found: {CREDENTIALS_FILE}"
                )

            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE),
                SCOPES,
            )

            credentials = flow.run_local_server(port=0)

        TOKEN_FILE.write_text(
            credentials.to_json(),
            encoding="utf-8",
        )

        return build("gmail", "v1", credentials=credentials)

    @staticmethod
    def send_email(
        recipient: str,
        subject: str,
        body: str,
        resume_bytes: bytes,
        resume_filename: str = "resume.pdf",
    ):
        service = EmailService.get_gmail_service()

        message = EmailMessage()
        message["To"] = recipient
        message["Subject"] = subject.strip()

        # Preserve the body exactly as received.
        # Newlines and blank lines are retained in plain-text email.
        message.set_content(body)

        # Attach resume PDF.
        message.add_attachment(
            resume_bytes,
            maintype="application",
            subtype="pdf",
            filename=resume_filename,
        )

        encoded_message = base64.urlsafe_b64encode(
            message.as_bytes()
        ).decode("utf-8")

        result = (
            service.users()
            .messages()
            .send(
                userId="me",
                body={"raw": encoded_message},
            )
            .execute()
        )

        return {
            "message_id": result.get("id"),
            "recipient": recipient,
            "status": "sent",
        }
