from typing import Any, Dict, List
from uuid import UUID
from ..models.key_models import StepType
from ..models.key_models import Step, Trace, Track

class AITrace:

    def __init__(self):
        pass

    def track_step(
        self,
        input: Any,
        output: Any,
        type: StepType = StepType.CUSTOMIZED,
        error_info: str | None = None,
        step_id: str | UUID | int | None = None,
        trace_id: str | UUID | int | None = None,
        **kwargs
    ) -> Step:
        """track step
        Track every agent step in calling module.

        Args:
            input(Any): input of module.
            output(Any): output of module. Probably None
            error_info(str | None): error information while occuring errors. Default to `None`.
            step_id(str | UUID | int | None): step id offered by caller. Default to `None`. If it's None, create a new uuid7 for step.
            trace_id(str | UUID | int | None): trace id which the step belongs to. Default to `None`. If it's None, the step
                                                will be thought as belongs to a new trace and AITrace will create a new uuid7 for the
                                                new trace.

        Returns:
            Step: step creation
        """
        pass

    def track_trace(
        self,
        input: Dict[str, Any],
        output: Dict[str, Any],
        tracks: List[Track] | None = None,
        error_info: str | None = None,
        trace_id: str | UUID | int | None = None,
        conversation_id: str | UUID | int | None = None,
        **kwargs
    ) -> Trace:
        """track trace
        Track trace after calling an agent execution.
        The design of track trace is to track a single complete agent execution process.
        For example:
            user ask one question and the agent will `think-action-observation` again and again to response rightly.
            Track trace is to track the progress of agent execution.
        
        Args:
            input(Dict[str, Any]): User input.
            output(Dict[str, Any]): agent final output.
            tracks(List[Track] | None): a list of execution tracks. Default to `None`. Maybe it's an easy question so that it doesn't include any track.
            error_info(str | None): error information while tracking trace. Default to `None`.
            trace_id(str | UUID | int | None): trace id. Default to `None`. If it's None, it will be thought as a new trace and create a new id for the trace.
            conversation_id(str | UUID | int | None): conversation id which the trace belongs to. Default to `None`. If it's None, it will be thought as a new
                                                        conversation and create a new id for the new conversation.

        Returns:
            Trace: trace creation
        """
        pass


at_client = AITrace()
