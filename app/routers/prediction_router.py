# app/routers/prediction_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.services.predictor import predict_from_payload
from app.models.student_model import Student
from app.models.user_model import User
from app.models.prediction_model import Prediction
from app.routers.auth_router import get_current_user

router = APIRouter(tags=["Prediction"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------
# NORMALIZADOR DE CATEGORÍAS
# ---------------------------

MAP_INPUT = {
    # Sueño
    "Insuficiente": "Insuficiente",
    "Normal": "Normal",
    # Horas de estudio
    "Cortas": "Cortas",
    "Adecuadas": "Adecuadas",
    "Intensas": "Intensas",
    # Asistencia
    "Irregular": "Irregular",
    "Regular": "Regular",
    "Constante": "Constante",
    # Redes sociales / entretenimiento
    "Ligero": "Ligero",
    "Moderado": "Moderado",
    "Excesivo": "Excesivo",
    "Poco": "Poco",  # 🔥 IMPORTANTE
    # Ejercicio
    "Sedentario": "Sedentario",
    "Activo": "Activo",
    "Frecuente": "Frecuente",
    # Salud mental
    "Delicada": "Delicada",
    "Óptima": "Optima",
    "Optima": "Optima",
    # Motivación
    "Limitada": "Limitada",
    "Media": "Media",
    "Alta": "Alta",
    # Enfoque
    "Disperso": "Disperso",
    "Concentrado": "Concentrado",
    # Gestión del tiempo
    "Caótico": "Caotico",
    "Caotico": "Caotico",
    "Adecuado": "Adecuado",
    # Ansiedad
    "Leve": "Leve",
    "Moderada": "Moderada",
    "Severa": "Severa",
    # Autoeficacia
    "Confiado": "Confiado",
    "Muy_Confiado": "Muy_Confiado",
    "Poco_Confiado": "Poco_Confiado",
    # Técnicas de estudio
    "Básico": "Basico",
    "Basico": "Basico",
    "Intermedio": "Intermedio",
    "Avanzado": "Avanzado",
    # Recursos / Entorno
    "Escaso": "Escasos",
    "Escasos": "Escasos",
    "Suficientes": "Suficientes",
    # Estrés financiero
    "Alto": "Alto",
    "Medio": "Medio",
    "Bajo": "Bajo",
}


def normalize(data: dict):
    """Corrige valores para que coincidan con las categorías del modelo MLP."""
    fixed = {}
    for k, v in data.items():
        fixed[k] = MAP_INPUT.get(v, v)
    return fixed


@router.post("/")
def predict_myself(
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Solo estudiantes pueden predecir
    if current_user.role != "student":
        raise HTTPException(403, "Solo estudiantes pueden predecir")

    # Obtener registro del estudiante
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(404, "No existe registro de estudiante")

    # Guardar hábitos
    for key, value in payload.items():
        if hasattr(student, key):
            setattr(student, key, value)

    db.commit()

    # 🔥 Normalizar antes de predecir
    clean = normalize(payload)

    # Ejecutar predicción
    predicted_class, score, probabilities = predict_from_payload(clean)

    # Guardar historial
    pred = Prediction(
        student_id=student.id,
        predicted_label=predicted_class,
        predicted_score=float(score),
    )

    db.add(pred)
    db.commit()

    return {
        "prediction": predicted_class,
        "score": round(score * 100, 2),
        "probabilities": probabilities,
    }
