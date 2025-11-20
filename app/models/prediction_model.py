from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from datetime import datetime
from app.core.database import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    predicted_class = Column(String(50))
    probabilities_json = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
