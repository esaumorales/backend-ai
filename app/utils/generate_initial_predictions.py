from app.core.database import SessionLocal
from app.models.student_model import Student
from app.models.prediction_model import Prediction
from app.services.predictor import predict_from_payload

# Importar mapeos
from app.utils.mappers import (
    map_study_hours,
    map_social_media,
    map_netflix,
    map_attendance,
    map_sleep,
    map_exercise,
    map_mental_health,
    map_anxiety,
    map_financial_stress,
    map_focus,
    map_motivation,
    map_self_efficacy,
    map_time_management,
    map_study_techniques,
    map_resources,
)

print("🔍 Generando predicciones...")

db = SessionLocal()
students = db.query(Student).all()

for st in students:
    try:
        payload = {
            "study_hours_per_day": map_study_hours(st.study_hours_per_day),
            "exercise_frequency": map_exercise(st.exercise_frequency),
            "focus_level": map_focus(st.focus_level),
            "study_resources_availability": map_resources(
                st.study_resources_availability
            ),
            "social_media_hours": map_social_media(st.social_media_hours),
            "mental_health_rating": map_mental_health(st.mental_health_rating),
            "test_anxiety_level": map_anxiety(st.test_anxiety_level),
            "financial_stress_level": map_financial_stress(st.financial_stress_level),
            "netflix_hours": map_netflix(st.netflix_hours),
            "academic_motivation": map_motivation(st.academic_motivation),
            "academic_self_efficacy": map_self_efficacy(st.academic_self_efficacy),
            "attendance_percentage": map_attendance(st.attendance_percentage),
            "time_management": map_time_management(st.time_management),
            "study_techniques_usage": map_study_techniques(st.study_techniques_usage),
            "home_study_environment": map_resources(st.home_study_environment),
            "sleep_hours": map_sleep(st.sleep_hours),
        }

        predicted_class, score, probs = predict_from_payload(payload)

        pred = Prediction(
            student_id=st.id,
            predicted_label=predicted_class,
            predicted_score=score,
        )
        db.add(pred)

    except Exception as e:
        print(f"❌ Error con estudiante {st.id}: {e}")

db.commit()
db.close()

print("✔ Predicciones generadas correctamente.")
