import logfire
from fastapi import FastAPI
from app.api.routes import chat, health
from app.core.settings import settings
from app.observability.logfire_config import configure_logfire
from app.observability.langsmith_config import configure_langsmith

# Observability
configure_logfire()
configure_langsmith()

# FastAPI
app = FastAPI(
    title=settings.app_name,
    description="Modular Multi-Agent AI Orchestration Platform",
    version="0.1.0",
)

# Instrument FastAPI with Logfire
logfire.instrument_fastapi(app)

# Routes
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