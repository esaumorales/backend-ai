from fastapi import APIRouter

router = APIRouter()

@router.get("/dashboard")
def tutor_dashboard():
    return {"message": "Dashboard del tutor listo"}
