from typing import Literal, Any, Dict, List
from uuid import UUID
from ..models.key_models import StepType
from ..models.key_models import Step, Trace, Track
from ..helper import id_helper

class AITrace:

    def __init__(self):
        pass

    def track_step(
        self,
        project_name: str,
        input: Any | None = None,
        output: Any | None = None,
        name: str | None = None,
        type: StepType = StepType.CUSTOMIZED,
        tags: List[str] | None = None,
        model: str | None = None,
        error_info: str | None = None,
        step_id: str | UUID | int | None = None,
        trace_id: str | UUID | int | None = None,
        **kwargs
    ) -> Step:
        """track step and log step.
        Track every agent step in calling module.

        Args:
            project_name(str): project name.
            input(Any | None): input of module. Default to `None`. None means it's logging output.
            output(Any | None): output of module. Default to `None`. None means it's logging input.
            name(str | None): the step name. Caller can set the name to define what the step role is. Default to ``None`. If it's None,
                                            AITrace will set step name based on step type.
            type(StepType): step type. Default to `StepType.CUSTOMIZED`.
            tags(List[str] | None): step tags. Default to `None`. If it's None, it will be set an empty list.
            model(str | None): model name. Probably using a llm model in the step. Default to `None`.
            error_info(str | None): error information while occuring errors. Default to `None`.
            step_id(str | UUID | int | None): step id offered by caller. Default to `None`. If it's None, create a new uuid7 for step.
            trace_id(str | UUID | int | None): trace id which the step belongs to. Default to `None`. If it's None, the step
                                                will be thought as belongs to a new trace and AITrace will create a new uuid7 for the
                                                new trace.

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

        # if input is not Dict type -> transfer it as a Dict type.
        if isinstance(input, Dict) is False:
            input = {"input": input}

        step = Step(
            project_name=project_name,
            name=name,
            id=step_id,
            trace_id=trace_id,
            type=type,
            tags=tags,
            input=input,
            output=output,
            error_info=error_info,
            model=model
        )

        return step

    def track_trace(
        self,
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
        """track trace and log trace.
        Track trace after calling an agent execution.
        The design of track trace is to track a single complete agent execution process.
        For example:
            user ask one question and the agent will `think-action-observation` again and again to response rightly.
            Track trace is to track the progress of agent execution.
        
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


at_client = AITrace()
