from uuid import UUID
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import KubentChatSession

async def create_new_chat_session(
    db: AsyncSession,
    user_uuid: UUID,
    topic: str | None,
    total_tokens: int | None,
) -> KubentChatSession:
    session = KubentChatSession(
        user_uuid=user_uuid,
        topic=topic,
        total_tokens=total_tokens,
    )
    db.add(session)
    await db.flush()
    return session

async def select_chat_session_by_id(
    db: AsyncSession,
    session_id: UUID,
) -> KubentChatSession | None:
    stmt = select(KubentChatSession).where(
        KubentChatSession.id == session_id
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def select_chat_session_by_user_id(
    db: AsyncSession,
    user_id: UUID,
    limit: int = 20,
) -> List[KubentChatSession]:
    """Select all chat sessions with Kubent by user uuid.
    
    Args:
        db(AsyncSession): db connection
        user_id(UUID): user id
        limit(int): search limits. Default to `20`
    Return:
        List[KubentChatSession]: a list of chat session with Kubent.
    """
    stmt = select(KubentChatSession).where(
        KubentChatSession.user_uuid == user_id
    ).limit(limit=limit)
    result = await db.execute(stmt)
    return result.scalars().all()
