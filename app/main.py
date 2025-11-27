from fastapi import FastAPI
from app.core.config import configure_cors
from app.core.database import Base, engine

# Routers
from app.routers.auth_router import router as auth_router
from app.routers.student_router import router as student_router
from app.routers.tutor_router import router as tutor_router
from app.routers.prediction_router import router as prediction_router
from app.routers.chat_router import router as chat_router
from app.routers.support_router import router as support_router
from app.routers.analytics_router import router as analytics_router

# Crear tablas automáticamente
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Academic Performance API",
    version="1.0.0",
)

configure_cors(app)


@app.get("/")
def root():
    return {"message": "Backend funcionando correctamente"}


# -----------------------------
# 📌 INCLUIR TODOS LOS ROUTERS
# -----------------------------
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(student_router, prefix="/students", tags=["Students"])
app.include_router(tutor_router, prefix="/tutor", tags=["Tutor"])
app.include_router(prediction_router, prefix="/predict", tags=["Prediction"])
app.include_router(chat_router, prefix="/chat", tags=["Chatbot"])
app.include_router(support_router, prefix="/support", tags=["Chat Humano"])
app.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])

# --- LOG DE ENDPOINTS ---
print("\n📌 ENDPOINTS REGISTRADOS:")
for route in app.routes:
    print(f"➡ {route.path} [{','.join(route.methods)}]")
print("--------------------------------------------------\n")
