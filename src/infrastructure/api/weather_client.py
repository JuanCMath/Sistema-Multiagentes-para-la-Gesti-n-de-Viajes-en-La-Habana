import requests
import os
from dotenv import load_dotenv

load_dotenv()

class WeatherAPIAgent:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "http://api.weatherapi.com/v1/current.json"

    def get_weather(self, city, country_code=""):
        location = city
        if country_code:
            location += f",{country_code}"
        params = {
            "key": self.api_key,
            "q": location,
            "lang": "es"  # Para respuesta en español
        }
        response = requests.get(self.api_url, params=params)
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

if __name__ == "__main__":
    agent = WeatherAPIAgent(api_key=os.getenv("WEATHER_API_KEY"))
    ciudad = "La Habana"
    resultado = agent.get_weather(ciudad, country_code="CU")  # En Caso de querer otro pais cambiar el codigo, por ahora solo es Cuba
    print(resultado)