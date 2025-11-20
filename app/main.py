from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from app.core.config import configure_cors
from app.models.student_data import StudentData, PredictionResponse
from app.services.predictor import predict_from_payload, ModelNotLoadedError


app = FastAPI(
    title="API Predicción de Rendimiento Académico",
    description="Servicio REST sobre el modelo MLP entrenado para predecir rendimiento estudiantil.",
    version="1.0.0",
)

# CORS para permitir llamadas desde tu frontend
configure_cors(app)


@app.get("/", tags=["Health"])
def root():
    return {"message": "API de IA para predicción de rendimiento académico funcionando ✅"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse, tags=["Predicción"])
def predict(student: StudentData):
    """
    Endpoint principal.

    Recibe las variables del estudiante y devuelve:
    - predicted_class: Insuficiente / Satisfactorio / Excelente
    - probabilities: dict con probabilidad por clase
    """
    # Compatibilidad Pydantic v1/v2
    if hasattr(student, "model_dump"):
        payload = student.model_dump()
    else:
        payload = student.dict()

    try:
        predicted_class, probabilities = predict_from_payload(payload)
    except ModelNotLoadedError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al predecir: {e}")

    return PredictionResponse(
        predicted_class=predicted_class,
        probabilities=probabilities,
    )
