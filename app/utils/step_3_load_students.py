# app/utils/step_3_load_students.py

import pandas as pd
import random
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.student_model import Student

# IMPORTANTE para que SQLAlchemy registre los modelos
from app.models import user_model, student_model, prediction_model


FILE_PATH = "app/data/Data_redes_bayesianas_riesgo.txt"


# -----------------------------
# Nombres aleatorios
# -----------------------------
NOMBRES = [
    "Juan","Carlos","Luis","Pedro","Miguel","Ana","María","Lucía","Carla","Paola",
    "Jorge","Andrés","Sofía","Camila","Valentina","Daniel","Fernando",
    "Rosa","Carmen","Julia","Gabriel","Sebastián","Alejandro","Ignacio","Diego"
]

APELLIDOS = [
    "Quispe","Huamán","García","Torres","Flores","Ramírez","Sánchez","Vargas",
    "Rojas","Medina","Castro","López","Gómez","Reyes","Navarro","Mendoza",
    "Paredes","Valverde","Salazar","Cáceres"
]


def random_name():
    return f"{random.choice(NOMBRES)} {random.choice(APELLIDOS)}"


# -----------------------------
# LIMPIAR FILAS (remover columnas que NO existen)
# -----------------------------
CAMPOS_VALIDOS = [
    "sleep_hours",
    "attendance_percentage",
    "time_management",
    "study_techniques_usage",
    "study_hours_per_day",
    "social_media_hours",
    "mental_health_rating",
    "test_anxiety_level",
    "exercise_frequency",
    "focus_level",
    "study_resources_availability",
    "AcademicPerformance"
]

def clean_row(row_dict):
    filtered = {}

    for key, value in row_dict.items():
        if key in CAMPOS_VALIDOS:
            filtered[key] = value

    # AcademicPerformance → academic_performance
    if "AcademicPerformance" in filtered:
        filtered["academic_performance"] = filtered.pop("AcademicPerformance")

    return filtered


# -----------------------------
# INSERTAR
# -----------------------------
def insert_students(tutor_id: int):
    db: Session = SessionLocal()

    print("📥 Leyendo dataset...")
    df = pd.read_csv(FILE_PATH, sep="\t")

    print("📌 Insertando CASOS ESPECIALES...")

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
            "academic_performance": "Excelente"
        },
        {
            "nombre": "Alumno Caso 2",
            "study_hours_per_day": "Cortas",
            "attendance_percentage": "Irregular",
            "social_media_hours": "Excesivo",
            "mental_health_rating": "Delicada",
            "test_anxiety_level": "Severa",
            "exercise_frequency": "Sedentario",
            "academic_performance": "Insuficiente"
        },
        {
            "nombre": "Alumno Caso 3",
            "focus_level": "Disperso",
            "study_hours_per_day": "Adecuadas",
            "attendance_percentage": "Regular",
            "study_techniques_usage": "Basico",
            "academic_performance": "Satisfactorio"
        },
        {
            "nombre": "Alumno Caso 4",
            "sleep_hours": "Normal",
            "study_hours_per_day": "Adecuadas",
            "attendance_percentage": "Regular",
            "study_resources_availability": "Suficientes",
            "academic_performance": "Satisfactorio"
        }
    ]

    for c in casos:
        st = Student(tutor_id=tutor_id, **c)
        db.add(st)

    print("📌 Insertando dataset real...")

    for _, row in df.iterrows():
        cleaned = clean_row(row.to_dict())
        nombre = random_name()

        st = Student(tutor_id=tutor_id, nombre=nombre, **cleaned)
        db.add(st)

    db.commit()
    print("✔ Estudiantes insertados correctamente")


if __name__ == "__main__":
    insert_students(1)
