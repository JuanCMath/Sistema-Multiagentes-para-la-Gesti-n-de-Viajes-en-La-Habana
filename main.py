import bootstrap

import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

from Agent.Agent import orchestrator_agent

from Agent.base import settings

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
class QueryRequest(BaseModel):
    query: str

# Endpoint principal
@app.post("/agent/orquestator")
async def call_orquestator_async(req: QueryRequest):
    try:
        content = types.Content(role="user", parts=[types.Part(text=req.query)])
        final_response_text = None

        print("Ejecutando consulta al agente...!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
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
        
        return {"response": final_response_text}

    except Exception as e:
        logger.exception("Error procesando consulta al agente")
        raise HTTPException(status_code=500, detail=str(e))




test = QueryRequest(query="¿Cuál es el clima en La Habana?")

import asyncio
if __name__ == "__main__":
        try:
            asyncio.run(call_orquestator_async(test))
        except Exception as e:
            print(f"An error occurred: {e}")