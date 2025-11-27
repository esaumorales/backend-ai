from datetime import datetime, timedelta
from jose import jwt, JWTError
import os

# Obtener clave secreta de entorno, y si no existe, usar una por defecto
SECRET_KEY = os.getenv("SECRET_KEY", "SUPER_SECRET_KEY_CAMBIA_ESTA_CLAVE")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 horas


# ==========================================================
# 🔐 CREAR TOKEN (LOGIN)
# ==========================================================
def create_access_token(data: dict):
    """Genera un JWT con expiración automática."""
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = expire

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


# ==========================================================
# 🔐 DECODIFICAR TOKEN (get_current_user)
# ==========================================================
def decode_access_token(token: str) -> dict:
    """
    Decodifica el JWT y devuelve su payload.
    Lanza un error si el token es inválido o expiró.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except JWTError:
        raise ValueError("Token inválido o expirado")
