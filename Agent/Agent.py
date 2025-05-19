from google.adk import Agent
from .base import settings
from .travel_agent import travel_agent
from .weather_agent import weather_agent

# Create an Orchestrator Agent
orchestrator_agent = Agent(
    name="orchestrator_agent_v1",
    model=settings.MODEL_GEMINI_2_0_FLASH,
    description="Orchestrates multiple agents to provide comprehensive assistance.",
    instruction="You are an orchestrator agent. Delegate tasks to specialized agents as needed. "
                "You can use the 'weather_agent' for weather-related queries; it receives a country of Cuba to check the weather. "
                "You can use the 'travel_agent' for managing trips within 'La Habana'.",
    sub_agents=[weather_agent, travel_agent],
)