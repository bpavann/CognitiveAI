from app.services.retrieval.qdrant_service import search_cognitiveai_knowledge
from app.services.retrieval.reranking_service import rerank_documents_fr


query = "What is Zero Trust Architecture according to NIST SP 800-207?"

results = search_cognitiveai_knowledge(
    query=query,
    limit=15
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
    print(f"Source_category: {result.get('source_category')}")
    print(f"Data Quality: {result.get('data_quality')}")
    print(f"Source: {result.get('source')}")
    print(f"Page: {result.get('page')}")
    print(f"Content:\n{result.get('content', '')[:500]}")