from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.student_model import Student
from app.models.prediction_model import Prediction
from app.services.predictor import predict_from_payload


def generate_predictions_for_all():
    db: Session = SessionLocal()

    try:
        students = db.query(Student).all()
        total = len(students)

        if total == 0:
            print("⚠ No hay estudiantes en la base de datos.")
            return

        print(f"🔍 Generando predicciones para {total} estudiantes...")

        count = 0
        for s in students:
            payload = s.to_payload()  # vector de entrada para el modelo

            label, score, proba_dict = predict_from_payload(payload)

            pred = Prediction(
                student_id=s.id,
                predicted_label=label,
                predicted_score=score
            )

            db.add(pred)
            count += 1

        db.commit()
        print(f"🎉 Predicciones generadas correctamente para {count} estudiantes.")

    except Exception as e:
        print("❌ Error generando predicciones:", e)
        db.rollback()

    finally:
        db.close()


if __name__ == "__main__":
    generate_predictions_for_all()
