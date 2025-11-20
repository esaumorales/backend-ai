from pydantic import BaseModel

class StudentCreate(BaseModel):
    nombre: str
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
    academic_performance: str

class StudentResponse(StudentCreate):
    id: int

    class Config:
        orm_mode = True
