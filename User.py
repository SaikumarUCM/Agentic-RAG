
from langchain_core.messages import HumanMessage
from agent import agent

def User(prompt: str):
    messages = {
        "messages": HumanMessage(content=prompt)
    }

    graph = agent()
    response = graph.invoke(messages)

    return response['messages'][1].content