# app/utils/step_4_generate_predictions.py

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.student_model import Student
from app.models.prediction_model import Prediction
from app.services.predictor import predict_from_payload


def generate_predictions():
    print("🔍 Generando predicciones...")

    db = SessionLocal()
    students = db.query(Student).all()

    for st in students:
        try:
            payload = st.to_payload()
            predicted_class, raw_score, proba = predict_from_payload(payload)

            if isinstance(raw_score, dict):
                raw_score = max(raw_score.values())

            pred = Prediction(
                student_id=st.id,
                predicted_label=predicted_class,
                predicted_score=float(raw_score),
            )

            db.add(pred)

        except Exception as e:
            print(f"❌ Error con estudiante {st.id}: {e}")

    db.commit()
    print("✔ Predicciones generadas")


if __name__ == "__main__":
    generate_predictions()
