from pydantic_settings import BaseSettings
from pydantic import ValidationError

class Settings(BaseSettings):
    GOOGLE_API_KEY: str
    WEATHER_API_KEY: str
    GOOGLE_GENAI_USE_VERTEXAI: bool = False
    WEATHER_API_URL: str = "http://api.weatherapi.com/v1/current.json"
    MODEL_GEMINI_2_0_FLASH: str = "gemini-2.0-flash"
    APP_NAME : str = "viajes_habana_app"
    ADMIN_USER_ID : str = "admin"

    class Config:
        env_file = ".env"

try:
    settings = Settings()
except ValidationError as e:
    print("Detalles del error de validación en Settings:")
    print(e.json())
    raise