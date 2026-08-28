import os
from dotenv import load_dotenv

    # Load environment variables from .env file
load_dotenv()

class Settings():
    app_name = "CognitiveAI"
    environment= "development"
    debug = True

    api_host = "127.0.0.1"
    api_port = 8000

    # LLM API Keys
    GROQ_API_KEY  = os.getenv("GROQ_API_KEY")
    GROK_MODEL="llama-3.3-70b-versatile"
    OPENAI_API_KEY  = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY  = os.getenv("GEMINI_API_KEY")  
    
    # Portkey Gateway Settings
    PORTKEY_API_KEY = os.getenv("PORTKEY_API_KEY")
    PORTKEY_CONFIG_ID = os.getenv("PORTKEY_CONFIG_ID")
    OPENAI_SLUG = "openai-slug-1" 
    GROQ_SLUG = "groq-slug-3"
    GEMINI_SLUG = "google-slug-2" 
    
    #Vector Database Settings
    QDRANT_API_KEY  = os.getenv("QDRANT_API_KEY")
    QDRANT_URL = os.getenv("QDRANT_URL")
    QDRANT_COLLECTION = "enterprise_rag"  

    # --- REASONING ENGINE (GROQ) ---
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = "llama-3.3-70b-versatile"
    GROQ_FALLBACK_API_KEY = os.getenv("GROQ_FALLBACK_API_KEY")

    # NVIDIA API Key
    NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

    # Apply LangChain environment variables for automatic tracing
    os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGSMITH_TRACING", "true")
    os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY", "")
    os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGSMITH_PROJECT", "rag_scale_test")
    os.environ["LANGCHAIN_ENDPOINT"] = os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")

settings = Settings()