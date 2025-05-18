from google.adk import Agent
from .base import settings, Base, session, Viaje
from .travel_agent import travel_agent
from .weather_agent import weather_agent
import logging

logging.basicConfig(level=logging.INFO)


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

print(f"Orchestrator Agent '{orchestrator_agent.name}' created using model '{settings.MODEL_GPT_4O}'.")


if __name__ == "__main__":
    # Este archivo será el punto de entrada para adk web
    # Ejemplo: Runner.run(orchestrator_agent)
    from google.adk.runners import Runner
    Runner.run(orchestrator_agent)

