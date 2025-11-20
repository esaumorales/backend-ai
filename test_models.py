import google.generativeai as genai
import os
from dotenv import load_dotenv

# 🟦 Cargar variables del .env
load_dotenv()

# 🟩 Configurar API KEY
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

models = genai.list_models()

for m in models:
    print("MODEL:", m.name)
    print("SUPPORTED:", m.supported_generation_methods)
    print("-" * 40)
