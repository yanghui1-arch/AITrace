from uuid import UUID
from dataclasses import dataclass
from typing import Optional, Any, List, Dict

from . import id_helper
from ..models import Step, Trace, StepType, Track
from .. import context

@dataclass
class BaseArguments:
    def to_kwargs(self, ignore_keys: Optional[List[str]] = None) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        ignore_keys = [] if ignore_keys is None else ignore_keys
        for key, value in self.__dict__.items():
            if (value is not None) and (key not in ignore_keys):
                result[key] = value

        return result

@dataclass
class StartArguments(BaseArguments):

    func_name: str
    tags: List[str] | None = None
    input: Dict[str, Any] | None = None
    project_name: str | None = None
    model: str | None = None
    usage: int | None = None

@dataclass
class EndArguments(BaseArguments):

    tags: List[str] | None = None
    input: Dict[str, Any] | None = None
    output: Dict[str, Any] | None = None
    project_name: str | None = None
    model: str | None = None
    error_info: str | None = None
    usage: int | None = None

def create_new_step(
    project_name: str,
    input: Any | None = None,
    output: Dict[str, Any] | None = None,
    name: str | None = None,
    type: StepType = StepType.CUSTOMIZED,
    tags: List[str] | None = None,
    model: str | None = None,
    usage: int | None = None,
    error_info: str | None = None,
    step_id: str | UUID | int | None = None,
    trace_id: str | UUID | int | None = None,
    parent_step_id: str | UUID | int | None = None,
    **kwargs
) -> Step:
    """create a new step data
    If not pass a parent step id, context will try to get the top step and make the top step id as new step parent id.

    Args:
        project_name(str): project name.
        input(Any | None): input of module. Default to `None`. None means it's logging output.
        output(Dict[str, Any] | None): output of module. Default to `None`. None means it's logging input.
        name(str | None): the step name. Caller can set the name to define what the step role is. Default to ``None`. If it's None,
                                        AITrace will set step name based on step type.
        type(StepType): step type. Default to `StepType.CUSTOMIZED`.
        tags(List[str] | None): step tags. Default to `None`. If it's None, it will be set an empty list.
        model(str | None): model name. Probably using a llm model in the step. Default to `None`.
        usage(int | None): llm token usage. Default to `None`.
        error_info(str | None): error information while occuring errors. Default to `None`.
        step_id(str | UUID | int | None): step id offered by caller. Default to `None`. If it's None, create a new uuid7 for step.
        trace_id(str | UUID | int | None): trace id which the step belongs to. Default to `None`. If it's None, the step
                                            will be thought as belongs to a new trace and AITrace will create a new uuid7 for the
                                            new trace.
        parent_step_id(str | UUID | int | None): parent step id of this step data. Default to `None`.

    Returns:
        Step: step creation
    """

    if step_id is None:
        step_id = id_helper.generate_id()
    if trace_id is None:
        trace_id = id_helper.generate_id()
    if name is None:
        name = type.value
    if tags is None:
        tags = []

    # if input is not Dict type -> transfer it to a Dict type.
    if input is not None and isinstance(input, Dict) is False:
        input = {"input": input}
    
    # process parent step id
    if not parent_step_id:
        parent_step: Step | None = context.get_storage_top_step_data()
        parent_step_id: str | None = parent_step.id if parent_step else None

    step = Step(
        project_name=project_name,
        name=name,
        id=step_id,
        trace_id=trace_id,
        parent_step_id=parent_step_id,
        type=type,
        tags=tags,
        input=input,
        output=output,
        error_info=error_info,
        model=model,
        usage=usage,
    )
    
    return step


def create_new_trace(
    project_name: str,
    input: Dict[str, Any] | None = None,
    output: Dict[str, Any] | None = None,
    tracks: List[Track] | None = None,
    name: str | None = None,
    tags: List[str] | None = None,
    error_info: str | None = None,
    model: str | None = None,
    trace_id: str | UUID | int | None = None,
    conversation_id: str | UUID | int | None = None,
    **kwargs
) -> Trace:
    """Create a new trace data
    
    Args:
        project_name(str): project name.
        input(Dict[str, Any] | None): User input. Default to `None`. If it's None, it's logging output.
        output(Dict[str, Any] | None): agent final output. Default to `None`. If it's None, it's logging input.
        tracks(List[Track] | None): a list of execution tracks. Default to `None`. Maybe it's an easy question so that it doesn't include any track.
        name(str | None): trace name. It defines what the trace does or its topic. Default to `None`. If it's None, it will be set using input user content.
        tags(List[str] | None): step tags. Default to `None`. If it's None, it will be set an empty list.
        error_info(str | None): error information while tracking trace. Default to `None`.
        model(str | None): model name. Which model agent using. Default to `None`.
        trace_id(str | UUID | int | None): trace id. Default to `None`. If it's None, it will be thought as a new trace and create a new id for the trace.
        conversation_id(str | UUID | int | None): conversation id which the trace belongs to. Default to `None`. If it's None, it will be thought as a new
                                                    conversation and create a new id for the new conversation.
    
    Returns:
        Trace: trace creation
    """
    
    if trace_id is None:
        trace_id = id_helper.generate_id()
    if conversation_id is None:
        conversation_id = id_helper.generate_id()
    if name is None:
        name = input['user']
    if tags is None:
        tags = []

    trace = Trace(
        project_name=project_name,
        id=trace_id,
        conversation_id=conversation_id,
        name=name,
        model=model,
        tags=tags,
        input=input,
        output=output,
        tracks=tracks,
        error_info=error_info
    )

    return trace
