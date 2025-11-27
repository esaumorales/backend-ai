# app/routers/analytics_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from joblib import load
import numpy as np

from app.core.database import SessionLocal
from app.models.student_model import Student
from app.models.user_model import User
from app.routers.auth_router import get_current_user

router = APIRouter(tags=["Analytics / Clustering"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================
# Cargar modelos entrenados (SCALER + KMEANS)
# ============================================================
try:
    scaler = load("app/artifacts/students_scaler.joblib")
    kmeans = load("app/artifacts/students_kmeans_k2.joblib")
    print("🚀 Modelos cargados correctamente")
except Exception as e:
    print("❌ Error cargando modelos:", e)
    scaler = None
    kmeans = None


# ============================================================
# CAMPOS EXACTOS DEL ENTRENAMIENTO (17 VARIABLES)
# ============================================================
FIELDS = [
    "study_hours_per_day",
    "social_media_hours",
    "netflix_hours",
    "attendance_percentage",
    "sleep_hours",
    "exercise_frequency",
    "mental_health_rating",
    "academic_motivation",
    "time_management",
    "procrastination_level",
    "focus_level",
    "test_anxiety_level",
    "academic_self_efficacy",
    "study_techniques_usage",
    "home_study_environment",
    "study_resources_availability",
    "financial_stress_level",
]


# ============================================================
# MAPEOS → convertir strings a números de forma estable
# ============================================================
MAPS = {
    "sleep_hours": {"Cortas": 1, "Normal": 2, "Largas": 3},
    "attendance_percentage": {"Irregular": 1, "Regular": 2, "Constante": 3},
    "time_management": {"Malo": 1, "Adecuado": 2, "Excelente": 3},
    "study_techniques_usage": {"Basico": 1, "Intermedio": 2, "Avanzado": 3},
    "study_hours_per_day": {"Cortas": 1, "Adecuadas": 2, "Altas": 3},
    "social_media_hours": {"Bajo": 1, "Moderado": 2, "Excesivo": 3},
    "mental_health_rating": {"Buena": 1, "Regular": 2, "Delicada": 3},
    "test_anxiety_level": {"Leve": 1, "Moderado": 2, "Severa": 3},
    "exercise_frequency": {"Sedentario": 1, "Ocasional": 2, "Frecuente": 3},
    "focus_level": {"Enfocado": 1, "Promedio": 2, "Disperso": 3},
    "study_resources_availability": {"Escasos": 1, "Regulares": 2, "Suficientes": 3},
    "procrastination_level": {"Bajo": 1, "Intermedio": 2, "Alto": 3},
    "home_study_environment": {"Malo": 1, "Aceptable": 2, "Bueno": 3},
    "financial_stress_level": {"Bajo": 1, "Medio": 2, "Alto": 3},
}


# ============================================================
# Convertir estudiante → vector EXACTO del entrenamiento
# ============================================================
def student_to_vector(student: Student):
    payload = student.to_payload()
    row = []

    for f in FIELDS:
        v = payload.get(f)

        if isinstance(v, (float, int)):
            row.append(float(v))
            continue

        if f in MAPS:
            row.append(float(MAPS[f].get(v, 2)))
        else:
            row.append(2.0)

    return np.array(row, dtype=float)


# ============================================================
# ENDPOINT → obtener todos los clusters
# ============================================================
@router.get("/clusters")
def get_clusters(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    if current_user.role != "tutor":
        raise HTTPException(403, "No autorizado")

    students = db.query(Student).all()
    clusters = {}

    for st in students:
        try:
            vec = student_to_vector(st)
            scaled = scaler.transform([vec])
            cid = int(kmeans.predict(scaled)[0])
        except Exception as e:
            print(f"❌ Error con estudiante {st.id}: {e}")
            cid = -1

        clusters.setdefault(
            cid,
            {
                "cluster": cid,
                "description": "Alto rendimiento" if cid == 0 else "Riesgo académico",
                "students": [],
            },
        )

        clusters[cid]["students"].append(
            {"id": st.id, "nombre": st.nombre, "tutor_id": st.tutor_id}
        )

    return list(clusters.values())
