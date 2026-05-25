from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.appointments import router as appointments_router
from app.api.call import router as call_router
from app.api.conversation import router as conversation_router
from app.api.customers import router as customers_router
from app.api.documents import router as documents_router
from app.api.health import router as health_router
from app.core.database import create_tables
from app.core.qdrant import ensure_collection


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    await ensure_collection()
    yield


app = FastAPI(
    title="Cleo Voice AI",
    description="AI Voice Receptionist & Knowledge Assistant",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, tags=["health"])
app.include_router(documents_router)
app.include_router(conversation_router)
app.include_router(appointments_router)
app.include_router(customers_router)
app.include_router(call_router)
