from fastapi import FastAPI

from app.api.routes import chat, health
from app.core.settings import settings


app = FastAPI(
    title=settings.app_name,
    description="Modular Multi-Agent AI Orchestration Platform",
    version="0.1.0",
)


app.include_router(
    health.router,
    prefix="/api",
    tags=["Health"],
)


app.include_router(
    chat.router,
    prefix="/api",
    tags=["Chat"],
)


@app.get("/")
async def root():
    return {
        "message": "Welcome to CognitiveAI",
        "version": "0.1.0",
    }