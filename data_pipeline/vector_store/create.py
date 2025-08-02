from qdrant_client.models import VectorParams, Distance, PointStruct

# Cloud example
# client = QdrantClient(
#     url="https://your-qdrant-endpoint",
#     api_key="your-secret-key"
# )

def create_collection(client, collection_name, vector_size):
    
    # Create the collection
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
    )

    