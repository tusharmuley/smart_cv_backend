from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["Health"])
def health():
    return {
        "success": True,
        "message": "API is healthy",
        "data": {
            "app_name": "Smart CV Backend",
            "app_version": "1.0.0",
            "status": "healthy"
        }
    }