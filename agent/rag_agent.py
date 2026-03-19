import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI

from rag.retriever_tool import retriever_tool

load_dotenv()

_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.9)
_llm_with_tools = _llm.bind_tools([retriever_tool])


def _assistant(state: MessagesState):
    return {"messages": _llm_with_tools.invoke(state["messages"])}


def agent():
    workflow = StateGraph(MessagesState)

    workflow.add_node("assistant", _assistant)
    workflow.add_node("tools", ToolNode([retriever_tool]))

    workflow.add_edge(START, "assistant")
    workflow.add_conditional_edges("assistant", tools_condition)
    workflow.add_edge("tools", "assistant")

    return workflow.compile()
