import os
import uuid
import logging
import warnings
from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional

from google.adk.memory import InMemoryMemoryService
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

from Agent.Agent import orchestrator_agent
from Agent.base import settings, Session, Viaje, ViajeCreate, ViajeRead, Conversacion, QueryRequest, ViajeUpdate

# Ignore all warnings
warnings.filterwarnings("ignore")

# Configura logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sistema Multiagente ADK")

os.environ['GOOGLE_API_KEY'] = settings.GOOGLE_API_KEY

# Servicio de sesiones en memoria
session_service = InMemorySessionService()
memory_service = InMemoryMemoryService()


session_service.create_session(
    app_name="viajes_habana_app",
    user_id="admin",
    session_id="default_session"
)

APP_NAME = "viajes_habana_app"
ADMIN_USER_ID = "admin"

# Inicializa runner del orquestador
runner_orchestrator = Runner(agent=orchestrator_agent, app_name=APP_NAME, session_service=session_service, memory_service=memory_service)


# Endpoint para inicializar una nueva sesión
@app.post("/init_session")
def init_session():
    session_id = str(uuid.uuid4())
    session_service.create_session(app_name=APP_NAME, user_id=ADMIN_USER_ID, session_id=session_id)
    return {"session_id": session_id}


# Endpoint principal del agente
@app.post("/agent/orquestator")
async def call_orquestator_async(req: QueryRequest, session_id: Optional[str] = Query(default=None)):
    try:
        if session_id is None:
            session_id = "default_session"
            # Asegurarse de usar await solo si create_session es async (en este caso lo es)
            session_service.create_session(app_name=APP_NAME, user_id=ADMIN_USER_ID, session_id=session_id)

        logger.info(f"Ejecutando consulta al agente en la sesion: {session_id}")

        content = types.Content(role="user", parts=[types.Part(text=req.query)])

        final_response_text = None

        async for event in runner_orchestrator.run_async(
            user_id=ADMIN_USER_ID,
            session_id=session_id,
            new_message=content
        ):
            if event.is_final_response() and event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
                break

        if final_response_text is None:
            raise ValueError("No se recibio respuesta final del agente.")

        # Obtener la sesión (NO usar await aquí, porque get_session no es async)
        completed_session = session_service.get_session(
            app_name=APP_NAME,
            user_id=ADMIN_USER_ID,
            session_id=session_id
        )
        # Guardar en memoria (esta sí es async)
        await memory_service.add_session_to_memory(completed_session)

        return {"response": final_response_text, "session_id": session_id}

    except Exception as e:
        logger.exception("Error procesando consulta al agente")
        raise HTTPException(status_code=500, detail=str(e))



# CRUD para Viajes
@app.post("/viajes/", response_model=ViajeRead)
def crear_viaje(viaje: ViajeCreate):
    with Session() as session:
        nuevo_viaje = Viaje(**viaje.dict())
        session.add(nuevo_viaje)
        session.commit()
        session.refresh(nuevo_viaje)
        return nuevo_viaje

@app.get("/viajes/", response_model=List[ViajeRead])
def listar_viajes():
    with Session() as session:
        viajes = session.query(Viaje).all()
        return viajes

@app.get("/viajes/{viaje_id}", response_model=ViajeRead)
def obtener_viaje(viaje_id: int):
    with Session() as session:
        viaje = session.query(Viaje).filter_by(id=viaje_id).first()
        if not viaje:
            raise HTTPException(status_code=404, detail="Viaje no encontrado")
        return viaje

@app.delete("/viajes/{viaje_id}")
def eliminar_viaje(viaje_id: int):
    with Session() as session:
        viaje = session.query(Viaje).filter_by(id=viaje_id).first()
        if not viaje:
            raise HTTPException(status_code=404, detail="Viaje no encontrado")
        session.delete(viaje)
        session.commit()
        return {"status": "success", "message": "Viaje eliminado exitosamente."}


@app.put("/viajes/{viaje_id}", response_model=ViajeRead)
def actualizar_viaje(viaje_id: int, viaje_data: ViajeUpdate):
    with Session() as session:
        viaje = session.query(Viaje).filter_by(id=viaje_id).first()
        if not viaje:
            raise HTTPException(status_code=404, detail="Viaje no encontrado")

        for field, value in viaje_data.dict(exclude_unset=True).items():
            setattr(viaje, field, value)

        session.commit()
        session.refresh(viaje)
        return viaje
