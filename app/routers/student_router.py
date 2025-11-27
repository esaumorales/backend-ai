from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import SessionLocal
from app.models.student_model import Student
from app.models.prediction_model import Prediction
from app.models.user_model import User
from app.routers.auth_router import get_current_user

router = APIRouter(tags=["Students"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def log(msg: str):
    print(f"📘 [STUDENTS] {msg}")


# ============================================================
# 🔹 OBTENER INFORMACIÓN DEL ESTUDIANTE LOGUEADO
# ============================================================
@router.get("/me")
def get_my_student(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    log(f"Consultando info del estudiante user_id={current_user.id}")

    student = db.query(Student).filter(Student.user_id == current_user.id).first()

    if not student:
        raise HTTPException(404, "Estudiante no encontrado")

    last = student.predictions[-1] if student.predictions else None

    return {
        "id": student.id,
        "nombre": student.nombre,
        "tutor_id": student.tutor_id,
        "academic_performance": last.predicted_label if last else "Sin datos",
        "score": round(last.predicted_score * 100, 2) if last else None,
    }


# ============================================================
# 🔹 LISTA DE TUTORES DISPONIBLES  (ANTES DEL ENDPOINT DINÁMICO)
# ============================================================
@router.get("/available-tutors")
def list_available_tutors(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    log(f"Usuario {current_user.id} pide lista de tutores")

    tutors = db.query(User).filter(User.role == "tutor").all()

    return [{"id": t.id, "name": t.name, "email": t.email} for t in tutors]


# ============================================================
# 🔹 ESQUEMA PARA ELEGIR TUTOR
# ============================================================
class TutorChoice(BaseModel):
    tutor_id: int


# ============================================================
# 🔹 ELEGIR TUTOR SOLO UNA VEZ  (ANTES DEL ENDPOINT DINÁMICO)
# ============================================================
@router.post("/choose-tutor")
def choose_tutor(
    data: TutorChoice,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    log(f"User {current_user.id} escoge tutor {data.tutor_id}")

    if current_user.role != "student":
        raise HTTPException(403, "Solo estudiantes pueden elegir tutor")

    student = db.query(Student).filter(Student.user_id == current_user.id).first()

    if not student:
        raise HTTPException(404, "Estudiante no existe")

    if student.tutor_id:
        raise HTTPException(400, "Ya elegiste tutor")

    tutor = (
        db.query(User).filter(User.id == data.tutor_id, User.role == "tutor").first()
    )
    if not tutor:
        raise HTTPException(404, "Tutor no existe")

    student.tutor_id = data.tutor_id
    db.commit()

    return {"message": "Tutor asignado correctamente"}


# ============================================================
# 🔹 LISTA DE ESTUDIANTES PAGINADA
# ============================================================
@router.get("/")
def get_students(db: Session = Depends(get_db), page: int = 1, limit: int = 10):

    offset = (page - 1) * limit
    total = db.query(Student).count()

    students = db.query(Student).offset(offset).limit(limit).all()

    response = []
    for s in students:
        last = s.predictions[-1] if s.predictions else None
        response.append(
            {
                "id": s.id,
                "nombre": s.nombre,
                "academic_performance": last.predicted_label if last else "Sin datos",
                "score": round(last.predicted_score * 100, 2) if last else None,
            }
        )

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit,
        "results": response,
    }


# ============================================================
# 🔹 DETALLE DEL ESTUDIANTE  (ENDPOINT DINÁMICO)
# ============================================================
@router.get("/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):

    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(404, "Estudiante no encontrado")

    last = student.predictions[-1] if student.predictions else None

    return {
        "id": student.id,
        "nombre": student.nombre,
        "academic_performance": last.predicted_label if last else "Sin datos",
        "score": round(last.predicted_score * 100, 2) if last else None,
        "raw": student.to_payload(),
    }
