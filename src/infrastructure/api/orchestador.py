import os
from fastapi import FastAPI, HTTPException
from typing import List, Optional
from sqlmodel import SQLModel
from weather_client import WeatherAPIAgent
from database_agent import DatabaseAgent, Viaje

app = FastAPI()

# Instancias de los agentes
weather_agent = WeatherAPIAgent(api_key=os.getenv("WEATHER_API_KEY"))
db_agent = DatabaseAgent()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(db_agent.engine)

@app.get("/clima/habana")
def consultar_clima_habana():
    clima = weather_agent.get_weather("La Habana", country_code="CU")
    if "error" in clima:
        raise HTTPException(status_code=502, detail=clima["error"])
    return clima

@app.get("/recomendacion-viaje/habana")
def recomendar_viaje_habana():
    clima = weather_agent.get_weather("La Habana", country_code="CU")
    if "error" in clima:
        raise HTTPException(status_code=502, detail=clima["error"])
    # no recomienda viajar si llueve
    condicion = clima.get("condicion", "").lower()
    if "lluvia" in condicion or "tormenta" in condicion:
        return {
            "recomendacion": "No es recomendable viajar en La Habana ahora.",
            "motivo": f"Condición climática actual: {clima['condicion']}"
        }
    else:
        return {
            "recomendacion": "Es buen momento para viajar a La Habana.",
            "motivo": f"Condición climática actual: {clima['condicion']}"
        }

@app.post("/viajes/", response_model=Viaje)
def crear_viaje(viaje: Viaje):
    return db_agent.crear_viaje(
        origen=viaje.origen,
        destino=viaje.destino,
        fecha=viaje.fecha,
        pasajero=viaje.pasajero
    )

@app.get("/viajes/", response_model=List[Viaje])
def listar_viajes(
    origen: Optional[str] = None,
    destino: Optional[str] = None
):
    return db_agent.consultar_viajes(origen=origen, destino=destino)

@app.delete("/viajes/{viaje_id}", response_model=dict)
def eliminar_viaje(viaje_id: int):
    exito = db_agent.eliminar_viaje(viaje_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Viaje no encontrado")
    return {"eliminado": True}