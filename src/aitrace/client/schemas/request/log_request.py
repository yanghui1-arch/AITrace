from typing import List, Dict, Any
from pydantic import BaseModel

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
    usage: int | None