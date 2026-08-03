from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.api import api_router
from app.core.exceptions import register_exception_handlers
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)
register_exception_handlers(app)
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {
        "message": "Welcome to SmartCV API 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }