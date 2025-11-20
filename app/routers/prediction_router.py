# app/routers/prediction_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.services.predictor import predict_from_payload
from app.models.student_model import Student
from app.models.prediction_model import Prediction

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/{student_id}")
def predict(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(404, "Estudiante no encontrado")

    payload = student.to_payload()
    predicted_class, probabilities, score = predict_from_payload(payload)

    pred = Prediction(
        student_id=student_id,
        predicted_label=predicted_class,
        predicted_score=score,
    )
    db.add(pred)
    db.commit()
    db.refresh(pred)

    return {
        "student_id": student_id,
        "label": predicted_class,
        "score": round(score * 100, 2),
        "probabilities": probabilities,
    }
