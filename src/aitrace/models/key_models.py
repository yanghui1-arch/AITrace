from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
from typing import Any, Dict, List

class StepType(Enum):
    CUSTOMIZED = 'customized'
    LLM_RESPONSE = 'llm_response'
    RETRIEVE = 'retrieve'
    TOOL = 'tool'

class Step(BaseModel):
    project_name: str
    name: str
    id: str
    trace_id: str
    parent_step_id: str | None = None
    type: StepType = StepType.CUSTOMIZED
    tags: List[str] = Field(default_factory=list)
    input: Dict[str, Any] | None = None
    output: Any | None = None
    error_info: str | None = None
    model: str | None = None
    usage: int | None = None

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
    def usage(self) -> int | None:
        return self._step.usage

class Trace(BaseModel):
    project_name: str
    id: str
    conversation_id: str
    name: str
    model: str | None = None
    tags: List[str] = Field(default_factory=list)
    input: Dict[str, Any] | None = None
    output: Any | None = None
    tracks: List[Track] | None = None
    error_info: str | None = None
    last_update_timestamp: datetime = Field(default_factory=datetime.now)

    @property
    def usage(self) -> int:
        if self.tracks:
            return sum([track.usage for track in self.tracks if track.usage])
        return 0

class Conversation(BaseModel):
    project_name: str
    id: str
    name: str
    traces: List[Trace]
    start_time: datetime
    last_update_time: datetime
    tags: List[str] = Field(default_factory=list)

    @property
    def usage(self):
        return sum([trace.usage for trace in self.traces])
