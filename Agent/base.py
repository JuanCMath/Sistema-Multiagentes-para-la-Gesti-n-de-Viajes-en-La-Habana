from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker

from google.adk.agents import Agent
from pydantic_settings import BaseSettings 


class Settings(BaseSettings):
    GOOGLE_API_KEY: str 
    OPENAI_API_KEY: str
    WEATHER_API_KEY: str
    GOOGLE_GENAI_USE_VERTEXAI: bool = False
    WEATHER_API_URL: str 
    MODEL_GEMINI_2_0_FLASH: str
    MODEL_GPT_4O: str

    class Config:
        env_file = ".env"
        
settings = Settings()

# SQLAlchemy setup
Base = declarative_base()
engine = create_engine("sqlite:///viajes.db")
Session = sessionmaker(bind=engine)
session = Session()

class Viaje(Base):
    __tablename__ = "viajes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    destino = Column(String, nullable=False)
    fecha = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
