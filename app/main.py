import json

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage, AIMessageChunk

from agent import agent
from app.schemas import PromptRequest

app = FastAPI()
_graph = agent()


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
