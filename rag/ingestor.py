import os

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

load_dotenv()

QDRANT_HOST = os.getenv("QDRANT_HOST")
COLLECTION_NAME = "articles"
VECTOR_DIM = 1536  # text-embedding-3-small output dimension

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
_client = QdrantClient(host=QDRANT_HOST)


def _ensure_collection():
    existing = [c.name for c in _client.get_collections().collections]
    if COLLECTION_NAME not in existing:
        _client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_DIM, distance=Distance.COSINE),
        )


def get_vector_store() -> QdrantVectorStore:
    _ensure_collection()
    return QdrantVectorStore(client=_client, collection_name=COLLECTION_NAME, embedding=embeddings)
