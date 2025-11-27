from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[int] = None  # si viene vacío → crear nueva sesión
    student_id: Optional[int] = None  # alumno al que se refiere el chat


class ChatMessageSchema(BaseModel):
    id: int
    sender: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True  # ✅ FIX para permitir .from_orm()


class ChatResponse(BaseModel):
    session_id: int
    response: str
    messages: Optional[List[ChatMessageSchema]] = None

    class Config:
        from_attributes = True  # ✅ también aquí
