from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI


def configure_cors(app: FastAPI) -> None:
    """Configura CORS para permitir al frontend (React) consumir la API."""
    origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
