from fastapi.middleware.cors import CORSMiddleware


def configure_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "https://frontend-ai-sigma.vercel.app",
            "*",  # si quieres permitir todo durante desarrollo
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
