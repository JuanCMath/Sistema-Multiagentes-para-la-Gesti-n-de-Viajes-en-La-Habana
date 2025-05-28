import os
import uuid
import logging
import warnings
from fastapi import FastAPI

from core.config import settings
from core.session import session_service

from api import viajes, agent

# Ignore all warnings
warnings.filterwarnings("ignore")

# Configura logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI(title="Sistema Multiagente ADK")
app.include_router(viajes.router, prefix="/viajes", tags=["Viajes"])
app.include_router(agent.router, prefix="/agent", tags=["agent"])

os.environ['GOOGLE_API_KEY'] = settings.GOOGLE_API_KEY


APP_NAME = "viajes_habana_app"
ADMIN_USER_ID = "admin"


@app.on_event("startup")
async def startup():
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=ADMIN_USER_ID,
        session_id='default_session'
    )
    

# Endpoint para inicializar una nueva sesión
@app.post("/init_session")
def init_session():
    session_id = str(uuid.uuid4())
    session_service.create_session(app_name=APP_NAME, user_id=ADMIN_USER_ID, session_id=session_id)
    return {"session_id": session_id}


