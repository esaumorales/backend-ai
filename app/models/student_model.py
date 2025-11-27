# app/models/student_model.py

from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)

    # Relación con usuario (opcional)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Tutor asignado
    tutor_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    nombre = Column(String(100), nullable=False)

    # ============================================================
    # 🔹 VARIABLES NUMÉRICAS (17 FEATURES DEL CLUSTERING)
    # ============================================================
    study_hours_per_day = Column(Float)
    social_media_hours = Column(Float)
    netflix_hours = Column(Float)

    attendance_percentage = Column(Float)
    sleep_hours = Column(Float)
    exercise_frequency = Column(Float)

    mental_health_rating = Column(Float)
    academic_motivation = Column(Float)
    time_management = Column(Float)

    procrastination_level = Column(Float)
    focus_level = Column(Float)
    test_anxiety_level = Column(Float)

    academic_self_efficacy = Column(Float)
    study_techniques_usage = Column(Float)
    home_study_environment = Column(Float)

    study_resources_availability = Column(Float)
    financial_stress_level = Column(Float)

    # No forma parte del clustering (puedes usarla para notas finales, etc.)
    academic_performance = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    # ============================================================
    # 🔹 RELACIÓN CON PREDICTIONS (IMPORTANTE PARA EL ERROR)
    # ============================================================
    predictions = relationship(
        "Prediction",
        back_populates="student",
        cascade="all, delete-orphan",
    )

    # ============================================================
    # 🔹 PAYLOAD PARA IA (KMEANS / MLP) → SOLO NÚMEROS
    # ============================================================
    def to_payload(self) -> dict:
        return {
            "study_hours_per_day": float(self.study_hours_per_day or 0),
            "social_media_hours": float(self.social_media_hours or 0),
            "netflix_hours": float(self.netflix_hours or 0),
            "attendance_percentage": float(self.attendance_percentage or 0),
            "sleep_hours": float(self.sleep_hours or 0),
            "exercise_frequency": float(self.exercise_frequency or 0),
            "mental_health_rating": float(self.mental_health_rating or 0),
            "academic_motivation": float(self.academic_motivation or 0),
            "time_management": float(self.time_management or 0),
            "procrastination_level": float(self.procrastination_level or 0),
            "focus_level": float(self.focus_level or 0),
            "test_anxiety_level": float(self.test_anxiety_level or 0),
            "academic_self_efficacy": float(self.academic_self_efficacy or 0),
            "study_techniques_usage": float(self.study_techniques_usage or 0),
            "home_study_environment": float(self.home_study_environment or 0),
            "study_resources_availability": float(
                self.study_resources_availability or 0
            ),
            "financial_stress_level": float(self.financial_stress_level or 0),
        }
