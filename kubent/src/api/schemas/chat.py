from typing import Literal
from pydantic import BaseModel

class ChatRequest(BaseModel):
    session_id: str | None
    message: str

class ChatResponse(BaseModel):
    message: str