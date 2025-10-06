from typing import Callable, Any, Tuple, Dict, List
from abc import ABC, abstractmethod
from dataclasses import dataclass
import functools

from ..models import Trace, Record
from ..helper import args_helper
from ..handler.log_handler import (
    log_input_as_record,
    log_input_as_trace,
    log_output_as_record,
    log_output_as_trace
)

@dataclass
class TrackerOptions:
    """ tracker options
    Controls how tracker tracks the llm input and output.
    
    Args:
        trace_turn_on(bool): whether log trace
        record_turn_on(bool): whether log record
        trace_inactivity_timeout(int|None): how long the trace is active. It belongs to the same trace when the previous is the same if it's None.
        func_name(str|None): function name. Default to None.
    """

    project_name: str
    tags: List[str] | None = None
    trace_turn_on: bool
    record_turn_on: bool
    trace_inactivity_timeout: int | None = None
    func_name: str | None = None

class BaseTracker(ABC):
    """ Base tracker to track all output
    Every tracker should be extended `BaseTracker` class.
    Following methods need to be implemented in subclass.
        * _before_calling_function: log trace & record according to tracker_options before calling function.
        * _after_calling_function : log trace & record & error information according to tracker_options after calling function.

    Args:
        provider(Optional[str]): provider name
    """

    def __init__(self):
        self.provider: str | None = None

    def track(
        self,
        func_name:Callable | str | None = None,
        project_name: str | None = None,
        tags: List[str] | None = None,
        trace_turn_on: bool = True,
        record_turn_on: bool = True,
        trace_inactivity_timeout: int | None = 600,
    ) -> Callable:
        """ track decorator

        Args:
            func_name(Callable|str|None): function name. Default to None.
            project_name(Optional[str]): project name to be tracked. Default to None.
        
        Returns:
            Callable: a decorator
        """

        if project_name is None:
            # post a request to get caller project list
            # if caller has `default project` name project, create a project named like default project - 2 
            project_name = "Default project"

        tracker_options = TrackerOptions(
            project_name=project_name,
            tags=tags,
            trace_turn_on=trace_turn_on,
            record_turn_on=record_turn_on,
            trace_inactivity_timeout=trace_inactivity_timeout
        )
    
        if callable(func_name):
            func = func_name
            return self._decorator(func=func, tracker_options=tracker_options)
        
        tracker_options.func_name = func_name

        def decorator(func:Callable):
            return self._decorator(func=func, tracker_options=tracker_options)
        
        return decorator
    
    def _decorator(
        self,
        func: Callable,
        tracker_options: TrackerOptions
    ) -> Callable:
        """ construct a decorator 
        
        Args:
            func(Callable): a callable function
            tracker_options(TrackerOptions): tracker options
        
        Returns:
            Callable: track decorator
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            result = None
            func_exception: Exception | None = None
            error_info: str | None = None
            # before track
            self._before_calling_function(
                func=func,
                tracker_options=tracker_options,
                args=args,
                kwargs=kwargs,
            )

            try:
                result = func(*args, **kwargs)
            except Exception as e:
                error_info = str(e)
                func_exception = e
            finally:
                # after track
                self._after_calling_function(output=result, error_info=error_info)
                if func_exception is not None:
                    raise func_exception
                else:
                    return result

        return wrapper

    def _before_calling_function(
        self,
        func:Callable,
        tracker_options: TrackerOptions | None,
        args:Tuple,
        kwargs:Dict[str, Any]
    ):
        """ prepare and log input before track function 
        Default to log input as trace.
        """
        
        try:
            start_arguments = self.start_inputs_args_preprocess(
                func=func,
                tracker_options=tracker_options,
                args=args,
                kwargs=kwargs
            )
        
        except Exception as exception:
            print(str(exception))
            
            start_arguments = args_helper.StartArguments(
                func_name=func.__name__,
                tags=tracker_options.tags,
                project_name=tracker_options.project_name
            )

        if tracker_options is None:
            # default to turn on trace
            log_input_as_trace(start_args=start_arguments)
        
        else:
            if tracker_options.record_turn_on and tracker_options.trace_turn_on:
                log_input_as_trace(start_args=start_arguments)
                log_input_as_record(start_args=start_arguments)

            elif tracker_options.record_turn_on:
                log_input_as_record(start_args=start_arguments)

            elif tracker_options.trace_turn_on:
                log_input_as_trace(start_args=start_arguments)

            else:
                raise ValueError("Please set your tracker options at least one of `record_turn_on` and `trace_turn_on` is True.")
        

    @abstractmethod
    def _after_calling_function(
        self,
        output:Any,
        error_info:str
    ):
        """ prepare and log output after track function """
        ...


    @abstractmethod
    def start_inputs_args_preprocess(
        self,
        func: Callable,
        tracker_options: TrackerOptions | None,
        args: Tuple,
        kwargs: Dict[str, Any]
    ):
        ...
