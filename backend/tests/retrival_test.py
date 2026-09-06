from app.services.retrieval.qdrant_service import search_cognitiveai_knowledge


query = "What are the six functions in the NIST Cybersecurity Framework 2.0?"

results = search_cognitiveai_knowledge(
    query="What are the six functions in the NIST Cybersecurity Framework 2.0?",
    limit=15,
    industry="enterprise",
)

print(f"\nQuery: {query}")
print(f"Results: {len(results)}")

for i, result in enumerate(results, 1):
    print("\n" + "=" * 80)
    print(f"RESULT {i}")
    print(f"Score: {result.get('score')}")
    print(f"Industry: {result.get('industry')}")
    print(f"Data Quality: {result.get('data_quality')}")
    print(f"Source: {result.get('source')}")
    print(f"Page: {result.get('page')}")
    print(f"Content:\n{result.get('content', '')[:500]}")