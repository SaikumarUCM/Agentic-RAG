import os

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.tools.retriever import create_retriever_tool
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))

_embeddings = HuggingFaceEmbeddings(model_name="intfloat/e5-base")
_client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

_vector_store = QdrantVectorStore(
    client=_client,
    collection_name="documents",
    embedding=_embeddings,
    content_payload_key="text",
)

retriever = _vector_store.as_retriever(search_kwargs={"k": 3})

retriever_tool = create_retriever_tool(
    retriever=retriever,
    name="retrieve_document_info_tool",
    description="useful for retrieving information from uploaded documents",
)
