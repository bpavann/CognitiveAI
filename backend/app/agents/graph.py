from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from app.agents.state import AgentState
from app.agents.planner_node import planner_node
from app.agents.retriever_node import retrieve_node
from app.agents.responder_node import generate_node
from app.agents.coding_node import coding_agent_node

# Create workflow
graph = StateGraph(AgentState)

# Nodes
graph.add_node("planner",planner_node)
graph.add_node("retriever",retrieve_node,)
graph.add_node("responder",generate_node)
graph.add_node("coding_agent", coding_agent_node)

# Planner routing
def route_planner(state: AgentState):
    if state["agent_type"] == "RESEARCH":
        return "retriever"
    if state["agent_type"] == "CODING":
        return "coding_agent"
    return "responder"

# Entry point and node connection
graph.set_entry_point("planner")
graph.add_conditional_edges(
    "planner",
    route_planner,
    {
        "retriever": "retriever",
        "coding_agent": "coding_agent",
        "responder": "responder",
    },
)
graph.add_edge("coding_agent", "responder")

graph.add_edge("retriever","responder")
graph.add_edge("responder",END)

# Memory
checkpointer = MemorySaver()

# Compile
cognitive_ai_agent = graph.compile(checkpointer=checkpointer)