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
        if tracker_options.track_llm_messages:
            llm_inputs: Dict[str, Any] = inspect_helper.inspect_openai(func)
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
        output: Any,
        error_info: str | None,
        tracker_options: TrackerOptions,
    ) -> args_helper.EndArguments:
        ...