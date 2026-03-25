import os
from typing import Iterable, Optional

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from .text_splitter import text_splitter

load_dotenv()

QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_PORT = os.getenv("QDRANT_PORT")
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


def ingest_urls(urls: Iterable[str], chunk_size: Optional[int] = None, chunk_overlap: Optional[int] = None):
    docs = text_splitter(urls=tuple(urls), chunk_size=chunk_size or 1000, chunk_overlap=chunk_overlap or 200)
    if not docs:
        print(f"Warning: No documents loaded from URLs: {list(urls)}")
        return
    get_vector_store().add_documents(documents=docs)


def ingest_url(url: str, chunk_size: Optional[int] = None, chunk_overlap: Optional[int] = None):
    ingest_urls((url,), chunk_size=chunk_size, chunk_overlap=chunk_overlap)
