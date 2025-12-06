from typing import Literal, List
from pydantic import BaseModel
from openai.types.completion_usage import CompletionUsage
from openai.types.chat import ChatCompletionAudio

class Function(BaseModel):
    name: str
    arguments: str

class ToolFunctionCall(BaseModel):
    id: int
    function: Function

class PatchStreamResponse(BaseModel):
    """Patch stream standard response"""
    role: Literal['assistant', 'tool']
    content: str
    tool_calls: List[ToolFunctionCall] | None = None
    audio: ChatCompletionAudio | None = None
    usage: CompletionUsage | None = None