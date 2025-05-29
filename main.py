import os
import uuid
import logging
import warnings
from fastapi import FastAPI

from core.config import settings
from core.session import session_service

from contextlib import asynccontextmanager

from api.routers import viajes, agent, memory

# Ignore all warnings
warnings.filterwarnings("ignore")

# Configura logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


os.environ['GOOGLE_API_KEY'] = settings.GOOGLE_API_KEY

@asynccontextmanager
async def lifespan(app: FastAPI):
    await session_service.create_session(
        app_name=settings.APP_NAME,
        user_id=settings.ADMIN_USER_ID,
        session_id='default_session'
    )
    yield 

app = FastAPI(title="Sistema Multiagente ADK", lifespan=lifespan)

app.include_router(viajes.router, prefix="/viajes", tags=["Viajes"])
app.include_router(agent.router, prefix="/agent", tags=["agent"])
app.include_router(memory.router, prefix="/memory", tags=["memory"])

