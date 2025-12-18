from uuid import UUID
from fastapi import APIRouter, Header, Depends
from src.env import Env
from src.repository import kubent_chat_session
from src.repository.models import KubentChatSession
from src.repository.db.conn import get_db, AsyncSession
from src.api.schemas import ChatRequest, ChatResponse, ResponseModel
from src.api.jwt import verify_at_token
from src.agent.kubent import Kubent

chat_router = APIRouter(prefix="/chat", tags=["Chat"])

@chat_router.post(
    "/optimize", 
    description="Chat with Kubent to optimize the agent system.", 
    response_model=ResponseModel[ChatResponse],
)
async def optimize_agent_system(
    req:ChatRequest,
    user_id: UUID = Depends(verify_at_token),
    db:AsyncSession = Depends(get_db)
):
    message:str = req.message
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
    env = Env(env_name=f"optimize_{user_id}")
    kubent = Kubent(current_env=env)
    optimize_solution:str = kubent.run(question=message)
    return ResponseModel.success(data=ChatResponse(message=optimize_solution))
    
