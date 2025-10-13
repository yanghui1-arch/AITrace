from enum import Enum
from typing import List, Literal
from dataclasses import dataclass
from ..models.key_models import StepType


@dataclass
class TrackerOptions:
    """ tracker options
    Controls how tracker tracks the llm input and output.
    
    Args:
        project_name(str): current work project name.
        tags(List[str] | None): tags of step or trace. Default to `None`.
        func_name(str | None): function name that caller set. Default to `None`. If caller doesn't
                                set name, it will be None.
        is_step(bool): whether track step. Default to `False`.
        is_trace(bool): whether track trace. Default to `False`.
        step_type(StepType | None): step type. Default to `None`. If is_step is `True` step_type has to be StepType.
        model(str | None): using model name. Default to `None`.
        step_name(str | None): step name. Default to `None`.
        trace_name(str | None): trace name. Default to `None`.
        track_llm_messages(Provider | List[Provider] | None): which provider to track llm messages. Default to `None`.
    """

    project_name: str
    tags: List[str] | None = None
    func_name: str | None = None
    is_step: bool = False
    is_trace: bool = False
    step_type: StepType | None = None
    model: str | None = None
    step_name: str | None = None
    trace_name: str | None = None
    track_llm_messages: "Provider" | List["Provider"] | None = None

class Provider(Enum):
    OPENAI = 'openai'
    GOOGLE = 'google'
    ANTHROPIC = 'anthropic'
    DEEPSEEK = 'deepseek'
    QWEN = 'qwen'
    OLLAMA = 'ollama'
