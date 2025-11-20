from fastapi import FastAPI
from app.core.config import configure_cors
from app.core.database import Base, engine
from app.routers.auth_router import router as auth_router
from app.routers.student_router import router as student_router
from app.routers.tutor_router import router as tutor_router
from app.routers.prediction_router import router as prediction_router

# Crear tablas automáticamente
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Academic Performance API",
    version="1.0.0"
)

configure_cors(app)

@app.get("/")
def root():
    return {"message": "Backend funcionando correctamente"}

# Rutas
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(student_router, prefix="/students", tags=["Students"])
app.include_router(tutor_router, prefix="/tutor", tags=["Tutor"])
app.include_router(prediction_router, prefix="/predict", tags=["Prediction"])
