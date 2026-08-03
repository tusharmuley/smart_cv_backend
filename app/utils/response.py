from typing import Any

from app.schemas.base import APIResponse


def success_response(message: str, data: Any = None) -> APIResponse:
    """
    Returns a standard success response.
    """
    return APIResponse(
        success=True,
        message=message,
        data=data
    )


def error_response(message: str, data: Any = None) -> APIResponse:
    """
    Returns a standard error response.
    """
    return APIResponse(
        success=False,
        message=message,
        data=data
    )