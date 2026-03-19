from typing import Optional
from pydantic import BaseModel


class PromptRequest(BaseModel):
    prompt: str
    url: Optional[str] = None
