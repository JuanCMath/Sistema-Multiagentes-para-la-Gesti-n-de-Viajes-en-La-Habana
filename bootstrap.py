from google.generativeai import configure
from Agent.base import settings

if not settings.GOOGLE_API_KEY:
    raise RuntimeError("Falta GOOGLE_API_KEY en configuración.")

configure(api_key=settings.GOOGLE_API_KEY)

print("Configuración de Google Generative AI completada.")