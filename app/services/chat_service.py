import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Modelo correcto para API legacy
model = genai.GenerativeModel("models/gemini-2.5-flash")

async def generate_chat_response(message: str) -> str:
    prompt = f"""
Eres un asistente académico experto que ayuda a estudiantes y tutores.
Usuario dice: {message}
Responde de forma amable, clara y educativa.
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Ocurrió un error al generar respuesta: {e}"
