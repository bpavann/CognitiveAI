from portkey_ai import Portkey,createHeaders, PORTKEY_GATEWAY_URL
from langchain_openai import ChatOpenAI
from app.core.settings import settings

# Initialize Portkey client
portkey_client = Portkey(
    api_key=settings.PORTKEY_API_KEY,
    config=settings.PORTKEY_CONFIG_ID
)

# Function to create a Portkey-backed ChatOpenAI client
def get_llm(feature: str = "cognitiveai-chat") -> ChatOpenAI:
    """
    Create and return a Portkey-backed LangChain LLM.

    Portkey is responsible for:
    - Model routing
    - Fallbacks
    - Retries
    - Caching
    - Gateway-level configuration

    CognitiveAI only needs to request an LLM
    through this interface..
    """
    return ChatOpenAI(
        base_url=PORTKEY_GATEWAY_URL,
        api_key=settings.PORTKEY_API_KEY,
        # Primary model.
        # Fallbacks are handled by the Portkey Config.
        model=f"@{settings.OPENAI_SLUG}/gpt-4.1-mini",
        temperature=0,
        default_headers=createHeaders(
            api_key=settings.PORTKEY_API_KEY,
            config=settings.PORTKEY_CONFIG_ID,
            metadata={
                "feature": feature,
                "_user": settings.app_name,
                "environment": settings.environment
            },
        ),
    )

# Function to extract cache status from Portkey response
def extract_cache_status(response) -> str:
    """
    Extract Portkey cache status from an LLM response.

    Returns:
        HIT
        MISS
        or another Portkey cache status.
    """
    for attr in ("_raw_response", "_response", "_http_response"):
        raw = getattr(response, attr, None)
        if raw is not None:
            status = getattr(raw, "headers", {}).get("x-portkey-cache-status", "")
            if status:
                return status.upper()
    return "MISS"