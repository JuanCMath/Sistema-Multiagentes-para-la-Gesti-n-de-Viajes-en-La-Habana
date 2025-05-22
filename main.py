import bootstrap

import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

from Agent.Agent import orchestrator_agent
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from Agent.base import settings, Session, Viaje, ViajeCreate, ViajeRead, Conversacion, QueryRequest, ViajeUpdate

import warnings
# Ignore all warnings
warnings.filterwarnings("ignore")

# Configura logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sistema Multiagente ADK")

os.environ['GOOGLE_API_KEY'] = settings.GOOGLE_API_KEY

# Servicio de sesiones en memoria
session_service = InMemorySessionService()


APP_NAME = "viajes_habana_app"
ADMIN_USER_ID = "admin"
ADMIN_SESSION_ID = "admin_session"

# Crear sesión fija de admin
session_service.create_session(
    app_name=APP_NAME,
    user_id=ADMIN_USER_ID,
    session_id=ADMIN_SESSION_ID
)

# Inicializa runner del orquestador
runner_orchestrator = Runner(agent=orchestrator_agent, app_name=APP_NAME, session_service=session_service)

# Modelo para la consulta


# Endpoint principal
@app.post("/agent/orquestator")
async def call_orquestator_async(req: QueryRequest):
    try:
        # Recuperar historial de la sesión/usuario
        with Session() as session:
            historial = (
                session.query(Conversacion)
                .filter_by(user_id=ADMIN_USER_ID)
                .order_by(Conversacion.timestamp.asc())
                .limit(5)
                .all()
            )

        # Crear historial como texto plano
        historial_texto = ""
        for turno in historial:
            historial_texto += f"Usuario: {turno.pregunta}\n"
            historial_texto += f"Agente: {turno.respuesta}\n"

        # Añadir la pregunta actual
        historial_texto += f"Usuario: {req.query}"

        # Crear el contenido válido como types.Content
        content = types.Content(
            role="user",
            parts=[types.Part(text=historial_texto)]
        )

        final_response_text = None
        logger.info("Ejecutando consulta al agente...")

        # Ejecutar el agente con el contexto combinado
        async for event in runner_orchestrator.run_async(
            user_id=ADMIN_USER_ID,
            session_id=ADMIN_SESSION_ID,
            new_message=content
        ):
            
            if event.is_final_response() and event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
                break

        if final_response_text is None:
            raise ValueError("No se recibió respuesta final del agente.")

        # Guardar conversación en la base de datos
        with Session() as session:
            nueva_conv = Conversacion(
                user_id=ADMIN_USER_ID,
                pregunta=req.query,
                respuesta=final_response_text
            )
            session.add(nueva_conv)
            session.commit()

        return {"response": final_response_text}

    except Exception as e:
        logger.exception("Error procesando consulta al agente")
        raise HTTPException(status_code=500, detail=str(e))


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


@app.delete("/conversaciones/")
def eliminar_todas_conversaciones():
    try:
        with Session() as session:
            deleted_count = session.query(Conversacion).delete()
            session.commit()
            return {
                "status": "success",
                "message": f"Se eliminaron {deleted_count} conversaciones del historial."
            }
    except Exception as e:
        logger.exception("Error al eliminar las conversaciones")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/viajes/{viaje_id}", response_model=ViajeRead)
def actualizar_viaje(viaje_id: int, viaje_data: ViajeUpdate):
    with Session() as session:
        viaje = session.query(Viaje).filter_by(id=viaje_id).first()
        if not viaje:
            raise HTTPException(status_code=404, detail="Viaje no encontrado")

        # Actualizar solo los campos enviados
        for field, value in viaje_data.dict(exclude_unset=True).items():
            setattr(viaje, field, value)

        session.commit()
        session.refresh(viaje)
        return viaje