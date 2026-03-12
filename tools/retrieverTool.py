

from RAG import vector_store

from langchain_core.tools.retriever import create_retriever_tool


retriever = vector_store.as_retriever(search_kwargs={"k": 2})
retriever_tool = create_retriever_tool(
    retriever=retriever,
    name= "retrieve_article_info_tool",
    description="useful for retrieving information about the article"
)