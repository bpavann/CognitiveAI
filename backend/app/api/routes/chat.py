import logfire
from fastapi import APIRouter
from pydantic import BaseModel
from app.services.llmgateway.service import LLMService

router = APIRouter()
llm_service = LLMService()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str


# Chat Endpoint
@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    with logfire.span("chat_request"):
        response = await llm_service.generate(request.message)
        return ChatResponse(response=response)
