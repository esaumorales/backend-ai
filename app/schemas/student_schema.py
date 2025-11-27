from pydantic import BaseModel


class StudentCreate(BaseModel):
    nombre: str

    # 17 variables numéricas usadas por el modelo de clustering
    study_hours_per_day: float
    social_media_hours: float
    netflix_hours: float

    attendance_percentage: float
    sleep_hours: float
    exercise_frequency: float

    mental_health_rating: float
    academic_motivation: float
    time_management: float

    procrastination_level: float
    focus_level: float
    test_anxiety_level: float

    academic_self_efficacy: float
    study_techniques_usage: float
    home_study_environment: float

    study_resources_availability: float
    financial_stress_level: float


class StudentResponse(StudentCreate):
    id: int

    class Config:
        orm_mode = True
