from fastapi import APIRouter
from pydantic import BaseModel


from app.gateway.service import LLMService

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str

# LLM Service From PortkeyAI 
llm_service = LLMService()

# Chat Endpoint

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    response = await llm_service.generate(request.message)
    return ChatResponse(
        response=response
    )