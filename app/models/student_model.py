from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from app.core.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    tutor_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    sleep_hours = Column(String(50))
    attendance_percentage = Column(String(50))
    time_management = Column(String(50))
    study_techniques_usage = Column(String(50))
    study_hours_per_day = Column(String(50))
    social_media_hours = Column(String(50))
    mental_health_rating = Column(String(50))
    test_anxiety_level = Column(String(50))
    exercise_frequency = Column(String(50))
    focus_level = Column(String(50))
    study_resources_availability = Column(String(50))
    academic_performance = Column(String(50))

    created_at = Column(DateTime, default=datetime.utcnow)
