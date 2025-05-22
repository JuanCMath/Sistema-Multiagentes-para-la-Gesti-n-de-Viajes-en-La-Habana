from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker
from pydantic import ValidationError, BaseModel
from google.adk.agents import Agent
from pydantic_settings import BaseSettings
from typing import Optional
from sqlalchemy import DateTime, Text
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, inspect
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///data/viajes.db")
Session = sessionmaker(bind=engine)

def init_db():
    inspector = inspect(engine)
    tablas_esperadas = {"viajes"}
    tablas_existentes = set(inspector.get_table_names())
    if not tablas_esperadas.issubset(tablas_existentes):
        print("Inicializando base de datos...")
        Base.metadata.create_all(engine)
    else:
        print("Base de datos ya inicializada.")


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
engine = create_engine("sqlite:///data/viajes.db")
Session = sessionmaker(bind=engine)


class QueryRequest(BaseModel):
    query: str
    

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
        
        
class Conversacion(Base):
    __tablename__ = "conversaciones"
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_id = Column(String, nullable=False)
    pregunta = Column(Text, nullable=False)
    respuesta = Column(Text, nullable=False)
    
class ViajeUpdate(BaseModel):
    destino: Optional[str] = None
    fecha: Optional[str] = None
    descripcion: Optional[str] = None
    
    
init_db()