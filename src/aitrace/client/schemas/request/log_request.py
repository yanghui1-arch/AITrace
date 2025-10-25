from datetime import datetime
from typing import List, Dict, Any
from pydantic import BaseModel, field_serializer
from openai.types.completion_usage import CompletionUsage
from ....models import Track
from ....helper import serialize_helper

class LogStepRequest(BaseModel):
    project_name: str
    step_name: str
    step_id: str
    trace_id: str
    parent_step_id: str | None
    step_type: str
    tags: List[str]
    input: Dict[str, Any] | None
    output: Any | None
    error_info: str | None
    model: str | None
    usage: CompletionUsage | None

    @field_serializer('input', 'output')
    def serialize_any_field(self, value: Any):
        return serialize_helper.safe_serialize(value)

class LogTraceRequest(BaseModel):
    project_name: str
    trace_name: str
    trace_id: str
    conversation_id: str
    tags: List[str]
    input: Dict[str, Any] | None
    output: Dict[str, Any] | None
    tracks: List[Track] | None
    error_info: str | None
    model: str | None
    last_update_timestamp: datetime

    @field_serializer('input', 'output')
    def serialize_any_field(self, value: Any):
        return serialize_helper.safe_serialize(value)