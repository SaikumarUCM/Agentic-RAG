from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState
from langchain_openai import ChatOpenAI

from rag.retriever_tool import retriever_tool, client, embeddings
from prompts import rag_answer_prompt

load_dotenv()

_rag_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
_direct_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.9)

SIMILARITY_THRESHOLD = 0.5


def _router(state: MessagesState) -> str:
    content = state["messages"][-1].content
    user_query = content if isinstance(content, str) else " ".join(c["text"] if isinstance(c, dict) else c for c in content)
    query_vector = embeddings.embed_query(user_query)
    results = client.query_points(
        collection_name="documents",
        query=query_vector,
        limit=1,
        score_threshold=SIMILARITY_THRESHOLD,
    ).points
    route = "rag" if results else "direct"
    score = results[0].score if results else 0.0
    print(f"[ROUTER] Score: {score:.3f} → {route.upper()}")
    return route


def _rag_assistant(state: MessagesState):
    content = state["messages"][-1].content
    user_query = content if isinstance(content, str) else " ".join(c["text"] if isinstance(c, dict) else c for c in content)
    context = retriever_tool.invoke({"query": user_query})
    formatted_prompt = rag_answer_prompt.format_messages(context=context, question=user_query)
    response = _rag_llm.invoke(formatted_prompt)
    return {"messages": [response]}


def _direct_assistant(state: MessagesState):
    response = _direct_llm.invoke(state["messages"])
    return {"messages": [response]}


def agent():
    workflow = StateGraph(MessagesState)

    workflow.add_node("rag_assistant", _rag_assistant)
    workflow.add_node("direct_assistant", _direct_assistant)

    workflow.add_conditional_edges(START, _router, {
        "rag": "rag_assistant",
        "direct": "direct_assistant",
    })

    workflow.add_edge("rag_assistant", END)
    workflow.add_edge("direct_assistant", END)

    return workflow.compile()
