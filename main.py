import bootstrap

import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types, Client

from Agent.Agent import orchestrator_agent

# Configura logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sistema Multiagente ADK")

# Servicio de sesiones en memoria
session_service = InMemorySessionService()
APP_NAME = "viajes_habana_app"

runner_orchestrator = Runner(agent=orchestrator_agent, app_name=APP_NAME, session_service=session_service)

# Modelos de datos
class QueryRequest(BaseModel):
    user_id: str
    session_id: str
    query: str

class SessionRequest(BaseModel):
    user_id: str
    session_id: Optional[str] = None

# Endpoints
@app.post("/session/create")
async def create_session(req: SessionRequest):
    try:
        sid = req.session_id or os.urandom(8).hex()
        session = session_service.create_session(
            app_name=APP_NAME,
            user_id=req.user_id,
            session_id=sid
        )
        return {"session_id": req.session_id, "user_id": session.user_id}
    except Exception as e:
        logger.exception("Error creando sesión")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/session/delete")
async def delete_session(req: SessionRequest):
    try:
        session_service.delete_session(
            app_name=APP_NAME,
            user_id=req.user_id,
            session_id=req.session_id
        )
        return {"status": "deleted", "session_id": req.session_id}
    except Exception as e:
        logger.exception("Error eliminando sesión")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/agent/orquestator")
async def call_orquestator_async(req: QueryRequest):
    try:
        content = types.Content(role="user", parts=[types.Part(text=req.query)])
        final_response_text = None

        print("Ejecutando consulta al agente...!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        async for event in runner_orchestrator.run_async(
            user_id=req.user_id,
            session_id=req.session_id,
            new_message=content
        ):
            if event.is_final_response() and event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
                break

        if final_response_text is None:
            raise ValueError("No se recibió respuesta final del agente.")
        
        return {"response": final_response_text}

    except Exception as e:
        logger.exception("Error procesando consulta al agente")
        raise HTTPException(status_code=500, detail=str(e))
