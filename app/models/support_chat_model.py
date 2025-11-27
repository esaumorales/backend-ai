from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class SupportChatSession(Base):
    __tablename__ = "support_chat_sessions"

    id = Column(Integer, primary_key=True, index=True)

    # 🔥 Correcto: el estudiante es una fila de students, no de users
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)

    # 🔥 Correcto: el tutor es un user
    tutor_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    messages = relationship(
        "SupportChatMessage",
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="SupportChatMessage.created_at",
    )


class SupportChatMessage(Base):
    __tablename__ = "support_chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("support_chat_sessions.id"), nullable=False)
    sender = Column(String(20), nullable=False)  # "student" | "tutor"
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("SupportChatSession", back_populates="messages")
