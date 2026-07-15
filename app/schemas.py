from pydantic import BaseModel, Field


class PromptRequest(BaseModel):
    prompt: str = Field(
        ...,
        min_length=1,
        description="User message sent to the LangGraph RAG agent",
        examples=["What is retrieval-augmented generation?"],
    )
