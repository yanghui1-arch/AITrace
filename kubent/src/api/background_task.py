from uuid import UUID
from typing import List
from openai.types.chat import ChatCompletionMessageParam
from src.repository.db.conn import AsyncSessionLocal
from src.repository import kubent_chat


async def add_chat(
    session_id:UUID,
    user_id:UUID,
    messages:List[ChatCompletionMessageParam]
):
    async with AsyncSessionLocal() as db:
        for message in messages:
            await kubent_chat.create_new_chat(
                db=db,
                session_id=session_id,
                user_id=user_id,
                role=message.get("role"),
                payload=message,
            )
            await db.commit()