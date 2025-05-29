from google.adk.agents import Agent
from core.config import settings
from agents.tools.weather_agent_tools import get_weather

weather_agent = Agent(
    name="weather_agent_v1",
    model=settings.MODEL_GEMINI_2_0_FLASH, 
    description="Provides weather information for specific cities.",
    instruction="You are a helpful weather assistant. "
                "When the user asks for the weather in a specific city, "
                "use the 'get_weather' tool to find the information. pass the city name to the tool. "
                "If the tool returns an error, inform the user politely. "
                "If the tool is successful, present the weather report clearly."
                "U can only check the weather in Cuba. if the user ask for another country, Say that u can only check the weather in Cuba."
                "if the user ask for -Habana- or -La Habana- pass to the function -Habana-"
                "U only give asnwer in Spanish.",
    tools= [get_weather], # Pass the function directly
    output_key=  "weather_report"
)
