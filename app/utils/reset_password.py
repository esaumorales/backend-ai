from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user_model import User
from app.services.hashing import hash_password

EMAIL = "esaur@gmail.com"
NEW_PASSWORD = "123"

def reset_password():
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.email == EMAIL).first()
        if not user:
            print("❌ Usuario no encontrado.")
            return
        
        user.password_hash = hash_password(NEW_PASSWORD)
        db.commit()
        print(f"🎉 Password actualizado correctamente para {EMAIL}")
    
    except Exception as e:
        print("❌ Error:", e)
        db.rollback()
    
    finally:
        db.close()


if __name__ == "__main__":
    reset_password()
