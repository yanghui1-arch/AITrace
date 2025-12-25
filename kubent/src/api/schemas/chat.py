from typing import Literal
from pydantic import BaseModel

class ChatRequest(BaseModel):
    session_id: str | None
    message: str
    project_id: int | None

class ChatResponse(BaseModel):
    message: str

class ChatSessionTitleRequest(BaseModel):
    message: str
    session_id: str