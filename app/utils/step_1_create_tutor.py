# app/utils/step_1_create_tutor.py

from sqlalchemy.orm import Session
from app.core.database import SessionLocal

# ⚠ IMPORTANTE – obliga a SQLAlchemy a registrar modelos
from app.models import user_model, student_model, prediction_model

from app.models.user_model import User
from app.services.hashing import hash_password


TUTOR_EMAIL = "tutor_principal@gmail.com"
TUTOR_PASSWORD = "123"
TUTOR_NAME = "Tutor Principal"


def create_tutor():
    db: Session = SessionLocal()

    tutor = db.query(User).filter(User.email == TUTOR_EMAIL).first()
    if tutor:
        print(f"✔ Tutor ya existe con ID={tutor.id}")
        return

    print("➕ Creando tutor principal...")
    new_tutor = User(
        name=TUTOR_NAME,
        email=TUTOR_EMAIL,
        password_hash=hash_password(TUTOR_PASSWORD),
        role="tutor"
    )

    db.add(new_tutor)
    db.commit()

    print(f"✔ Tutor creado con ID={new_tutor.id}")
    db.close()


if __name__ == "__main__":
    create_tutor()
