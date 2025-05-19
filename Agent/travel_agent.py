from google.adk.agents import Agent
from .base import settings, session, Viaje, Session

# Define the functions for managing trips
def new_trip(destino: str, fecha: str, descripcion: str = None) -> dict:
    """Creates a new trip and saves it to the database.
    Args:
        destino (str): The destination of the trip.
        fecha (str): The date of the trip.
        descripcion (str, optional): A description of the trip.
    Returns:
        dict: A dictionary containing the status and a message.
              If successful, includes the ID of the created trip.
    """
    try:
        with Session() as session:
            nuevo_viaje = Viaje(destino=destino, fecha=fecha, descripcion=descripcion)
            session.add(nuevo_viaje)
            session.commit()
            return {"status": "success", "message": "Viaje creado exitosamente.", "id": nuevo_viaje.id}
    except Exception as e:
        print(f"Error al crear un viaje: {e}")
        return {"status": "error", "message": str(e)}

def delete_trip(viaje_id: int) -> dict:
    """Deletes a trip from the database.
    
    Args:
        viaje_id (int): The ID of the trip to be deleted.
        
    Returns:
        dict: A dictionary containing the status and a message.
              If the trip is found and deleted, includes a success message.
              If not found, includes an error message.
    """
    try:
        with Session() as session:
            viaje = session.query(Viaje).filter_by(id=viaje_id).first()
            if viaje:
                session.delete(viaje)
                session.commit()
                return {"status": "success", "message": "Viaje eliminado exitosamente."}
            else:
                return {"status": "error", "message": "Viaje no encontrado."}
    except Exception as e:
        print(f"Error al eliminar el viaje: {e}")
        return {"status": "error", "message": str(e)}

def check_trips() -> dict:
    """Retrieves all trips from the database.
    
    Returns:
        dict: A dictionary containing the status and a list of trips.
              Each trip includes its ID, destination, date, and description.
    """
    try:
        with Session() as session:
            viajes = session.query(Viaje).all()
            return {
                "status": "success",
                "viajes": [
                    {"id": viaje.id, "destino": viaje.destino, "fecha": viaje.fecha, "descripcion": viaje.descripcion}
                    for viaje in viajes
                ],
            }
    except Exception as e:
        print(f"Error al verificar viajes: {e}")
        return {"status": "error", "message": str(e)}

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
                "To use the tool - new_trip - pass the destination, date, and description (optional)."
                "To use the tool - delete_trip - pass the ID of the trip to be deleted."
                "If the User doesnt give any of the parameters needed to create a trip, inform him that he needs to give the destination, date and description (optional).",
    tools=[new_trip, delete_trip, check_trips],
)