from typing import Any

from pydantic import BaseModel


class APIResponse(BaseModel):
    """
    Common response format for all APIs.
    """

    success: bool
    message: str
    data: Any | None = None