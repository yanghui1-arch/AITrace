from fastapi import APIRouter
from .chat import chat_router

api_router = APIRouter(prefix="/kubent/api")
api_router.include_router(router=chat_router)

__all__ = [
    "api_router"
]