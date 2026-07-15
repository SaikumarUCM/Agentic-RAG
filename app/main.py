import json
from pathlib import Path

import yaml
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage, AIMessageChunk

from agent import agent
from app.schemas import PromptRequest

app = FastAPI(
    title="Agentic RAG API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)
_graph = agent()
_OPENAPI_PATH = Path(__file__).with_name("openapi.yaml")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    with _OPENAPI_PATH.open(encoding="utf-8") as f:
        app.openapi_schema = yaml.safe_load(f)
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/")
def root():
    return {"message": "Hello, World!"}


@app.post("/chat")
def chat(request: PromptRequest):
    def token_stream():
        for chunk, _ in _graph.stream(
            {"messages": [HumanMessage(content=request.prompt)]},
            stream_mode="messages",
        ):
            if isinstance(chunk, AIMessageChunk) and chunk.content:
                yield f"data: {json.dumps({'token': chunk.content})}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(token_stream(), media_type="text/event-stream")
