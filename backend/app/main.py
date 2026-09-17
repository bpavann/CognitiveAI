import logfire
import uvicorn
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI,Response
from app.config.settings import settings
from app.agents.graph import cognitive_ai_agent
from app.observability.logfire_config import configure_logfire
from app.observability.langsmith_config import configure_langsmith
from app.nemoguard.guardrails import check_input, check_output
from app.nemoguard.security_check import mask_output_pii, check_answer_grounding

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
    thread_id: Optional[str] = "default_user"

class ChatResponse(BaseModel):
    question: str
    answer: str
    thought_process: list[str]
    status: str
    documents: list[dict]

@app.get("/")
def home():
    return {"message": "CognitiveAI Decision Intelligence Platform"}

@app.get("/graph")
def get_graph_image():
    """
    Returns the Mermaid image of the agent's workflow.
    """
    try:
        png_bytes = cognitive_ai_agent.get_graph().draw_mermaid_png()
        return Response(content=png_bytes, media_type="image/png")
    except Exception as e:
        return {"error": f"Could not generate graph image: {e}"}

# Chat Endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Executes the CognitiveAI pipeline with LangGraph.
    """
    with logfire.span("chat_request"):
        logfire.info(f"📥 User request: {request.message[:100]}")

        # LANGGRAPH
        ## Input Guardrails
        logfire.info("🛡️ Running input guardrails.")
        try:
            input_result = await check_input(request.message)
            input_content = input_result.get("content", "")

            if input_content == "I'm sorry, I can't respond to that.":
                logfire.warning("🛡️ Input blocked by NeMo Guardrails.")
                return ChatResponse(
                    question=request.message,
                    answer=input_content,
                    thought_process=["NeMo Guardrails: Input Blocked",],
                    status="blocked",
                    documents=[]
                )
            logfire.info("🛡️ Input guardrails completed.")
        except Exception as exc:
            logfire.exception("❌ Input guardrails failed",error=str(exc))
            return ChatResponse(
                question=request.message,
                answer="I apologize, but I could not safely process your request.",
                thought_process=["NeMo Guardrails: Input Guardrail Error"],
                status="guardrail_error",
                documents=[]
            )
        logfire.info("🧠 Starting LangGraph pipeline.")
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
            "plan": ["LangGraph: Started",],
            "status": "Initializing Graph...",
            "final_answer": ""
        }

        config = {"configurable": {"thread_id": request.thread_id}}

        with logfire.span("cognitiveai_pipeline"):
            try:
                final_output = cognitive_ai_agent.invoke(state,config=config)
                logfire.info("✅ LangGraph pipeline completed.")
                
                # Output Gaurdrails
                logfire.info("🛡️ Running output guardrails.")
                bot_response = final_output.get("final_answer", "")
                documents = final_output.get("documents", [])
                if documents:
                    grounded = check_answer_grounding(bot_response,documents)

                    if not grounded:
                        logfire.warning("⚠️ Answer failed grounding check.")
                        return ChatResponse(
                            question=request.message,
                            answer="I could not generate a sufficiently grounded answer from the available knowledge.",
                            thought_process=final_output.get("plan", []) + [
                                "Grounding Guardrail: Answer Not Sufficiently Grounded"
                            ],
                            status="grounding_failed",
                            documents=documents
                        )
                # Output Guard
                bot_response = mask_output_pii(bot_response)
                output_result = await check_output(request.message,bot_response)
                output_content = output_result.get("content", "")
                logfire.info("🛡️ Output guardrails completed.")

                if output_content == "I'm sorry, I can't respond to that.":
                    logfire.warning("🛡️ Output blocked by NeMo Guardrails.")
                    return ChatResponse(
                        question=request.message,
                        answer=output_content,
                        thought_process=final_output.get("plan", []) + [
                            "NeMo Guardrails: Output Blocked"
                        ],
                        status="blocked",
                        documents=final_output.get("documents", [])
                    )
                return ChatResponse(
                    question=request.message,
                    answer=bot_response,
                    thought_process=final_output.get("plan", []),
                    status=final_output.get("status", ""),
                    documents=final_output.get("documents", [])
                )

            except Exception as exc:
                logfire.exception(
                    "❌ CognitiveAI execution failed",
                    error=str(exc),
                    thread_id=request.thread_id
                )
                return ChatResponse(
                    question=request.message,
                    answer=(
                        "I apologize, but I encountered an "
                        "internal error while processing your request."
                    ),
                    thought_process=[
                        "LangGraph: Execution Error",
                    ],
                    status="error",
                    documents=[]
                )

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
