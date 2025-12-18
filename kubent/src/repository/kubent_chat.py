from typing import Dict, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from .models import KubentChat

async def create_new_chat(
    db: AsyncSession,
    session_id:UUID,
    user_id:UUID,
    role:str,
    payload:Dict[str, Any],
):
    chat = KubentChat(session_uuid=session_id, user_uuid=user_id, role=role, payload=payload)
    db.add(chat)
    await db.flush()
    return chat

async def select_chat(db: AsyncSession):
    ...
