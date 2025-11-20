import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.database import SessionLocal
from app.models.student_model import Student
from app.models.user_model import User

FILE_PATH = "app/data/Data_redes_bayesianas_riesgo.txt"


def ensure_tutor_exists(db: Session):
    """Crea el tutor principal si no existe."""
    tutor = db.execute(
        select(User).where(User.email == "tutor@gmail.com")
    ).scalar_one_or_none()

    if tutor:
        print(f"✔ Tutor ya existe con id={tutor.id}")
        return tutor.id

    print("➕ Creando tutor principal...")

    new_tutor = User(
        name="Tutor Principal",
        email="tutor@gmail.com",
        password_hash="123",
        role="tutor"
    )

    db.add(new_tutor)
    db.commit()
    db.refresh(new_tutor)

    print(f"✔ Tutor creado con id={new_tutor.id}")
    return new_tutor.id


def insert_student(db: Session, nombre: str, data: dict, tutor_id: int):
    student = Student(
        nombre=nombre,
        tutor_id=tutor_id,

        sleep_hours=data.get("sleep_hours", "Desconocido"),
        attendance_percentage=data.get("attendance_percentage", "Desconocido"),
        time_management=data.get("time_management", "Desconocido"),
        study_techniques_usage=data.get("study_techniques_usage", "Desconocido"),
        study_hours_per_day=data.get("study_hours_per_day", "Desconocido"),
        social_media_hours=data.get("social_media_hours", "Desconocido"),
        mental_health_rating=data.get("mental_health_rating", "Desconocido"),
        test_anxiety_level=data.get("test_anxiety_level", "Desconocido"),
        exercise_frequency=data.get("exercise_frequency", "Desconocido"),
        focus_level=data.get("focus_level", "Desconocido"),
        study_resources_availability=data.get("study_resources_availability", "Desconocido"),
        academic_performance=data.get("AcademicPerformance", "Desconocido"),
    )

    db.add(student)
    db.commit()


def load_students():
    print("📥 Leyendo dataset...")

    df = pd.read_csv(FILE_PATH, sep="\t")
    db: Session = SessionLocal()

    try:
        print("📌 Verificando tutor...")

        tutor_id = ensure_tutor_exists(db)

        print("📌 Insertando los 4 CASOS ESPECIALES...")

        casos = [
            {
                "nombre": "Alumno Caso 1",
                "sleep_hours": "Normal",
                "attendance_percentage": "Constante",
                "time_management": "Adecuado",
                "study_techniques_usage": "Intermedio",
                "study_hours_per_day": "Adecuadas",
                "social_media_hours": "Excesivo",
                "mental_health_rating": "Delicada",
                "test_anxiety_level": "Severa",
                "exercise_frequency": "Sedentario",
                "focus_level": "Disperso",
                "study_resources_availability": "Suficientes",
                "AcademicPerformance": "Excelente"
            },
            {
                "nombre": "Alumno Caso 2",
                "study_hours_per_day": "Cortas",
                "attendance_percentage": "Irregular",
                "social_media_hours": "Excesivo",
                "mental_health_rating": "Delicada",
                "test_anxiety_level": "Severa",
                "exercise_frequency": "Sedentario",
                "AcademicPerformance": "Insuficiente"
            },
            {
                "nombre": "Alumno Caso 3",
                "focus_level": "Disperso",
                "study_hours_per_day": "Adecuadas",
                "attendance_percentage": "Regular",
                "study_techniques_usage": "Basico",
                "AcademicPerformance": "Satisfactorio"
            },
            {
                "nombre": "Alumno Caso 4",
                "sleep_hours": "Normal",
                "study_hours_per_day": "Adecuadas",
                "attendance_percentage": "Regular",
                "study_resources_availability": "Suficientes",
                "AcademicPerformance": "Satisfactorio"
            },
        ]

        for caso in casos:
            insert_student(db, caso["nombre"], caso, tutor_id)

        print("📌 Insertando estudiantes del dataset...")

        base_index = 5
        for idx, row in df.iterrows():
            data = row.to_dict()
            insert_student(db, f"Estudiante {base_index + idx}", data, tutor_id)

        print("🎉 Datos cargados correctamente ✔")

    except Exception as e:
        print("❌ Error insertando estudiantes:", e)
        db.rollback()

    finally:
        db.close()


if __name__ == "__main__":
    load_students()
