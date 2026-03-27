from fastapi import FastAPI
from langchain_core.messages import HumanMessage

from agent import agent
from app.schemas import PromptRequest

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello, World!"}


@app.post("/chat")
def chat(request: PromptRequest):
    graph = agent()
    response = graph.invoke({"messages": [HumanMessage(content=request.prompt)]})
    return {"response": response["messages"][-1].content}
