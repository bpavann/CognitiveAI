import logfire

from app.config.settings import settings


def configure_logfire() -> None:
    """
    Configure Logfire for CognitiveAI.
    """

    logfire.configure(
        token=settings.LOGFIRE_TOKEN,
        service_name=settings.app_name,
    )