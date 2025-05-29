from core.session import memory_service
from agents.weather_agent import weather_agent

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

async def load_memory():
    """Load the memory of the agent

    Args:
        none
    Returns:
        str : Memory loaded
    """
    # Cargar la memoria del agente
    memory = memory_service._load_memory()
    return {"memoria": memory}