from app.core.database import Base, engine
from app.models import (
    user_model,
    support_chat_model,
)


def create_support_tables():
    print("🛠 Creando tablas de chat humano...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas correctamente.")


if __name__ == "__main__":
    create_support_tables()
