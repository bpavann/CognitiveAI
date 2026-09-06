import logfire
from qdrant_client import QdrantClient
from app.core.settings import settings
from app.services.retrieval.embedding_service import embed_query
from qdrant_client.models import Filter, FieldCondition, MatchValue

qdrant_client = QdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY,
)

# Search Function
def search_cognitiveai_knowledge(query: str,limit: int = 15,industry: str | None = None,data_quality: str | None = None,) -> list[dict]:
    """
    Performs .
    Performs a high-precision semantic similarity search in Qdrant.
    Uses the modern query_points interface and metadata filters:
        industry
        data_quality
    """
    if not query or not query.strip():
        return []

    try:
        # 1. Generate query embedding
        query_vector = embed_query(query)

        # Select matching collection
        collection_name = settings.QDRANT_COLLECTION

        # 2. Build metadata filters
        filter_conditions = []

        if industry:
            filter_conditions.append(FieldCondition(key="industry",match=MatchValue(value=industry)))

        if data_quality:
            filter_conditions.append(FieldCondition(key="data_quality",match=MatchValue(value=data_quality)))

        query_filter = None

        if filter_conditions:
            query_filter = Filter(must=filter_conditions)

        # 3. Qdrant similarity search
        logfire.info("Qdrant search",collection=collection_name,embedding_model="all-mpnet-base-v2",limit=limit,industry=industry,data_quality=data_quality)

        response = qdrant_client.query_points(collection_name=collection_name,query=query_vector,query_filter=query_filter,limit=limit,with_payload=True).points

    except Exception as exc:
        logfire.error(f"Qdrant search failed: {exc}")
        raise

    # 4. Format retrieval results
    results = []
    for hit in response:
        payload = hit.payload or {}
        results.append(
            {
                "content": (
                    payload.get("text")
                    or payload.get("content")
                    or ""
                ),
                "source": payload.get("source"),
                "page": payload.get("page"),
                "industry": payload.get("industry"),
                "data_quality": payload.get("data_quality"),
                "source_type": payload.get("source_type"),
                "metadata": payload.get("metadata", {}),
                "score": hit.score,
            }
        )
    logfire.info(f"Qdrant returned {len(results)} results")
    return results
