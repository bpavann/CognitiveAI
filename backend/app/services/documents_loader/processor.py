# Imports
import os
import sys
import json
import logfire
import uuid
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.http import models
from app.core.settings import settings
from app.services.documents_loader.schema import DocumentChunk
from app.services.retrieval.embedding_service import embed_texts, get_embedding_dim
from app.services.documents_loader.loader import parse_pdf,parse_html,parse_text,parse_office,parse_json,parse_csv,parse_xlsx
from app.services.documents_loader.splitter import chunk_text

# Configuration
logfire.configure(service_name="CognitiveAI-ingestion-service")

# Local folder where parsed + chunked JSON metadata is saved (replaces GCS processed bucket)
PROCESSED_DATA_DIR = "processed_data"

# Initialize Qdrant Client
qdrant_client = QdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY,
    timeout=60
)
print("Connected to Qdrant")

print("\nCollections:")
print(qdrant_client.get_collections())

print("\nTesting collection:")
print(qdrant_client.collection_exists(settings.QDRANT_COLLECTION))

# Constants
SUPPORTED_EXTENSIONS = {".pdf",".html",".htm",".txt",".json",".csv",".docx",".pptx",".xlsx"}
VALID_INDUSTRIES = {"logistics","ecommerce","enterprise","finance"}
VALID_DATA_QUALITY = {"clean","noisy"}

VALID_INDUSTRIES = {
    "logistics",
    "ecommers",
    "enterprise",
    "finance_risk",
}

VALID_DATA_QUALITY = {
    "true_data",
    "noisy_data",
}

def discover_files(base_dir: str):
    """
    Recursively discover supported files and determine:

        industry
        data_quality

    Expected directory structure:

        dataset/
        ├── Logistics/
        │   ├── true_data/
        │   └── noisy_data/
        ├── Ecommers/
        │   ├── true_data/
        │   └── noisy_data/
        ├── Enterprise/
        │   ├── true_data/
        │   └── noisy_data/
        └── Finance_Risk/
            ├── true_data/
            └── noisy_data/

    Returns:
        (file_path, industry, data_quality)
    """

    base_path = Path(base_dir)

    for file_path in base_path.rglob("*"):

        # Ignore directories
        if not file_path.is_file():
            continue
        # Ignore macOS system files
        if file_path.name == ".DS_Store":
            continue
        # Ignore unsupported file types
        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            logfire.warning(f"Skipping unsupported file type: {file_path}")
            continue

        # Get path relative to dataset directory
        relative_parts = file_path.relative_to(base_path).parts

        # Expected:
        # industry / data_quality / filename
        if len(relative_parts) < 3:
            logfire.warning(f"Invalid directory structure: {file_path}")
            continue

        # Get actual folder names
        industry = relative_parts[0].lower()
        data_quality = relative_parts[1].lower()

        # Validate industry
        if industry not in VALID_INDUSTRIES:
            logfire.warning(f"Unknown industry '{industry}' for file: {file_path}")
            continue

        # Validate data quality
        if data_quality not in VALID_DATA_QUALITY:
            logfire.warning(f"Unknown data quality '{data_quality}' for file: {file_path}")
            continue

        # Valid file discovered
        logfire.info(f"Discovered file: {file_path} | industry={industry} | data_quality={data_quality}")

        yield file_path, industry, data_quality

# Main Ingestion Controller
def run_universal_ingestion(
    base_dir: str,
    wipe: bool = False,
):
    """
    Scan the complete data directory recursively and ingest
    documents from all industries.
    Pipeline:
        Discover
            ↓
        Parse
            ↓
        Chunk
            ↓
        DocumentChunk
            ↓
        Save processed metadata
            ↓
        Embed
            ↓
        Qdrant
    """
    with logfire.span("Universal Ingestion Started",base_directory=base_dir):

        # 1. Wipe Qdrant collection if requested
        if wipe:
            with logfire.span("Wiping Collection"):
                print("Attempting collection deletion...")
                if qdrant_client.collection_exists(settings.QDRANT_COLLECTION):
                    qdrant_client.delete_collection(settings.QDRANT_COLLECTION)
                    logfire.info(f"Collection '{settings.QDRANT_COLLECTION}' deleted.")
                print("Collection deleted successfully")

        # 2. Create Qdrant collection if it doesn't exist
        if not qdrant_client.collection_exists(settings.QDRANT_COLLECTION):
            dim = get_embedding_dim()
            qdrant_client.create_collection(
                collection_name=settings.QDRANT_COLLECTION,
                vectors_config=models.VectorParams(
                    size=dim,
                    distance=models.Distance.COSINE,
                ),
            )
            logfire.info(f"Created collection '{settings.QDRANT_COLLECTION}' ({dim}-dim, Cosine).")
        
        # 3. Ensure payload indexes exist
        qdrant_client.create_payload_index(
            collection_name=settings.QDRANT_COLLECTION,
            field_name="industry",
            field_schema=models.PayloadSchemaType.KEYWORD,
        )

        qdrant_client.create_payload_index(
            collection_name=settings.QDRANT_COLLECTION,
            field_name="data_quality",
            field_schema=models.PayloadSchemaType.KEYWORD,
        )

        logfire.info(
            "Qdrant payload indexes ensured: "
            "industry=KEYWORD, data_quality=KEYWORD"
        )

        # 4. Discover files recursively
        files = list(discover_files(base_dir))
        logfire.info(f"Discovered {len(files)} supported files for ingestion.")

        # 5. Process every file
        for (file_path,industry,data_quality,) in files:
            process_file(
                file_path=str(file_path),
                filename=file_path.name,
                industry=industry,
                data_quality=data_quality,
            )

