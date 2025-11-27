# app/utils/create_chat_tables.py

from app.core.database import Base, engine
from app.models import (
    user_model,
    student_model,
    prediction_model,
    chat_model,  # 👈 importante
)


def create_chat_tables():
    print("🛠 Creando tablas de chat...")

    # Solo crea las tablas que no existan
    Base.metadata.create_all(bind=engine)

    print("✅ Tablas creadas correctamente.")


if __name__ == "__main__":
    create_chat_tables()
