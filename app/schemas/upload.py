from pydantic import BaseModel


class UploadResponseData(BaseModel):
    """
    Response data after resume upload.
    """

    resume_text: str