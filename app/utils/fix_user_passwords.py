from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user_model import User
from app.services.hashing import hash_password, verify_password
from passlib.exc import UnknownHashError

DEFAULT_PASSWORD = "123"   # puedes cambiarlo si quieres

def fix_passwords():
    db: Session = SessionLocal()
    try:
        print("🔍 Buscando usuarios con hashes inválidos...")

        users = db.query(User).all()
        fixed_count = 0

        for user in users:
            try:
                # Intentar verificar con un password falso
                verify_password("test", user.password_hash)
            except UnknownHashError:
                # Hash inválido → repararlo
                print(f"⚠ Usuario con hash inválido detectado: {user.email}")
                user.password_hash = hash_password(DEFAULT_PASSWORD)
                fixed_count += 1

        db.commit()
        print(f"🎉 Corrección completa. {fixed_count} usuarios reparados.")

    except Exception as e:
        print("❌ Error durante la corrección:", e)
        db.rollback()

    finally:
        db.close()


if __name__ == "__main__":
    fix_passwords()
