from fastapi import FastAPI
from langchain_core.messages import HumanMessage

from agent import agent
from rag.ingestor import ingest_url
from app.schemas import PromptRequest

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello, World!"}


@app.post("/chat")
def chat(request: PromptRequest):
    if request.url:
        ingest_url(request.url)

    graph = agent()
    print(request.prompt)
    response = graph.invoke({"messages": HumanMessage(content=request.prompt)})
    return {"response": response["messages"][-1].content}
