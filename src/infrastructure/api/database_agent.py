from typing import Optional, List
from sqlmodel import SQLModel, Field, create_engine, Session, select

class Viaje(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    origen: str
    destino: str
    fecha: str
    pasajero: str

# Agente
class DatabaseAgent:
    def __init__(self, db_url: str = "sqlite:///viajes.db"):
        self.engine = create_engine(db_url, echo=False)
        SQLModel.metadata.create_all(self.engine)

    def crear_viaje(self, origen: str, destino: str, fecha: str, pasajero: str) -> Viaje:
        viaje = Viaje(origen=origen, destino=destino, fecha=fecha, pasajero=pasajero)
        with Session(self.engine) as session:
            session.add(viaje)
            session.commit()
            session.refresh(viaje)
            return viaje

    def eliminar_viaje(self, viaje_id: int) -> bool:
        with Session(self.engine) as session:
            viaje = session.get(Viaje, viaje_id)
            if viaje:
                session.delete(viaje)
                session.commit()
                return True
            return False

    def consultar_viajes(self, origen: Optional[str]=None, destino: Optional[str]=None) -> List[Viaje]:
        with Session(self.engine) as session:
            query = select(Viaje)
            if origen:
                query = query.where(Viaje.origen == origen)
            if destino:
                query = query.where(Viaje.destino == destino)
            return session.exec(query).all()

if __name__ == "__main__":
    db_agent = DatabaseAgent()

    # Crear un viaje
    nuevo_viaje = db_agent.crear_viaje(
        origen="La Habana",
        destino="Varadero",
        fecha="2025-05-18",
        pasajero="Juan Pérez"
    )
    print("Viaje creado:", nuevo_viaje)

    # Consultar todos los viajes
    viajes = db_agent.consultar_viajes()
    print("Todos los viajes:", viajes)

    # Eliminar un viaje
    exito = db_agent.eliminar_viaje(nuevo_viaje.id)
    print("Viaje eliminado:", exito)