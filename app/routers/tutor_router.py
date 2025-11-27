# app/routers/tutor_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import SessionLocal
from app.models.student_model import Student
from app.models.prediction_model import Prediction

router = APIRouter(tags=["Tutor"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/dashboard")
def tutor_dashboard(db: Session = Depends(get_db)):

    total_students = db.query(func.count(Student.id)).scalar()
    total_predictions = db.query(func.count(Prediction.id)).scalar()

    rows = (
        db.query(Prediction.predicted_label, func.count(Prediction.id))
        .group_by(Prediction.predicted_label)
        .all()
    )

    distribution = {label: count for label, count in rows}

    return {
        "total_students": total_students,
        "total_predictions": total_predictions,
        "distribution": distribution,
    }
