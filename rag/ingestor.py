from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore

from rag.shared import client, embeddings, COLLECTION_NAME, VECTOR_DIM


def _ensure_collection():
    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_DIM, distance=Distance.COSINE),
        )


def get_vector_store() -> QdrantVectorStore:
    _ensure_collection()
    return QdrantVectorStore(client=client, collection_name=COLLECTION_NAME, embedding=embeddings)
