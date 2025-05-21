import requests
from google.adk.agents import Agent
from .base import settings

# @title Define the get_weather Tool
def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city (e.g., "New York", "London", "Tokyo")

    Returns:
        dict: A dictionary containing the weather information.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes a 'report' key with weather details.
              If 'error', includes an 'error_message' key.
    """

    location = city.lower().replace(" ", "") # Basic normalization

    country_code = "CU"  # Cuba's country code
    
    location += f",{country_code}"
    params = {
        "key": settings.WEATHER_API_KEY,
        "q": location,
        "lang": "en"  # Para respuesta en ingles
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
