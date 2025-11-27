from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import SessionLocal
from app.models.user_model import User
from app.models.support_chat_model import SupportChatSession, SupportChatMessage
from app.models.student_model import Student
from app.models.prediction_model import Prediction

from app.routers.auth_router import get_current_user

router = APIRouter(tags=["Soporte / Chat Humano"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==========================
# LISTA DE ESTUDIANTES (para el TUTOR)
# ==========================


@router.get("/students")
def get_students_for_chat(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    page: int = 1,
    limit: int = 20,
):
    if current_user.role != "tutor":
        raise HTTPException(403, "Solo tutores pueden acceder")

    if page < 1:
        page = 1

    offset = (page - 1) * limit

    total = db.query(Student).filter(Student.tutor_id == current_user.id).count()

    students = (
        db.query(Student)
        .filter(Student.tutor_id == current_user.id)
        .order_by(Student.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    results = []
    for s in students:
        pred = (
            db.query(Prediction)
            .filter(Prediction.student_id == s.id)
            .order_by(Prediction.created_at.desc())
            .first()
        )

        results.append(
            {
                "id": s.id,
                "nombre": s.nombre,
                "prediccion": pred.predicted_label if pred else "Sin datos",
            }
        )

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit,
        "results": results,
    }


# ==========================
# LISTA DE SESIONES
# ==========================


@router.get("/sessions")
def list_support_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Tutor: filtra por tutor_id (users.id)
    if current_user.role == "tutor":
        sessions = (
            db.query(SupportChatSession)
            .filter(SupportChatSession.tutor_id == current_user.id)
            .order_by(SupportChatSession.created_at.desc())
            .all()
        )
        return [s.id for s in sessions]

    # Estudiante: hay que buscar SU fila en students primero
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


# ==========================
# MENSAJES DE UNA SESIÓN
# ==========================


@router.get("/sessions/{session_id}/messages")
def get_support_messages(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = (
        db.query(SupportChatSession).filter(SupportChatSession.id == session_id).first()
    )

    if not session:
        raise HTTPException(404, "Sesión no encontrada")

    # permisos
    if current_user.role == "tutor" and session.tutor_id != current_user.id:
        raise HTTPException(403, "No autorizado")

    if current_user.role == "student":
        student = db.query(Student).filter(Student.user_id == current_user.id).first()
        if not student or session.student_id != student.id:
            raise HTTPException(403, "No autorizado")

    return [
        {
            "id": m.id,
            "sender": m.sender,
            "content": m.content,
            "created_at": m.created_at,
        }
        for m in session.messages
    ]


# ==========================
# ENVIAR MENSAJE
# ==========================


class MessageData(BaseModel):
    content: str
    session_id: int | None = None
    receiver_id: int | None = None


@router.post("/messages")
def send_support_message(
    data: MessageData,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    content = data.content
    session_id = data.session_id
    receiver_id = data.receiver_id

    # Crear sesión si no existe
    if not session_id:
        if not receiver_id:
            raise HTTPException(400, "receiver_id requerido para crear sesión")

        # Si soy tutor -> receiver_id es student_id (tabla students)
        # Si soy student -> receiver_id es tutor_id (tabla users)
        if current_user.role == "tutor":
            session = SupportChatSession(
                tutor_id=current_user.id,
                student_id=receiver_id,
            )
        else:  # student
            # buscar mi fila en students
            student = (
                db.query(Student).filter(Student.user_id == current_user.id).first()
            )
            if not student:
                raise HTTPException(404, "Estudiante no encontrado")

            session = SupportChatSession(
                tutor_id=receiver_id,
                student_id=student.id,
            )

        db.add(session)
        db.commit()
        db.refresh(session)

    else:
        session = (
            db.query(SupportChatSession)
            .filter(SupportChatSession.id == session_id)
            .first()
        )
        if not session:
            raise HTTPException(404, "Sesión no encontrada")

    # Guardar mensaje
    msg = SupportChatMessage(
        session_id=session.id,
        sender=current_user.role,  # "tutor" o "student"
        content=content,
    )

    db.add(msg)
    db.commit()
    db.refresh(msg)

    return {
        "session_id": session.id,
        "message": {
            "id": msg.id,
            "sender": msg.sender,
            "content": msg.content,
            "created_at": msg.created_at,
        },
    }
