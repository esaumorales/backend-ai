from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import json
from app.services.predictor import predict_from_payload
from app.schemas.prediction_schema import PredictionResponse
from app.core.database import SessionLocal
from app.models.prediction_model import Prediction

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=PredictionResponse)
def predict(data: dict, db: Session = Depends(get_db)):

    predicted_class, probabilities = predict_from_payload(data)

    db_pred = Prediction(
        student_id=data.get("student_id", None),
        predicted_class=predicted_class,
        probabilities_json=json.dumps(probabilities)
    )
    db.add(db_pred)
    db.commit()

    return PredictionResponse(
        predicted_class=predicted_class,
        probabilities=probabilities
    )
