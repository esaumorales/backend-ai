# app/models/prediction_model.py
from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)

    predicted_label = Column(String(50), nullable=False)
    predicted_score = Column(Float, nullable=False)  # 0.0 a 1.0

    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="predictions")
