import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import SessionLocal, engine, Base
from app.models.student_model import Student
from app.models.prediction_model import Prediction

FILE_PATH = "app/data/Data_redes_bayesianas_riesgo.txt"
DEFAULT_TUTOR_ID = 3


def reset_tables():
    print("🧹 Desactivando restricciones de FOREIGN KEY...")
    with engine.connect() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
        conn.commit()

        print("🗑️ Eliminando tablas 'predictions' y 'students' si existen...")
        conn.execute(text("DROP TABLE IF EXISTS predictions;"))
        conn.execute(text("DROP TABLE IF EXISTS students;"))
        conn.commit()

        print("🔒 Reactivando FOREIGN KEY checks...")
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
        conn.commit()

    print("📌 Recreando tablas limpias...")
    Base.metadata.create_all(bind=engine)


def insert_student(db, nombre, data):
    student = Student(
        nombre=nombre,
        tutor_id=DEFAULT_TUTOR_ID,

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
        # 🔥 Resetear tablas
        reset_tables()

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
            insert_student(db, caso["nombre"], caso)

        print("📌 Insertando estudiantes desde el dataset...")

        base_index = 5
        for idx, row in df.iterrows():
            data = row.to_dict()
            insert_student(db, f"Estudiante {base_index + idx}", data)

        print("🎉 TODOS LOS ESTUDIANTES HAN SIDO CARGADOS CORRECTAMENTE ✔")

    except Exception as e:
        print("❌ Error cargando los estudiantes:", e)
        db.rollback()

    finally:
        db.close()


if __name__ == "__main__":
    load_students()
