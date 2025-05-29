from fastapi import APIRouter, HTTPException
from google.adk.runners import Runner
from google.genai import types
from agents.orquestator_agent import orchestrator_agent
from domain.schemas import QueryRequest
from core.session import session_service, memory_service
from core.config import settings

router = APIRouter()

# Inicializa runner del orquestador (si no está inicializado globalmente)
runner_orchestrator = Runner(
    agent=orchestrator_agent,
    app_name=settings.APP_NAME,
    session_service= session_service
)

@router.post("/orquestator")
async def call_orquestator_async(req: QueryRequest):
    try:
        session_id = "default_session"
        await session_service.create_session(app_name=settings.APP_NAME, user_id=settings.ADMIN_USER_ID, session_id=session_id)

        content = types.Content(role="user", parts=[types.Part(text=req.query)])
        final_response_text = None

        async for event in runner_orchestrator.run_async(
            user_id=settings.ADMIN_USER_ID,
            session_id=session_id,
            new_message=content
        ):
            if event.is_final_response() and event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
                break

        if final_response_text is None:
            raise ValueError("No se recibió respuesta final del agente.")

        session = await runner_orchestrator.session_service.get_session(
            app_name=settings.APP_NAME,
            user_id=settings.ADMIN_USER_ID,
            session_id=session_id
        )

        await memory_service.add_session_to_memory(session)

        return {"response": final_response_text, "session_id": session_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
