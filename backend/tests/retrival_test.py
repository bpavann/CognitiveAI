from app.services.retrieval.qdrant_service import search_cognitiveai_knowledge


query = "What is Zero Trust Architecture according to NIST SP 800-207?"

results = search_cognitiveai_knowledge(
    query=query,
    limit=15
)

print(f"\nQuery: {query}")
print(f"Results: {len(results)}")

for i, result in enumerate(results, 1):
    print("\n" + "=" * 80)
    print(f"RESULT {i}")
    print(f"Score: {result.get('score')}")
    print(f"Source_category: {result.get('source_category')}")
    print(f"Data Quality: {result.get('data_quality')}")
    print(f"Source: {result.get('source')}")
    print(f"Page: {result.get('page')}")
    print(f"Content:\n{result.get('content', '')[:500]}")