from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from app.agents.state import AgentState
from app.agents.planner_node import planner_node
from app.agents.retriever_node import retrieve_node
from app.agents.responder_node import generate_node
from app.agents.coding_node import coding_agent_node

# Create workflow
workflow = StateGraph(AgentState)

# Nodes
workflow.add_node("planner",planner_node)
workflow.add_node("retriever",retrieve_node,)
workflow.add_node("responder",generate_node)
workflow.add_node("coding_agent", coding_agent_node)

# Planner routing
def route_planner(state: AgentState):
    if state["agent_type"] == "RESEARCH":
        return "retriever"
    if state["agent_type"] == "CODING":
        return "coding_agent"
    return "responder"

# Entry point and node connection
workflow.set_entry_point("planner")
workflow.add_conditional_edges(
    "planner",
    route_planner,
    {
        "retriever": "retriever",
        "coding_agent": "coding_agent",
        "responder": "responder",
    },
)
workflow.add_edge("coding_agent", "responder")

workflow.add_edge("retriever","responder")
workflow.add_edge("responder",END)

# Memory
checkpointer = MemorySaver()

# Compile
cognitive_ai_agent = workflow.compile(checkpointer=checkpointer)