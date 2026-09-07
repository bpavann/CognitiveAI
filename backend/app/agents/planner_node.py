from app.agents.state import AgentState
from app.services.llmgateway.client import get_llm
import logfire

# Portkey-backed LLM: fallback + cache + retry — same .invoke() interface as ChatGroq
llm = get_llm(feature="planner")

# Validate planner decision
valid_agents = {"CONVERSATIONAL","RESEARCH","CODING"}

# Planner Node
def planner_node(state: AgentState):
    """
    Planner / Router Agent.

    Responsibilities:
    1. Understand the user's latest request.
    2. Decide which agent should handle the request.
    3. Refine the query when necessary.

    Supported agent types:
        - CONVERSATIONAL
        - RESEARCH
        - CODING
    """
    messages = state.get("messages", [])

    # Extract Coversation History
    history = ""
    for msg in messages[:-1]:
        role = (
            "User"
            if msg.get("role") == "user"
            else "Assistant"
        )
        history += f"{role}: {msg.get('content', '')}\n"
    
    # Extract latest user message
    user_message = (
        messages[-1].get("content", "").strip()
        if messages
        else ""
    )

    # Handle empty input
    if not user_message:
        logfire.warning("Planner received an empty user message.")
        return {
            "agent_type": "CONVERSATIONAL",
            "current_query": "",
            "status": "No user query provided.",
            "plan": ["No query to process."],
        }

    # Planner prompt
    prompt = f"""
    You are the Planner/Router Agent for CognitiveAI.

    Choose exactly ONE agent based on the latest user message and conversation history.

    AGENTS:
    - CONVERSATIONAL: greetings, casual chat, follow-ups, general conversation.
    - RESEARCH: factual/knowledge questions requiring retrieval or grounded documentation, especially cybersecurity, NIST, AI risk, Zero Trust, and secure software.
    - CODING: writing, debugging, explaining, reviewing, or modifying code; programming, Python, APIs, FastAPI, and software engineering.

    ROUTING RULES:
    1. Choose CONVERSATIONAL for normal conversation.
    2. Choose RESEARCH when factual knowledge or grounded documentation is required.
    3. Choose CODING when the primary objective is programming or software development.
    4. If multiple categories apply, choose the user's PRIMARY objective.
    5. Preserve important technical details.
    6. Refine the query so the downstream agent can execute it.
    7. Output ONLY the requested format.

    HISTORY:
    {history}

    USER:
    {user_message}

    OUTPUT FORMAT:
    AGENT: <CONVERSATIONAL|RESEARCH|CODING>
    QUERY: <refined user query>
    """

    # Execute planner
    with logfire.span("🧠 CognitiveAI Planner"):
        try:
            response = llm.invoke(prompt)
            decision = response.content.strip()
            logfire.info(f"Planner decision: {decision}")
        except Exception as exc:
            logfire.error(f"Planner execution failed: {exc}")
            raise

    # Parse planner response
    agent_type = None
    refined_query = None

    for line in decision.splitlines():
        line = line.strip()
        if line.upper().startswith("AGENT:"):
            agent_type = (line.split(":", 1)[1].strip().upper())      
        elif line.upper().startswith("QUERY:"):
            refined_query = (line.split(":", 1)[1].strip())     

    # Validate planner decision  
    if agent_type not in valid_agents:
        logfire.warning(f"Invalid planner decision: {agent_type}. Falling back to RESEARCH.")
        agent_type = "RESEARCH"

    if not refined_query:
        refined_query = user_message

    # Build execution plan
    if agent_type == "CONVERSATIONAL":
        plan = [
            "Agent: Conversational",
            "Retrieval: Skipped",
            "Coding Agent: Skipped"
        ]
        status = ("Conversational request identified.")
    elif agent_type == "RESEARCH":
        plan = [
            "Agent: Researcher",
            f"Research Query: {refined_query}",
            "Knowledge Retrieval: Required"
        ]
        status = ("Research request identified.")
    else:
        plan = [
            "Agent: Coding",
            f"Coding Request: {refined_query}",
            "Knowledge Retrieval: Not required initially"
        ]
        status = ("Coding request identified.")

    # Logging
    logfire.info("Planner routing completed",agent_type=agent_type,current_query=refined_query)

    # Update AgentState
    return {
        "agent_type": agent_type,
        "current_query": refined_query,
        "status": status,
        "plan": plan,
    }

