from uuid import UUID
from typing import List
from fastapi import APIRouter, BackgroundTasks, Depends
from openai.types.chat import ChatCompletionMessageParam
from src.env import Env
from src.repository import (
    step,
    trace,
    kubent_chat,
    kubent_chat_session,
)
from src.repository.models import (
    Step,
    KubentChatSession,
    KubentChat,
)
from src.repository.db.conn import get_db, AsyncSession
from src.api.schemas import ChatRequest, ChatResponse, ResponseModel
from src.api.jwt import verify_at_token
from src.api.background_task import add_chat
from src.utils import mermaid
from src.agent.kubent import Kubent, Result

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
            title=None, 
            total_tokens=None
        )
        await db.commit()
        session_id = chat_session.id
    else:
        session_id = UUID(req.session_id)
        chats:List[KubentChat] = await kubent_chat.select_chat(db=db, session_id=session_id)
        chat_hist = [chat.payload for chat in chats]

    if req.project_id:
        # Get some project's traces and then push them to kubent to analyze.
        traces_id: List[UUID] = await trace.select_latest_traces_id_by_project_id(db=db, project_id=req.project_id)
        steps_in_traces: List[List[Step]] = [await step.select_steps_by_trace_id(db=db, trace_id=trace_id) for trace_id in traces_id]
        exec_graphs: List[str] = [mermaid.steps_to_mermaid(steps=steps) for steps in steps_in_traces]

    env = Env(env_name=f"optimize_{user_id}")
    kubent = Kubent(current_env=env)
    kubent_result:Result = kubent.run(question=message, chat_hist=chat_hist, agent_workflows=exec_graphs)
    optimize_solution:str = kubent_result.answer
    background_task.add_task(add_chat, session_id=session_id, user_id=user_id, messages=kubent_result.chats)
    return ResponseModel.success(data=ChatResponse(message=optimize_solution))
    
