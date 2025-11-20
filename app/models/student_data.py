from pydantic import BaseModel
from typing import Dict


class StudentData(BaseModel):
    # Campos que vas a recoger desde el frontend
    sleep_hours: str
    attendance_percentage: str
    time_management: str
    study_techniques_usage: str
    study_hours_per_day: str
    social_media_hours: str
    mental_health_rating: str
    test_anxiety_level: str
    exercise_frequency: str
    focus_level: str
    study_resources_availability: str


class PredictionResponse(BaseModel):
    predicted_class: str
    probabilities: Dict[str, float]
