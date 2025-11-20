from app.core.database import engine, Base

# IMPORTANTE: importar los modelos DESDE __init__
import app.models

print("🧹 Eliminando tablas existentes...")
with engine.connect() as conn:
    conn.exec_driver_sql("SET FOREIGN_KEY_CHECKS = 0;")
    conn.exec_driver_sql("DROP TABLE IF EXISTS predictions;")
    conn.exec_driver_sql("DROP TABLE IF EXISTS students;")
    conn.exec_driver_sql("DROP TABLE IF EXISTS users;")
    conn.exec_driver_sql("SET FOREIGN_KEY_CHECKS = 1;")

print("📌 Creando tablas...")
Base.metadata.create_all(bind=engine)

print("🎉 Tablas creadas correctamente.")
