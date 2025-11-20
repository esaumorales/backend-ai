# app/models/student_model.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)

    tutor_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Variables del dataset
    study_hours_per_day = Column(String(50))
    exercise_frequency = Column(String(50))
    focus_level = Column(String(50))
    study_resources_availability = Column(String(50))
    social_media_hours = Column(String(50))
    mental_health_rating = Column(String(50))
    test_anxiety_level = Column(String(50))
    financial_stress_level = Column(String(50))
    netflix_hours = Column(String(50))
    academic_motivation = Column(String(50))
    academic_self_efficacy = Column(String(50))
    attendance_percentage = Column(String(50))
    time_management = Column(String(50))
    study_techniques_usage = Column(String(50))
    procrastination_level = Column(String(50))
    sleep_hours = Column(String(50))
    home_study_environment = Column(String(50))
    academic_performance = Column(String(50))

    created_at = Column(DateTime, default=datetime.utcnow)

    # relación con predicciones
    predictions = relationship(
        "Prediction",
        back_populates="student",
        cascade="all, delete-orphan",
    )

    def to_payload(self) -> dict:
        """
        Devuelve un diccionario con las features EXACTAS
        que espera el modelo entrenado.
        """
        return {
            "study_hours_per_day": self.study_hours_per_day,
            "exercise_frequency": self.exercise_frequency,
            "focus_level": self.focus_level,
            "study_resources_availability": self.study_resources_availability,
            "social_media_hours": self.social_media_hours,
            "mental_health_rating": self.mental_health_rating,
            "test_anxiety_level": self.test_anxiety_level,
            "financial_stress_level": self.financial_stress_level,
            "netflix_hours": self.netflix_hours,
            "academic_motivation": self.academic_motivation,
            "academic_self_efficacy": self.academic_self_efficacy,
            "attendance_percentage": self.attendance_percentage,
            "time_management": self.time_management,
            "study_techniques_usage": self.study_techniques_usage,
            "procrastination_level": self.procrastination_level,
            "sleep_hours": self.sleep_hours,
            "home_study_environment": self.home_study_environment,
            "AcademicPerformance": self.academic_performance,
        }
