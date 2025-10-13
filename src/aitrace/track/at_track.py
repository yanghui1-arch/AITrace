from typing import override, Callable, Tuple, Dict, Any
from .base import BaseTracker, TrackerOptions
from ..helper import args_helper, inspect_helper

class AITraceTracker(BaseTracker):
    
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
        # track passing llm messages
        if tracker_options.track_llm:
            llm_inputs: Dict[str, Any] = inspect_helper.inspect_llm_inputs(func=func, provider=tracker_options.track_llm)
            inputs: Dict[str, Dict[str, Any]] = {
                "llm_inputs": llm_inputs,
                "func_inputs": inputs,
            }

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
        if output and isinstance(output, Dict) is False:
            final_output['output'] = output
        
        if tracker_options.track_llm:
            llm_outputs: Dict[str, Any] = inspect_helper.inspect_llm_outputs(func=func, provider=tracker_options.track_llm)
            final_output['llm_outputs'] = llm_outputs

        return args_helper.EndArguments(
            tags=tracker_options.tags,
            output=final_output,
            project_name=tracker_options.project_name,
            model=tracker_options.model,
            error_info=error_info
        )
