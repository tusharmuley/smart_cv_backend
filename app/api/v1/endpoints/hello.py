from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def read_root() -> dict:
    return {"message": "Hello from Smart CV backend"}
