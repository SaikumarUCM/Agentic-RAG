from langchain_core.prompts import ChatPromptTemplate

rag_answer_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant. Use the following context retrieved from the knowledge base to answer the user's question accurately.

Context:
{context}

If the context does not contain enough information, say so honestly."""),
    ("human", "{question}"),
])
