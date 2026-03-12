


from pprint import pprint


from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from RAG import llm
from tools.retrieverTool import retriever_tool

llm_with_tools= llm.bind_tools([retriever_tool])

#Node
def assistant(state: MessagesState):
    from langgraph.graph import MessagesState
    return { "messages" : llm_with_tools.invoke(state["messages"])}



def agent():


    from RAG import llm

    llm_with_tools= llm.bind_tools([retriever_tool])
        #Build Graph

    Workflow = StateGraph(MessagesState)

    #Add Nodes
    Workflow.add_node("assistant", assistant)
    Workflow.add_node("tools", ToolNode([retriever_tool]))

    # Add Edges
    Workflow.add_edge(START, "assistant")
    Workflow.add_conditional_edges("assistant", tools_condition)
    Workflow.add_edge("tools", "assistant")


    #Compile the Graph
    graph= Workflow.compile()

    return graph

