# app/models/student_model.py

from sqlalchemy import Column, Integer, Text, Float, String, ForeignKey, DateTime
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
    study_hours_per_day = Column(Text)
    social_media_hours = Column(Text)
    netflix_hours = Column(Text)

    attendance_percentage = Column(Text)
    sleep_hours = Column(Text)
    exercise_frequency = Column(Text)

    mental_health_rating = Column(Text)
    academic_motivation = Column(Text)
    time_management = Column(Text)

    procrastination_level = Column(Text)
    focus_level = Column(Text)
    test_anxiety_level = Column(Text)

    academic_self_efficacy = Column(Text)
    study_techniques_usage = Column(Text)
    home_study_environment = Column(Text)

    study_resources_availability = Column(Text)
    financial_stress_level = Column(Text)

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

        def safe_float(value):
            try:
                return float(value)
            except:
                return 0.0

        return {
            "study_hours_per_day": safe_float(self.study_hours_per_day),
            "social_media_hours": safe_float(self.social_media_hours),
            "netflix_hours": safe_float(self.netflix_hours),
            "attendance_percentage": safe_float(self.attendance_percentage),
            "sleep_hours": safe_float(self.sleep_hours),
            "exercise_frequency": safe_float(self.exercise_frequency),
            "mental_health_rating": safe_float(self.mental_health_rating),
            "academic_motivation": safe_float(self.academic_motivation),
            "time_management": safe_float(self.time_management),
            "procrastination_level": safe_float(self.procrastination_level),
            "focus_level": safe_float(self.focus_level),
            "test_anxiety_level": safe_float(self.test_anxiety_level),
            "academic_self_efficacy": safe_float(self.academic_self_efficacy),
            "study_techniques_usage": safe_float(self.study_techniques_usage),
            "home_study_environment": safe_float(self.home_study_environment),
            "study_resources_availability": safe_float(
                self.study_resources_availability
            ),
            "financial_stress_level": safe_float(self.financial_stress_level),
        }
