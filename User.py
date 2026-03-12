
from langchain_core.messages import HumanMessage
from agent import agent

messages = {
    "messages": HumanMessage(content=" what is task decomposition in the context of AI agents?")
}

graph = agent()
response = graph.invoke(messages)

for message in response["messages"]:
    message.pretty_print()