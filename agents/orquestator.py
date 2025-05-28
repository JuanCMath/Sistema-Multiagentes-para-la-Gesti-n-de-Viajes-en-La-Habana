from google.adk import Agent
from core.config import settings
from .travel_agent import travel_agent
from .weather_agent import weather_agent
from google.adk.tools import load_memory


async def recomend_trip():
    """Recomend (or no) a trip within the Habana Based on the weather conditions

    Args:
        none
    Returns:
        str : Rocomended or no
    """
    # Paso 1: Consultar clima
    reporte_clima = await weather_agent.tools[0]("Habana")
    condicion = reporte_clima.get('condicion', '').lower()
    # Puedes personalizar las condiciones 'malas'
    condiciones_buenas = ['sunny', 'clear', 'partly cloudy', 'mostly sunny']

    # Paso 2: Decidir si recomendar
    if not any(c.lower() in condicion for c in condiciones_buenas):
        return f"No se recomienda viajar en La Habana en el dia de hoy debido a las condiciones climáticas: {condicion}."
    else:
        return f"¡El clima es adecuado! Se recomienda viajar en La Habana"
    
    
# Create an Orchestrator Agent
orchestrator_agent = Agent(
    name="orchestrator_agent_v1",
    model=settings.MODEL_GEMINI_2_0_FLASH,
    description="Orchestrates multiple agents to provide comprehensive assistance.",
    instruction="You are an orchestrator agent. Delegate tasks to specialized agents as needed. "
                "You can use the 'weather_agent' for weather-related queries; it receives a country of Cuba to check the weather. "
                "You can use the 'travel_agent' for managing trips within 'La Habana'."
                "Before u create a trip, use ur tool -recomend_trip- and give the returned information from tool to the user"
                "Answer the user's question. Use the 'load_memory' tool if the answer might be in past conversations."
                "U only Give Answer in Spanish.",
    tools=[recomend_trip, load_memory],
    sub_agents=[weather_agent, travel_agent],
)