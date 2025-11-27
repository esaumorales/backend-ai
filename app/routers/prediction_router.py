# app/routers/prediction_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.services.predictor import predict_from_payload
from app.models.student_model import Student
from app.models.user_model import User
from app.models.prediction_model import Prediction
from app.routers.auth_router import get_current_user

router = APIRouter(tags=["Prediction"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def predict_myself(
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Solo estudiantes pueden predecir
    if current_user.role != "student":
        raise HTTPException(403, "Solo estudiantes pueden predecir")

    # Obtener registro del estudiante
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(404, "No existe registro de estudiante")

    # Guardar hábitos antes de predecir
    for key, value in payload.items():
        if hasattr(student, key):
            setattr(student, key, value)

    db.commit()

    # Ejecutar predicción
    predicted_class, score, probabilities = predict_from_payload(payload)

    # Guardar predicción en historial
    pred = Prediction(
        student_id=student.id,
        predicted_label=predicted_class,
        predicted_score=float(score),
    )

    db.add(pred)
    db.commit()

    return {
        "prediction": predicted_class,
        "score": round(score * 100, 2),
        "probabilities": probabilities,
    }
