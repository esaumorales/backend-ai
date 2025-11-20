# app/utils/step_4_generate_predictions.py

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.student_model import Student
from app.models.prediction_model import Prediction
from app.services.predictor import predict_from_payload

from app.models import user_model, student_model, prediction_model  # IMPORTANTE


def generate_predictions():
    print("🔍 Generando predicciones para todos los estudiantes...")

    db: Session = SessionLocal()

    try:
        students = db.query(Student).all()
        total = len(students)

        if total == 0:
            print("⚠ No hay estudiantes en la base de datos.")
            return

        print(f"📌 Total estudiantes encontrados: {total}")

        for i, student in enumerate(students, start=1):

            try:
                payload = student.to_payload()

                # Ejecutar modelo
                predicted_class, probabilities, _ = predict_from_payload(payload)

                score = float(probabilities[predicted_class])

                pred = Prediction(
                    student_id=student.id,
                    predicted_label=predicted_class,
                    predicted_score=score
                )
                db.add(pred)

                if i % 50 == 0:
                    print(f"   → {i}/{total} predicciones generadas...")

            except Exception as e:
                print(f"❌ Error con estudiante ID={student.id}: {e}")
                continue

        db.commit()
        print("🎉 PREDICCIONES GENERADAS EXITOSAMENTE ✔")

    except Exception as e:
        print("❌ Error general:", e)
        db.rollback()

    finally:
        db.close()


if __name__ == "__main__":
    generate_predictions()
