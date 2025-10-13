from typing import Callable, Tuple, Dict, Any
from .base import BaseTracker, TrackerOptions

class AITraceTracker(BaseTracker):
    
    def start_inputs_args_preprocess(
        self,
        func: Callable,
        tracker_options: TrackerOptions | None,
        args: Tuple,
        kwargs: Dict[str, Any]
    ):
        ...

    def end_output_exception_preprocess(
        self,
        output: Any,
        error_info: str | None,
        tracker_options: TrackerOptions,
    ):
        ...