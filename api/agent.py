from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from google.adk.runners import Runner
from google.genai import types
from agents.orquestator import orchestrator_agent
from data.schemas import QueryRequest
from core.session import session_service

router = APIRouter()

APP_NAME = "viajes_habana_app"
ADMIN_USER_ID = "admin"

# Inicializa runner del orquestador (si no está inicializado globalmente)
runner_orchestrator = Runner(
    agent=orchestrator_agent,
    app_name=APP_NAME,
    session_service= session_service
)

@router.post("/orquestator")
async def call_orquestator_async(req: QueryRequest, session_id: Optional[str] = Query(default=None)):
    try:
        if session_id is None:
            session_id = "default_session"
            await session_service.create_session(app_name=APP_NAME, user_id=ADMIN_USER_ID, session_id=session_id)

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
            raise ValueError("No se recibió respuesta final del agente.")

        return {"response": final_response_text, "session_id": session_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))