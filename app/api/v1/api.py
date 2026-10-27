from fastapi import APIRouter

from app.api.v1.endpoints import hello
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.upload import router as upload_router
from app.api.v1.endpoints import analyze
from app.api.v1.endpoints import email
from app.api.v1.endpoints import bulk_email

api_router = APIRouter()
api_router.include_router(hello.router, prefix="/hello", tags=["hello"])
api_router.include_router(health_router)
api_router.include_router(upload_router)
api_router.include_router(analyze.router)
api_router.include_router(email.router)
api_router.include_router(bulk_email.router)
