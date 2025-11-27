# app/routers/chat_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.schemas.chat_schema import ChatRequest, ChatResponse, ChatMessageSchema
from app.services.chat_service import generate_chat_response
from app.models.chat_model import ChatSession, ChatMessage
from app.models.user_model import User

from app.routers.auth_router import get_current_user

router = APIRouter(tags=["Chat"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    payload: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 1. Obtener o crear sesión
    session = None

    if payload.session_id:
        session = (
            db.query(ChatSession)
            .filter(
                ChatSession.id == payload.session_id,
                ChatSession.user_id == current_user.id,
            )
            .first()
        )
        if not session:
            raise HTTPException(status_code=404, detail="Sesión de chat no encontrada")
    else:
        session = ChatSession(
            user_id=current_user.id,
            student_id=payload.student_id,
        )
        db.add(session)
        db.commit()
        db.refresh(session)

    # 2. Guardar mensaje del usuario
    user_msg = ChatMessage(
        session_id=session.id,
        sender="user",
        content=payload.message,
    )
    db.add(user_msg)
    db.commit()
    db.refresh(user_msg)

    # 3. Llamar a la IA
    reply_text = await generate_chat_response(
        db=db,
        current_user=current_user,
        message=payload.message,
        student_id=session.student_id,
    )

    # 4. Guardar respuesta
    ai_msg = ChatMessage(
        session_id=session.id,
        sender="ai",
        content=reply_text,
    )
    db.add(ai_msg)
    db.commit()
    db.refresh(ai_msg)

    # 5. Devolver historial
    messages = [ChatMessageSchema.from_orm(m) for m in session.messages]

    return ChatResponse(
        session_id=session.id,
        response=reply_text,
        messages=messages,
    )


@router.get("/sessions")
def list_support_sessions(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    if current_user.role == "tutor":
        sessions = (
            db.query(SupportChatSession)
            .filter(SupportChatSession.tutor_id == current_user.id)
            .order_by(SupportChatSession.created_at.desc())
            .all()
        )
        return [s.id for s in sessions]

    # 🔥 ESTUDIANTE — FIX REAL
    student = db.query(Student).filter(Student.user_id == current_user.id).first()

    if not student:
        return []

    sessions = (
        db.query(SupportChatSession)
        .filter(SupportChatSession.student_id == student.id)
        .order_by(SupportChatSession.created_at.desc())
        .all()
    )

    return [s.id for s in sessions]


@router.get("/sessions/{session_id}/messages", response_model=list[ChatMessageSchema])
def get_session_messages(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = (
        db.query(ChatSession)
        .filter(
            ChatSession.id == session_id,
            ChatSession.user_id == current_user.id,
        )
        .first()
    )
    if not session:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")

    return [ChatMessageSchema.from_orm(m) for m in session.messages]
