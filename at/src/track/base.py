from typing import Callable, Any, Tuple, Dict
from abc import ABC, abstractmethod
from dataclasses import dataclass
import functools

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

    trace_turn_on: bool
    record_turn_on: bool
    trace_inactivity_timeout: int | None = None
    func_name: str | None = None

class BaseTracker(ABC):
    """ Base tracker to track all output
    Every tracker should be extended `BaseTracker` class.
    Following methods need to be implemented in subclass.

    Args:
        provider(Optional[str]): provider name
    """

    def __init__(self):
        self.provider: str | None = None

    def track(
        self,
        func_name:Callable | str | None = None,
        project_name: str | None = None,
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
            trace_turn_on=trace_turn_on,
            record_turn_on=record_turn_on,
            trace_inactivity_timeout=trace_inactivity_timeout
        )
    
        if callable(func_name):
            func = func_name
            return self._decorator(func=func, tracker_options=tracker_options)
        
        tracker_options.func_name = func_name

        def decorator(func:Callable):
            return self._decorator(func=func)
        
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
                args=args,
                kwargs=kwargs
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
        args:Tuple,
        kwargs:Dict[str, Any]
    ):
        """ preparation for logging input before track function """
        print(f"_before_calling_function: {args}")

    def _after_calling_function(
        self,
        output:Any,
        error_info:str
    ):
        """ preparation for logging output after track function """
        print(f"_after_calling_function: {output}")
