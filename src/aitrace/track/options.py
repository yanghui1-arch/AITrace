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
        step_type(StepType | None): step type. Default to `None`.
        model(str | None): using model name. Default to `None`.
        step_name(str | None): step name. Default to `None`.
        trace_name(str | None): trace name. Default to `None`.
        track_llm(Provider | List[Provider] | None): track a certain llm. Default to `None`. 
                                                    If `track_llm` is not `None`, AITrace will track provider's api. 
    """

    project_name: str
    tags: List[str] | None = None
    func_name: str | None = None
    step_type: StepType | None = None
    model: str | None = None
    step_name: str | None = None
    trace_name: str | None = None
    track_llm: "Provider" | List["Provider"] | None = None

class Provider(Enum):
    OPENAI = 'openai'
    GOOGLE = 'google'
    ANTHROPIC = 'anthropic'
    DEEPSEEK = 'deepseek'
    QWEN = 'qwen'
    OLLAMA = 'ollama'
