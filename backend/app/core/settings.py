import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


class Settings:
    # Application
    app_name = "CognitiveAI"
    environment = "development"
    debug = True

    api_host = "127.0.0.1"
    api_port = 8000

    # LLM API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # Groq Model
    GROQ_MODEL = "llama-3.1-8b-instant"

    # Portkey Gateway
    PORTKEY_API_KEY = os.getenv("PORTKEY_API_KEY")
    PORTKEY_CONFIG_ID = os.getenv("PORTKEY_CONFIG_ID")

    OPENAI_SLUG = "openai-slug-1"
    GROQ_SLUG = "groq-slug-3"
    GEMINI_SLUG = "google-slug-2"

    # Vector Database - Qdrant
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    QDRANT_URL = os.getenv("QDRANT_URL")
    QDRANT_COLLECTION = "enterprise_rag"

    # Groq Fallback
    GROQ_FALLBACK_API_KEY = os.getenv("GROQ_FALLBACK_API_KEY")

    # NVIDIA
    NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

    # LangSmith
    LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING")
    LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
    LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT")
    LANGSMITH_ENDPOINT = os.getenv("LANGSMITH_ENDPOINT")

    # Logfire
    LOGFIRE_TOKEN = os.getenv("LOGFIRE_TOKEN")


settings = Settings()