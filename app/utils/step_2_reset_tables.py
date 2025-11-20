# app/utils/step_2_reset_tables.py

from sqlalchemy import text
from app.core.database import Base, engine

# ⚠ IMPORTANTE – obliga a SQLAlchemy a registrar modelos
from app.models import user_model, student_model, prediction_model


def reset_tables():
    print("🧹 RESET: Eliminando tablas students y predictions...")

    with engine.connect() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
        conn.execute(text("DROP TABLE IF EXISTS predictions;"))
        conn.execute(text("DROP TABLE IF EXISTS students;"))
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))

    print("📌 Recreando tablas...")
    Base.metadata.create_all(bind=engine)
    print("✔ Tablas listas")


if __name__ == "__main__":
    reset_tables()
