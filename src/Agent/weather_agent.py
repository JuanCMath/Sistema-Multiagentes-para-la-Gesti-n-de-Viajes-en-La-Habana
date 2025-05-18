import os
import asyncio
import requests
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm # For multi-model support
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types # For creating message Content/Parts
from pydantic_settings import BaseSettings 
import warnings

# Ignore all warnings
warnings.filterwarnings("ignore")

import logging
from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker
logging.basicConfig(level=logging.ERROR)


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
AGENT_MODEL = settings.MODEL_GEMINI_2_0_FLASH


# SQLAlchemy setup
Base = declarative_base()
engine = create_engine("sqlite:///viajes.db")
Session = sessionmaker(bind=engine)
session = Session()

# Define the Viaje model
class Viaje(Base):
    __tablename__ = "viajes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    destino = Column(String, nullable=False)
    fecha = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)

# Create the table if it doesn't exist
Base.metadata.create_all(engine)

# Define the functions for managing trips
def crear_viaje(destino: str, fecha: str, descripcion: str = None) -> dict:
    """Creates a new trip and saves it to the database.
    Args:
        destino (str): The destination of the trip.
        fecha (str): The date of the trip.
        descripcion (str, optional): A description of the trip.
    Returns:
        dict: A dictionary containing the status and a message.
              If successful, includes the ID of the created trip.
    """
    nuevo_viaje = Viaje(destino=destino, fecha=fecha, descripcion=descripcion)
    session.add(nuevo_viaje)
    session.commit()
    return {"status": "success", "message": "Viaje creado exitosamente.", "viaje_id": nuevo_viaje.id}

def eliminar_viaje(viaje_id: int) -> dict:
    """Deletes a trip from the database.
    
    Args:
        viaje_id (int): The ID of the trip to be deleted.
        
    Returns:
        dict: A dictionary containing the status and a message.
              If the trip is found and deleted, includes a success message.
              If not found, includes an error message.
    """
    viaje = session.query(Viaje).filter_by(id=viaje_id).first()
    if viaje:
        session.delete(viaje)
        session.commit()
        return {"status": "success", "message": "Viaje eliminado exitosamente."}
    else:
        return {"status": "error", "message": "Viaje no encontrado."}

def verificar_viajes() -> dict:
    """Retrieves all trips from the database.
    
    Returns:
        dict: A dictionary containing the status and a list of trips.
              Each trip includes its ID, destination, date, and description.
    """
    viajes = session.query(Viaje).all()
    return {
        "status": "success",
        "viajes": [
            {"id": viaje.id, "destino": viaje.destino, "fecha": viaje.fecha, "descripcion": viaje.descripcion}
            for viaje in viajes
        ],
    }

# Create the travel_agent
travel_agent = Agent(
    name="travel_agent_v1",
    model=AGENT_MODEL,
    description="Manages trips within 'La Habana'. Can create, delete, and list trips.",
    instruction="You are a travel assistant for managing trips within 'La Habana'. "
                "Use the provided tools to create, delete, or list trips. "
                "Ensure all operations are performed accurately and provide clear feedback to the user.",
    tools=[crear_viaje, eliminar_viaje, verificar_viajes],
)

print(f"Agent '{travel_agent.name}' created using model '{AGENT_MODEL}'.")



# @title Define the get_weather Tool
def get_weather(city: str, country_code='CU') -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city (e.g., "New York", "London", "Tokyo").

    Returns:
        dict: A dictionary containing the weather information.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes a 'report' key with weather details.
              If 'error', includes an 'error_message' key.
    """
    print(f"--- Tool: get_weather called for city: {city} ---") # Log tool execution
    location = city.lower().replace(" ", "") # Basic normalization

    if country_code:
            location += f",{country_code}"
    params = {
        "key": settings.WEATHER_API_KEY,
        "q": location,
        "lang": "es"  # Para respuesta en español
    }
    response = requests.get(settings.WEATHER_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        weather = {
            "ciudad": data["location"]["name"],
            "pais": data["location"]["country"],
            "temperatura_C": data["current"]["temp_c"],
            "condicion": data["current"]["condition"]["text"],
            "humedad": data["current"]["humidity"],
            "viento_kph": data["current"]["wind_kph"]
        }
        return weather
    else:
        return {"error": f"Error consultando el clima: {response.status_code} - {response.text}"}
    

weather_agent = Agent(
    name="weather_agent_v1",
    model=AGENT_MODEL, 
    description="Provides weather information for specific cities.",
    instruction="You are a helpful weather assistant. "
                "When the user asks for the weather in a specific city, "
                "use the 'get_weather' tool to find the information. "
                "If the tool returns an error, inform the user politely. "
                "If the tool is successful, present the weather report clearly.",
    tools=[get_weather], # Pass the function directly
)

print(f"Agent '{weather_agent.name}' created using model '{AGENT_MODEL}'.")




# Create an Orchestrator Agent
orchestrator_agent = Agent(
    name="orchestrator_agent_v1",
    model=settings.MODEL_GPT_4O,
    description="Orchestrates multiple agents to provide comprehensive assistance.",
    instruction="You are an orchestrator agent. Delegate tasks to specialized agents as needed. "
                "You can use the 'weather_agent' for weather-related queries, he reciev a country of Cuba to check the weather. "
                "You can use the 'travel_agent' for managing trips within 'La Habana' ",
    tools=[weather_agent, travel_agent],
)

print(f"Orchestrator Agent '{orchestrator_agent.name}' created using model '{AGENT_MODEL}'.")
