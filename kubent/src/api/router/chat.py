from uuid import UUID
from typing import List
from fastapi import APIRouter, BackgroundTasks, Depends
from openai.types.chat import ChatCompletionMessageParam
from src.env import Env
from src.repository import kubent_chat_session, kubent_chat
from src.repository.models import KubentChatSession, KubentChat
from src.repository.db.conn import get_db, AsyncSession
from src.api.schemas import ChatRequest, ChatResponse, ResponseModel
from src.api.jwt import verify_at_token
from src.agent.kubent import Kubent, Result
from src.api.background_task import add_chat

chat_router = APIRouter(prefix="/chat", tags=["Chat"])

@chat_router.post(
    "/optimize", 
    description="Chat with Kubent to optimize the agent system.", 
    response_model=ResponseModel[ChatResponse],
)
async def optimize_agent_system(
    req:ChatRequest,
    background_task:BackgroundTasks,
    user_id: UUID = Depends(verify_at_token),
    db:AsyncSession = Depends(get_db)
):
    message:str = req.message
    chat_hist:List[ChatCompletionMessageParam]|None = None
    if not req.session_id:
        chat_session:KubentChatSession = await kubent_chat_session.create_new_chat_session(
            db=db, 
            user_uuid=user_id,
            topic=None, 
            total_tokens=None
        )
        await db.commit()
        session_id = chat_session.id
    else:
        session_id = UUID(req.session_id)
        chats:List[KubentChat] = await kubent_chat.select_chat(db=db, session_id=session_id)
        chat_hist = [chat.payload for chat in chats]

    env = Env(env_name=f"optimize_{user_id}")
    kubent = Kubent(current_env=env)
    kubent_result:Result = kubent.run(question=message, chat_hist=chat_hist)
    optimize_solution:str = kubent_result.answer
    background_task.add_task(add_chat, session_id=session_id, user_id=user_id, messages=kubent_result.chats)
    return ResponseModel.success(data=ChatResponse(message=optimize_solution))
    
