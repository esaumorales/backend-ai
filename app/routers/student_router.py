# app/routers/student_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.student_model import Student
from app.models.prediction_model import Prediction

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_students(
    db: Session = Depends(get_db),
    page: int = 1,
    limit: int = 10
):
    if page < 1:
        page = 1

    offset = (page - 1) * limit

    total = db.query(Student).count()

    students = (
        db.query(Student)
        .offset(offset)
        .limit(limit)
        .all()
    )

    response = []
    for s in students:
        last = s.predictions[-1] if s.predictions else None
        response.append({
            "id": s.id,
            "nombre": s.nombre,
            "academic_performance": last.predicted_label if last else "Sin datos",
            "score": round(last.predicted_score * 100, 2) if last else None,
        })

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit,
        "results": response
    }



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


@router.get("/{student_id}/predictions")
def get_student_predictions(
    student_id: int,
    db: Session = Depends(get_db),
    page: int = 1,
    limit: int = 10
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(404, "Estudiante no encontrado")

    if page < 1:
        page = 1

    offset = (page - 1) * limit

    total = (
        db.query(Prediction)
        .filter(Prediction.student_id == student_id)
        .count()
    )

    preds = (
        db.query(Prediction)
        .filter(Prediction.student_id == student_id)
        .order_by(Prediction.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit,
        "results": [
            {
                "id": p.id,
                "label": p.predicted_label,
                "score": round(p.predicted_score * 100, 2),
                "created_at": p.created_at,
            }
            for p in preds
        ]
    }
