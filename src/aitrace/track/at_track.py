from typing import override, Callable, Tuple, Dict, Any
from .base import BaseTracker, TrackerOptions
from ..helper import args_helper, inspect_helper

class AITraceTracker(BaseTracker):
    """AITraceTracker is to track the agent inputs and outputs"""
    
    def __init__(self):
        super().__init__()
        # store and restore calling llm stacks to track llm inputs and outputs.
        self._llm_track_frames = []
    
    @override
    def start_inputs_args_preprocess(
        self,
        func: Callable,
        tracker_options: TrackerOptions | None,
        args: Tuple,
        kwargs: Dict[str, Any]
    ) -> args_helper.StartArguments:
        
        inputs: Dict[str, Any] = inspect_helper.parse_to_dict_input(
            func=func,
            args=args,
            kwargs=kwargs
        )
        # set sys.settrace
        if tracker_options.track_llm:
            inspect_helper.start_trace_llm(func_name=func.__name__, provider=tracker_options.track_llm)

        return args_helper.StartArguments(
            func_name=func.__name__,
            tags=tracker_options.tags,
            input=inputs,
            project_name=tracker_options.project_name,
            model=tracker_options.model,
        )

    @override
    def end_output_exception_preprocess(
        self,
        func:Callable,
        output: Any | None,
        error_info: str | None,
        tracker_options: TrackerOptions,
    ) -> args_helper.EndArguments:
        
        final_output = {}
        llm_inputs = None
        
        # TODO: fix final_output is an empty dictionary if output is a Dict
        if output and isinstance(output, Dict) is False:
            final_output['output'] = output
        
        if tracker_options.track_llm:
            # stop trace any funcs first
            track_llm_func = inspect_helper.stop_trace_llm()

            llm_inputs: Dict[str, Any] = track_llm_func.inputs
            llm_outputs: Dict[str, Any] = track_llm_func.output
            final_output['llm_outputs'] = llm_outputs

        return args_helper.EndArguments(
            tags=tracker_options.tags,
            llm_input=llm_inputs,
            output=final_output,
            project_name=tracker_options.project_name,
            model=tracker_options.model,
            error_info=error_info
        )
