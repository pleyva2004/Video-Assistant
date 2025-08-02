from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from sentence_transformers import SentenceTransformer



def query_qdrant(
    client,
    question: str,
    collection_name: str,
    top_k: int = 5,
    model_name: str = "all-MiniLM-L6-v2"
):

    model = SentenceTransformer(model_name)

    query_vector = model.encode(question)

    results = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=top_k
    )

    # Format results
    matches = []
    for result in results:
        matches.append({
            "score": result.score,
            "text": result.payload.get("text"),
            "chunk_index": result.payload.get("chunk_index"),
            "video_id": result.payload.get("video_id")
        })

    return matches


if __name__ == "__main__":

    client = QdrantClient(":memory:")

    collection_name = "youtube_transcripts"

    query = "what was the speaker’s main point?"

    results = query_qdrant(question=query, collection_name=collection_name)

    print(results)



