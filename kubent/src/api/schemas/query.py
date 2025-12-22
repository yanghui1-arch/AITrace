from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class QueryKubentChatSession(BaseModel):
    id: UUID
    user_uuid: UUID
    topic: str | None
    last_update_timestamp: datetime