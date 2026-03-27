from langchain_core.tools.retriever import create_retriever_tool
from langchain_qdrant import QdrantVectorStore

from rag.shared import client, embeddings, COLLECTION_NAME

_vector_store = QdrantVectorStore(
    client=client,
    collection_name=COLLECTION_NAME,
    embedding=embeddings,
    content_payload_key="text",
)

retriever = _vector_store.as_retriever(search_kwargs={"k": 3})

retriever_tool = create_retriever_tool(
    retriever=retriever,
    name="retrieve_document_info_tool",
    description="useful for retrieving information from uploaded documents",
)
