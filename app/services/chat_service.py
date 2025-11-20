import os
import google.generativeai as genai

# Configurar API Key desde env
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Cargar el modelo Gemini más estable
model = genai.GenerativeModel("gemini-pro")


async def generate_chat_response(message: str) -> str:
    """
    Genera una respuesta usando Gemini (Google AI).
    """

    prompt = f"""
Eres un asistente académico experto que ayuda a estudiantes y tutores.
Siempre brindas explicaciones claras, consejos útiles y sugerencias específicas
sobre hábitos de estudio, rendimiento académico, estrés, motivación y aprendizaje.

Usuario dice:
{message}

Responde de forma amable, clara y educativa.
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Ocurrió un error al generar respuesta: {e}"
