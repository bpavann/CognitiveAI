from app.services.retrieval.qdrant_service import search_cognitiveai_knowledge
from app.services.retrieval.reranking_service import rerank_documents_fr


query = "freight transportation and supply chain"

results = search_cognitiveai_knowledge(
    query="What are the six functions in the NIST Cybersecurity Framework 2.0?",
    limit=15,
    industry="enterprise",
    data_quality="true_data",
)

print(f"Qdrant results: {len(results)}")

reranked = rerank_documents_fr(
    query=query,
    documents=results,
    top_n=5,
)

print(f"Reranked results: {len(reranked)}")

for i, result in enumerate(reranked, 1):
    print("\n" + "=" * 80)
    print(f"RESULT {i}")
    print(f"Qdrant score: {result.get('score')}")
    print(f"Rerank score: {result.get('rerank_score')}")
    print(f"Industry: {result.get('industry')}")
    print(f"Data Quality: {result.get('data_quality')}")
    print(f"Source: {result.get('source')}")
    print(f"Page: {result.get('page')}")
    print(f"Content:\n{result.get('content', '')[:500]}")