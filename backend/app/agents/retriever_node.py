import logfire
from app.agents.state import AgentState
from app.services.retrieval.qdrant_service import search_cognitiveai_knowledge
from app.services.retrieval.reranking_service import rerank_documents_cai


def retrieve_node(state: AgentState):
    """
    Retrieve relevant knowledge from Qdrant
    and rerank the results using FlashRank.
    """
    query = state["current_query"]

    # Retrieve documents from Qdrant
    with logfire.span("🔍 Knowledge Retrieval"):
        logfire.info(f"Searching Qdrant for: {query}")

        raw_results = search_cognitiveai_knowledge(query,limit=15)
        logfire.info(f"Retrieved {len(raw_results)} candidates from Qdrant")

    # 3. Extract document content
    documents = [doc["content"] for doc in raw_results]

    # 4. Rerank documents
    with logfire.span("⚖️ Semantic Reranking"):

        reranked_documents = rerank_documents_cai(query,raw_results,top_n=5)

        logfire.info("Reranking complete. Kept top 5 documents.")
        
    # 5. Format documents for Responder
    formatted_documents = [
        f"CONTENT: {doc}"
        for doc in reranked_documents
    ]
    formatted_documents = [
        f"CONTENT: {doc['content']}"
        for doc in reranked_documents
    ]

    # 6. Update AgentState
    return {
        "documents": formatted_documents,
        "status": "Relevant knowledge retrieved.",
        "plan": state["plan"] + [
            "Context Retrieved"
        ]
    }