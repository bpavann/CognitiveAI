from pydantic import BaseModel, Field


class DocumentChunk(BaseModel):
    """
    Represents a processed document chunk.
    """
    chunk_id: str
    content: str
    source: str
    page: int | None = None

    metadata: dict = Field(
        default_factory=dict
    )