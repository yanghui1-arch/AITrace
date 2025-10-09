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