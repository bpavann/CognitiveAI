import uuid
import logfire
from pathlib import Path
from typing import List

from app.services.documents_loader.schema import DocumentChunk


def chunk_text(
    text: str,
    source: str,
    industry: str,
    data_quality: str,
    chunk_size: int = 1500,
) -> List[DocumentChunk]:
    """
    Split text into chunks and return standardized
    DocumentChunk objects.
    """

    with logfire.span(
        "Text Chunking",
        text_length=len(text),
        source=source,
        industry=industry,
        data_quality=data_quality,
    ):
        if not text.strip():
            return []

        paragraphs = text.split("\n\n")

        chunks: List[DocumentChunk] = []
        current_chunk = ""

        for paragraph in paragraphs:
            paragraph = paragraph.strip()

            if not paragraph:
                continue

            if len(current_chunk) + len(paragraph) <= chunk_size:
                current_chunk += paragraph + "\n\n"

            else:
                if current_chunk.strip():
                    chunks.append(
                        DocumentChunk(
                            chunk_id=str(uuid.uuid4()),
                            content=current_chunk.strip(),
                            source=source,
                            metadata={
                                "industry": industry,
                                "data_quality": data_quality,
                                "source_type": Path(source).suffix.lower().lstrip("."),
                            },
                        )
                    )

                current_chunk = paragraph + "\n\n"

        if current_chunk.strip():
            chunks.append(
                DocumentChunk(
                    chunk_id=str(uuid.uuid4()),
                    content=current_chunk.strip(),
                    source=source,
                    metadata={
                        "industry": industry,
                        "data_quality": data_quality,
                        "source_type": Path(source).suffix.lower().lstrip("."),
                    },
                )
            )

        logfire.info(
            f"Generated {len(chunks)} document chunks"
        )

        return chunks