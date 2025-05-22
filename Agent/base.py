from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker
from pydantic import ValidationError, BaseModel
from google.adk.agents import Agent
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    GOOGLE_API_KEY: str 
    OPENAI_API_KEY: str
    WEATHER_API_KEY: str
    GOOGLE_GENAI_USE_VERTEXAI: bool = False
    WEATHER_API_URL: str 
    MODEL_GEMINI_2_0_FLASH: str

    class Config:
        env_file = ".env"

try:
    settings = Settings()
except ValidationError as e:
    print("Detalles del error de validación en Settings:")
    print(e.json())
    raise

# SQLAlchemy setup
Base = declarative_base()
engine = create_engine("sqlite:///viajes.db")
Session = sessionmaker(bind=engine)

class Viaje(Base):
    __tablename__ = "viajes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    destino = Column(String, nullable=False)
    fecha = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    
    
class ViajeCreate(BaseModel):
    destino: str
    fecha: str
    descripcion: Optional[str] = None

class ViajeRead(BaseModel):
    id: int
    destino: str
    fecha: str
    descripcion: Optional[str] = None

    class Config:
        orm_mode = True