# Process One File
def process_file(file_path: str,filename: str,industry: str,data_quality: str):
    """
    Process a single file.
    Pipeline:
        Parse
          ↓
        Chunk
          ↓
        DocumentChunk
          ↓
        Save JSON
          ↓
        Embed
          ↓
        Qdrant
    """
    with logfire.span( "Processing File",file=filename,industry=industry,data_quality=data_quality,):
        try:
            # 1. Determine file extension
            ext = filename.lower().rsplit(".", 1)[-1]

            # 2. Parse document / create chunks
            if ext == "pdf":
                full_text = parse_pdf(file_path)

            elif ext in ("html", "htm"):
                full_text = parse_html(file_path)

            elif ext == "txt":
                full_text = parse_text(file_path)

            elif ext == "json":
                full_text = parse_json(file_path)

            elif ext in ("docx", "pptx"):
                full_text = parse_office(file_path)
                
            elif ext == "xlsx":
                full_text = parse_xlsx(file_path)

            elif ext == "csv":
                csv_chunks = parse_csv(file_path)
                chunks = [
                    DocumentChunk(
                        chunk_id=str(uuid.uuid4()),
                        content=content,
                        source=file_path,
                        metadata={
                            "industry": industry,
                            "data_quality": data_quality,
                            "source_type": "csv",
                        },
                    )
                    for content in csv_chunks
                ]
            else:
                logfire.warning(f"Skipping unsupported file type: {filename}")
                return


            # 3. Normal document validation + chunking
            if ext != "csv":
                if not full_text or not full_text.strip():
                    logfire.warning(f"No text extracted from {filename} — skipping.")
                    return

                chunks = chunk_text(
                    full_text,
                    source=file_path,
                    industry=industry,
                    data_quality=data_quality,
                )

            # 4. Validate chunks
            if not chunks:
                logfire.warning(f"No chunks generated for {filename}.")
                return

            # 5. Save processed metadata locally
            processed_data = {
                "filename": filename,
                "industry": industry,
                "data_quality": data_quality,
                "chunks": [
                    chunk.model_dump()
                    for chunk in chunks
                ],
            }

            
            local_path = save_processed_locally(data=processed_data,industry=industry,data_quality=data_quality,filename=filename)
            logfire.info(f"Saved processed data → {local_path}")

            # 6. Generate embeddings
            with logfire.span("Vectorizing & Indexing"):
                embeddings = embed_texts([chunk.content for chunk in chunks])
                # 7. Create Qdrant points
                points = [
                    models.PointStruct(
                        id=chunk.chunk_id,
                        vector=vector,
                        payload={
                            "text": chunk.content,
                            "source": chunk.source,
                            "page": chunk.page,
                            "industry": chunk.metadata.get("industry"),
                            "data_quality": chunk.metadata.get("data_quality"),
                            "source_type": chunk.metadata.get("source_type"),
                            "metadata": chunk.metadata,
                        },
                    )
                    for chunk, vector in zip(chunks, embeddings)
                ]

                # 8. Upsert into Qdrant
                BATCH_SIZE = 500
                for i in range(0, len(points), BATCH_SIZE):
                    batch = points[i:i + BATCH_SIZE]
                    qdrant_client.upsert(
                        collection_name=settings.QDRANT_COLLECTION,
                        points=batch,
                    )
                    logfire.info(f"Indexed batch {i // BATCH_SIZE + 1} ({len(batch)} points) from {filename}")

        except Exception as e:
            logfire.error(f"Failed to process {filename}: {e}")
# Save Processed JSON
def save_processed_locally(data: dict,industry: str,data_quality: str,filename: str,) -> str:
    """
    Save processed chunk metadata as: processed_data
    """
    folder = os.path.join(PROCESSED_DATA_DIR,industry,data_quality)
    os.makedirs(folder,exist_ok=True)
    dest = os.path.join(folder,f"{filename}.json")
    with open(dest,"w",encoding="utf-8",) as f:
        json.dump(data,f,ensure_ascii=False,indent=2)
    return dest

# Command Line Execution
if __name__ == "__main__":
    # Usage:
    #   python -m app.services.documents_loader.processor data
    #   python -m app.services.documents_loader.processor data --wipe
    wipe_requested = "--wipe" in sys.argv
    clean_args = [
        arg
        for arg in sys.argv
        if arg != "--wipe"
    ]
    target_dir = (
        clean_args[1]
        if len(clean_args) > 1
        else "data"
    )
    if not os.path.exists(target_dir):
        print(f"Error: path '{target_dir}' does not exist.")
        sys.exit(1)
    run_universal_ingestion(base_dir=target_dir,wipe=wipe_requested,)
    logfire.info("Ingestion job completed.")