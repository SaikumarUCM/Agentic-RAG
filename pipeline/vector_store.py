import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
COLLECTION_NAME = "documents"
VECTOR_DIM = 768  # intfloat/e5-base output dimension

_client = None


def _get_client() -> QdrantClient:
    global _client
    if _client is None:
        _client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    return _client


def _ensure_collection():
    client = _get_client()
    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_DIM, distance=Distance.COSINE),
        )


def store_vectors(chunks, embeddings):
    _ensure_collection()
    client = _get_client()

    points = [
        PointStruct(
            id=i,
            vector=emb,
            payload={"text": chunks[i].page_content, "source": chunks[i].metadata.get("source", "")},
        )
        for i, emb in enumerate(embeddings)
    ]

    client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"Stored {len(points)} vectors in Qdrant collection '{COLLECTION_NAME}'")
