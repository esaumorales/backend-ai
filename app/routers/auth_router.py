from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.user_model import User
from app.models.student_model import Student
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse
from app.services.hashing import hash_password, verify_password
from app.core.security import create_access_token, decode_access_token


# 🔥 Prefijo correcto
router = APIRouter(tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# ----------------------------
# DB
# ----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ----------------------------
# REGISTER
# ----------------------------
@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):

    # Validar email duplicado
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email ya registrado")

    # Crear usuario en tabla USERS
    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=hash_password(user.password),
        role=user.role,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Si es estudiante → crear también en la tabla STUDENTS
    if new_user.role == "student":
        student = Student(
            nombre=new_user.name,
            user_id=new_user.id,  # 👈 YA EXISTE ESTE CAMPO EN TU MODELO
        )
        db.add(student)
        db.commit()

    return new_user


# ----------------------------
# LOGIN
# ----------------------------
@router.post("/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):

    # Buscar usuario
    user = db.query(User).filter(User.email == credentials.email).first()

    # Validar
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

    # Generar JWT
    token = create_access_token({"id": user.id, "role": user.role})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
        },
    }


# ----------------------------
# GET CURRENT USER
# ----------------------------
@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(lambda: get_current_user())):
    return current_user


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:

    try:
        payload = decode_access_token(token)
        user_id = payload.get("id")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.id == int(user_id)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
        )

    return user
