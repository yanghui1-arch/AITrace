from typing import override, Callable, Tuple, Dict, Any
from openai import Stream
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk
from .base import BaseTracker, TrackerOptions
from ..helper import args_helper, inspect_helper
from ..helper.llm import openai_helper

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
        llm_usage = None
        
        if output: 
            final_output['func_output'] = output
        else:
            final_output['func_output'] = None
        
        if tracker_options.track_llm:
            # stop trace any funcs first
            track_llm_func = inspect_helper.stop_trace_llm(func_name=func.__name__)
            if not isinstance(track_llm_func.output, Stream):
                llm_inputs = openai_helper.remove_chat_completion_input_fields(
                    openai_chat_completion_params=track_llm_func.inputs, 
                    ignore_fields=tracker_options.llm_ignore_fields
                )

                llm_outputs:openai_helper.FilteredFieldsOpenAIChatCompletionsOutput = openai_helper.remove_chat_completion_output_fields(
                    openai_chat_completion_output=track_llm_func.output, 
                    ignore_fields=tracker_options.llm_ignore_fields
                )

                llm_usage = llm_outputs.usage

                final_output['llm_outputs'] = llm_outputs.model_dump(exclude_none=True)
            else:
                final_output['llm_outputs'] = track_llm_func.output

        return args_helper.EndArguments(
            tags=tracker_options.tags,
            llm_input=llm_inputs,
            output=final_output,
            project_name=tracker_options.project_name,
            model=tracker_options.model,
            error_info=error_info,
            usage=llm_usage,
        )
