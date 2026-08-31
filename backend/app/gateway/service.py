import logfire
from langchain_core.messages import HumanMessage
from app.gateway.client import get_llm


class LLMService:
    """
    Application-level service responsible for
    interacting with the configured LLM.
    """
    def __init__(self):
        self.llm = get_llm(feature="cognitiveai-chat")

    async def generate(self,message: str,) -> str:
        with logfire.span("llm_creation", feature="cognitiveai-chat"): 
            response = await self.llm.ainvoke(message)
            return response.content