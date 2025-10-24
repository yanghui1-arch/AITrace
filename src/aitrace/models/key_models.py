from uuid import UUID
from enum import Enum
from datetime import datetime
from typing import Any, Dict, List
from pydantic import BaseModel, Field
from openai.types.completion_usage import CompletionUsage

class StepType(Enum):
    CUSTOMIZED = 'customized'
    LLM_RESPONSE = 'llm_response'
    RETRIEVE = 'retrieve'
    TOOL = 'tool'

class Step(BaseModel):
    project_name: str
    name: str
    id: str | UUID
    trace_id: str | UUID
    parent_step_id: str | UUID | None = None
    type: StepType = StepType.CUSTOMIZED
    tags: List[str] = Field(default_factory=list)
    input: Dict[str, Any] | None = None
    output: Any | None = None
    error_info: str | None = None
    model: str | None = None
    usage: CompletionUsage | None = None

class Track(BaseModel):
    _step: Step
    call_timestamp: datetime

    @property
    def step(self):
        return self._step
    
    @property
    def project_name(self):
        return self._step.project_name
    
    @property
    def usage(self) -> CompletionUsage | None:
        return self._step.usage

class Trace(BaseModel):
    project_name: str
    id: str | UUID | int
    conversation_id: str | UUID
    name: str
    model: str | None = None
    tags: List[str] = Field(default_factory=list)
    input: Dict[str, Any] | None = None
    output: Any | None = None
    tracks: List[Track] | None = None
    error_info: str | None = None
    last_update_timestamp: datetime = Field(default_factory=datetime.now)

class Conversation(BaseModel):
    project_name: str
    id: str | UUID
    name: str
    traces: List[Trace]
    start_time: datetime
    last_update_time: datetime
    tags: List[str] = Field(default_factory=list)
