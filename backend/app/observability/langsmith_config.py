import os

from app.core.settings import settings


def configure_langsmith() -> None:
    """
    Configure LangSmith tracing.
    """

    os.environ["LANGSMITH_TRACING"] = (settings.LANGSMITH_TRACING)
    os.environ["LANGSMITH_API_KEY"] = (settings.LANGSMITH_API_KEY)
    os.environ["LANGSMITH_PROJECT"] = (settings.LANGSMITH_PROJECT)
    os.environ["LANGSMITH_ENDPOINT"]= (settings.LANGSMITH_ENDPOINT)
    