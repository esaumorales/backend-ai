import os
from typing import Optional

import google.generativeai as genai
from sqlalchemy.orm import Session

from app.models.student_model import Student
from app.models.prediction_model import Prediction
from app.models.user_model import User

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Modelo de Gemini
model = genai.GenerativeModel("models/gemini-2.5-flash")


async def generate_chat_response(
    db: Session,
    current_user: User,
    message: str,
    student_id: Optional[int] = None,
) -> str:
    """
    Genera una respuesta de IA con contexto del alumno y predicciones.
    """

    student_context = "No se ha especificado un alumno en esta conversación."
    prediction_context = "No hay predicciones registradas para este alumno."

    # ============================
    #   CONTEXTO DEL ALUMNO
    # ============================
    if student_id is not None:
        student = db.query(Student).filter(Student.id == student_id).first()

        if student:
            student_context = f"""
Alumno ID: {student.id}
Nombre: {student.nombre}

Sueño: {student.sleep_hours}
Asistencia: {student.attendance_percentage}
Gestión del tiempo: {student.time_management}
Uso de técnicas de estudio: {student.study_techniques_usage}
Horas de estudio por día: {student.study_hours_per_day}
Uso de redes sociales: {student.social_media_hours}
Salud mental: {student.mental_health_rating}
Ansiedad en exámenes: {student.test_anxiety_level}
Ejercicio físico: {student.exercise_frequency}
Nivel de enfoque: {student.focus_level}
Recursos de estudio disponibles: {student.study_resources_availability}
Rendimiento académico observado: {student.academic_performance}
""".strip()

            last_pred = (
                db.query(Prediction)
                .filter(Prediction.student_id == student.id)
                .order_by(Prediction.created_at.desc())
                .first()
            )

            if last_pred:
                prediction_context = (
                    f"Rendimiento predicho por el modelo: {last_pred.predicted_label} "
                    f"con score {round(last_pred.predicted_score * 100, 2)}%."
                )
            else:
                prediction_context = "Aún no hay predicción generada para este alumno."
        else:
            student_context = "El alumno indicado no existe."
            prediction_context = "No se puede obtener predicción."

    # ============================
    #   ROL DEL USUARIO
    # ============================
    role_text = (
        "Eres un asistente académico que ayuda a TUTORES a analizar casos de estudiantes."
        if getattr(current_user, "role", None) == "tutor"
        else "Eres un asistente académico que aconseja a ESTUDIANTES sobre cómo mejorar."
    )

    # ============================
    #   PROMPT FINAL (VERSIÓN CORTA)
    # ============================
    prompt = f"""
{role_text}

Contexto del alumno:
{student_context}

Predicción:
{prediction_context}

Instrucciones IMPORTANTES para tu respuesta:
- Responde de forma corta, clara y amable.
- NO uses markdown, títulos, ni símbolos como #, *, -, etc.
- Organiza la respuesta SOLO en 3 párrafos naturales:
  
  1) Primer párrafo: explica lo positivo del alumno, máximo 2 frases.
  
  2) Segundo párrafo: explica lo que está en riesgo, máximo 3 frases.
  
  3) Tercer párrafo: da 2 o 3 acciones concretas para mejorar. Escríbelas como texto normal, sin viñetas ni símbolos.

- No repitas demasiados datos. Resume lo esencial.
- Mantente profesional y académico, sin lenguaje clínico.
- No inventes datos que no están en el contexto.

Mensaje del usuario:
\"\"\"{message}\"\"\"
"""

    # ============================
    #   GENERAR RESPUESTA IA
    # ============================
    try:
        response = model.generate_content(prompt)

        # Gemini a veces no devuelve texto → lo manejamos
        if not response or not hasattr(response, "text") or not response.text:
            return (
                "Lo siento, no pude generar una respuesta en este momento. "
                "¿Puedes intentar reformular tu pregunta?"
            )

        return response.text

    except Exception as e:
        return f"Ocurrió un error al generar respuesta: {e}"
