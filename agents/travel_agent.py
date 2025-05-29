from google.adk.agents import Agent
from core.config import settings
from agents.tools.travel_agent_tools import new_trip, delete_trip, check_trips

# Create the travel_agent
travel_agent = Agent(
    name="travel_agent_v1",
    model=settings.MODEL_GEMINI_2_0_FLASH,
    description="Manages trips within 'La Habana'. Can create, delete, and list trips.",
    instruction="You are a travel assistant for managing trips within 'La Habana'. "
                "Use the provided tools to create, delete, or list trips. "
                "Ensure all operations are performed accurately and provide clear feedback to the user."
                "If the user asks for a trip outside of 'La Habana', inform them that you can only assist with trips within 'La Habana'."
                "Use -new_trip- to create a trip, -delete_trip- to remove a trip, and -check_trips- to list all trips."
                "To use the tool - new_trip - pass the destination, date, and description (not needed, optional for the user, if the user doesnt give pass null to the tool)."
                "To use the tool - delete_trip - pass the ID of the trip to be deleted."
                "If the User doesnt give any of the parameters needed to create a trip, inform him that he needs to give the destination, date and description (optional)."
                "U only Give Asnwers in Spanish.",
    tools=[new_trip, delete_trip, check_trips],
)