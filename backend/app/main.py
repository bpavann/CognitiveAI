import logfire
from fastapi import FastAPI
from pydantic import BaseModel
from app.config.settings import settings
from app.observability.logfire_config import configure_logfire
from app.observability.langsmith_config import configure_langsmith
from app.agents.graph import cognitive_ai_agent

# Observability
configure_logfire()
configure_langsmith()

# FastAPI
app = FastAPI(
    title=settings.app_name,
    description="Modular Multi-Agent AI Orchestration Platform",
    version="0.1.0"
)

# Instrument FastAPI with Logfire
logfire.instrument_fastapi(app)

# Request / Response Models
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

# Chat Endpoint
@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    with logfire.span("chat_request"):
        state = {
            "messages": [
                {
                    "role": "user",
                    "content": request.message,
                }
            ],
            "current_query": "",
            "agent_type": "",
            "documents": [],
            "plan": [],
            "status": "",
            "final_answer": ""
        }
        config = {"configurable": {"thread_id": "default"}}
        result = cognitive_ai_agent.invoke(state,config=config)
        
        return ChatResponse(response=result["final_answer"])

# Root Endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to CognitiveAI","version": "0.1.0"}
