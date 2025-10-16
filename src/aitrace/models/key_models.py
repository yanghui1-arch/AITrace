from uuid import UUID
from enum import Enum
from datetime import datetime
from typing import Any, Dict, List
from dataclasses import dataclass, field

class StepType(Enum):
    CUSTOMIZED = 'customized'
    LLM_RESPONSE = 'llm_response'
    RETRIEVE = 'retrieve'
    TOOL = 'tool'

@dataclass
class Step:
    project_name: str
    name: str
    id: str | UUID
    trace_id: str | UUID
    parent_step_id: str | UUID | None = None
    type: StepType = StepType.CUSTOMIZED
    tags: List[str] = field(default_factory=list)
    input: Dict[str, Any] | None = None
    output: Any | None = None
    error_info: str | None = None
    model: str | None = None
    usage: int | None = None

@dataclass
class Track:
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

@dataclass
class Trace:
    project_name: str
    id: str | UUID | int
    conversation_id: str | UUID
    name: str
    model: str | None = None
    tags: List[str] = field(default_factory=list)
    input: Dict[str, Any] | None = None
    output: Any | None = None
    tracks: List[Track] | None = None
    error_info: str | None = None
    last_update_timestamp: datetime = field(default_factory=datetime.now)

    @property
    def usage(self) -> int:
        if self.tracks:
            return sum([track.usage for track in self.tracks if track.usage])
        return 0

@dataclass
class Conversation:
    project_name: str
    id: str | UUID
    name: str
    traces: List[Trace]
    start_time: datetime
    last_update_time: datetime
    tags: List[str] = field(default_factory=list)

    @property
    def usage(self):
        return sum([trace.usage for trace in self.traces])
