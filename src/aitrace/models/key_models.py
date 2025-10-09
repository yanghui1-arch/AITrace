from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from typing import Any, Dict, List

class StepType(Enum):
    CUSTOMIZED = 'customized'
    LLM_RESPONSE = 'llm_response'
    RETRIEVE = 'retrieve'
    TOOL = 'tool'

@dataclass
class Step:
    project_name: str
    name: str
    id: str
    trace_id: str
    type: StepType = StepType.CUSTOMIZED
    tags: List[str] = []
    input: Dict[str, Any] | None = None
    output: Any | None = None
    error_info: str | None = None
    model: str | None = None

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
    
@dataclass
class Trace:
    project_name: str
    id: str
    conversation_id: str
    name: str
    model: str | None = None
    tags: List[str] = []
    input: Dict[str, Any]
    output: Any | None = None
    tracks: List[Track] | None = None
    error_info: str | None = None

@dataclass
class Conversation:
    project_name: str
    id: str
    name: str
    tags: List[str]
    traces: List[Trace]
    start_time: datetime
    last_update_time: datetime
