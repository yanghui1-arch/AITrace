from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from ..jwt import verify_at_token
from ..schemas.response import ResponseModel
from ..schemas.query import QueryKubentChatSession
from ...repository import kubent_chat_session
from ...repository.db.conn import get_db
from ...repository.models.kubent_chat_session import KubentChatSession

query_router = APIRouter(prefix="/query")

@query_router.get("/session")
async def query_session(
    user_id: UUID = Depends(verify_at_token),
    db:AsyncSession = Depends(get_db)
):
    """Get query that user chat session with Kubent"""
    try:
        chat_sessions:List[KubentChatSession] = await kubent_chat_session.select_chat_session_by_user_id(db=db, user_id=user_id)
        query_chat_sessions:List[QueryKubentChatSession] = [
            QueryKubentChatSession(
                id=session.id, 
                user_uuid=session.user_uuid,
                topic=session.topic,
                last_update_timestamp=session.last_update_timestamp
            ) for session in chat_sessions
        ]
        return ResponseModel.success(data=query_chat_sessions)
    except Exception as exce:
        return ResponseModel.error(exce)