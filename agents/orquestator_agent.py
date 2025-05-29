from google.adk import Agent
from core.config import settings
from .travel_agent import travel_agent
from .weather_agent import weather_agent
from agents.tools.orquestator_tools import recomend_trip, load_memory

# Create an Orchestrator Agent
orchestrator_agent = Agent(
    name="orchestrator_agent_v1",
    model=settings.MODEL_GEMINI_2_0_FLASH,
    description="Orchestrates multiple agents to provide comprehensive assistance.",
    instruction="You are an orchestrator agent. Delegate tasks to specialized agents as needed. "
                "Use the tool load_memory to check if the information that the user is asking for is in the past conversations. "
                "You can use the 'weather_agent' for weather-related queries; it receives a country of Cuba to check the weather. "
                "You can use the 'travel_agent' for managing trips within 'La Habana'."
                "Before u create a trip, use ur tool -recomend_trip- and give the returned information from tool to the user"
                "Answer the user's question. Use the 'load_memory' tool if the answer might be in past conversations."
                "U only Give Answer in Spanish.",
    tools=[recomend_trip, load_memory],
    sub_agents=[weather_agent, travel_agent],
)