from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from typing import List, Tuple
import uuid

def upload_chunks_to_qdrant(
    client,
    chunk_texts: List[str],
    chunk_embeddings: List[List[float]],
    collection_name: str = "youtube_transcripts",
    video_id: str = None,
    qdrant_url: str = "http://localhost:6333",
    qdrant_api_key: str = None,
):
    """
    Uploads chunk embeddings and texts to Qdrant collection.

    Args:
        chunk_texts: List of chunked text segments.
        chunk_embeddings: List of corresponding embedding vectors.
        collection_name: Name of the Qdrant collection to use.
        video_id: Optional metadata to tag chunks with the source video.
        qdrant_url: Qdrant instance URL (local or cloud).
        qdrant_api_key: API key for Qdrant Cloud, if applicable.
    """

    # Build points
    points = [
        PointStruct(
            id=str(uuid.uuid4()),  # safer for distributed settings
            vector=chunk_embeddings[i],
            payload={
                "text": chunk_texts[i],
                "chunk_index": i,
                "video_id": video_id
            }
        )
        for i in range(len(chunk_texts))
    ]

    client.upsert(
        collection_name=collection_name,
        points=points
    )

    # print(f"Uploaded {len(points)} chunks to collection '{collection_name}'")
