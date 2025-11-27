from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

resp = client.models.generate_content(
    model="models/gemini-2.5-flash",
    contents="Hola IA"
)

print(resp.text)
