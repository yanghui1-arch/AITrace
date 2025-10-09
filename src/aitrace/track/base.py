from typing import Callable, Any, Tuple, Dict, List
from abc import ABC, abstractmethod
from dataclasses import dataclass
import functools

from ..models.key_models import StepType
from ..helper import args_helper, inspect_helper
from ..core.aitrace import at_client

@dataclass
class TrackerOptions:
    """ tracker options
    Controls how tracker tracks the llm input and output.
    
    Args:
        project_name(str): current work project name.
        tags(List[str] | None): tags of step or trace. Default to `None`.
        func_name(str | None): function name that caller set. Default to `None`. If caller doesn't
                                set name, it will be None.
        is_step(bool): whether track step. Default to `False`.
        is_trace(bool): whether track trace. Default to `False`.
        step_type(StepType | None): step type. Default to `None`. If is_step is `True` step_type has to be StepType.
        model(str | None): using model name. Default to `None`.
        step_name(str | None): step name. Default to `None`.
        trace_name(str | None): trace name. Default to `None`.
    """

    project_name: str
    tags: List[str] | None = None
    func_name: str | None = None
    is_step: bool = False
    is_trace: bool = False
    step_type: StepType | None = None
    model: str | None = None
    step_name: str | None = None
    trace_name: str | None = None

class BaseTracker(ABC):
    """ Base tracker to track all output
    Every tracker should be extended `BaseTracker` class.
    Following methods need to be implemented in subclass.
        * start_inputs_args_preprocess: preprocess start input before calling function

    Args:
        provider(Optional[str]): provider name
    """

    def __init__(self):
        self.provider: str | None = None
 
    def track_step(
        self,
        func_name: str | Callable,
        project_name: str,
        tags: List[str] | None = None,
        step_type: StepType = StepType.CUSTOMIZED,
        step_name: str | None = None,
        model: str | None = None,
    ) -> Callable:
        """track step decorator
        Track step in calling modules. If use decorator to track step, the step and the trace id will be always a whole new ones.
        In other words, you cannot set the step id and its belonging trace id. It's recommended to be used in a simple demo.

        Args:
            func_name(str | Callable): caller can set it they want to name with 'str' type. If caller doesn't set, it will be `Callable`.
            project_name(str): current work project name.
            tags(List[str] | None): tags of tracking steps. Default to `None`.
            step_type(StepType): step type. Default to `StepType.CUSTOMIZED`.
            step_name(str | None): step name. Default to `None`.
            model(str | None): using model name. Default to `None`. If you are using llama you can set the field to `llama`.
            
        Returns:
            Callable: decorator
        """

        tracker_options = TrackerOptions(
            project_name=project_name,
            tags=tags,
            is_step=True,
            step_type=step_type,
            step_name=step_name,
            model=model,
        )
    
        if callable(func_name):
            func = func_name
            return self._decorator(func=func, tracker_options=tracker_options)
        
        tracker_options.func_name = func_name

        def decorator(func:Callable):
            return self._decorator(func=func, tracker_options=tracker_options)
        
        return decorator

    def track_trace(
        self,
        func_name: str | Callable,
        project_name: str,
        tags: List[str] | None = None,
        trace_name: str | None = None,
        model: str | None = None,
    ):
        """track trace decorator
        Track trace in calling modules.

        Args:
            func_name(str | Callable): caller can set it they want to name with 'str' type. If caller doesn't set, it will be `Callable`.
            project_name(str): current work project name.
            tags(List[str] | None): tags of tracking traces. Default to `None`.
            trace_name(str | None): trace name. Default to `None`.
            model(str | None): using model name. Default to `None`. If you are using llama you can set it `llama`.

        Returns:
            Callable: decorator
        """
        
        tracker_options = TrackerOptions(
            project_name=project_name,
            tags=tags,
            is_trace=True,
            trace_name=trace_name,
            model=model,
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
                self._after_calling_function(output=result, error_info=error_info, tracker_options=tracker_options)
                if func_exception is not None:
                    raise func_exception
                else:
                    return result

        return wrapper

    def _before_calling_function(
        self,
        func:Callable,
        tracker_options: TrackerOptions,
        args:Tuple,
        kwargs:Dict[str, Any]
    ):
        """ prepare and log input before track function.

        Args:
            func(Callable): func
            tracker_options(TrackerOptions): tracker options
            args(Tuple): passing func arguments. If no arguments, the dictionary is empty.
            kwargs(Dict[str, Any]): passing func keywords arguements. If no keywords arguments, the dictionary is empty.
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

        if tracker_options.is_step:
            at_client.track_step(
                project_name=tracker_options.project_name,
                input=inspect_helper.parse_to_dict_input(func=func, args=args, kwargs=kwargs),
                output=None,
                name=tracker_options.step_name,
                type=tracker_options.step_type,
                tags=tracker_options.tags,
                model=tracker_options.model
            )
        elif tracker_options.is_trace:
            at_client.track_trace(
                project_name=tracker_options.project_name,
                input=inspect_helper.parse_to_dict_input(func=func, args=args, kwargs=kwargs),
                output=None,
                # TODO: Define whether tracks can be get in local or from remote. 
                tracks=None,
                name=tracker_options.trace_name,
                tags=tracker_options.tags,
                model=tracker_options.model,
            )
        else:
            raise ValueError("Value error in tracker decorator. before calling function." \
        "Please check whether set is_trace=True or is_step=True in your tracker_options.One of them should be True.")

    def _after_calling_function(
        self,
        output:Any,
        error_info: str | None,
        tracker_options: TrackerOptions
    ):
        """ prepare and log output after track function """

        if not isinstance(output, Dict):
            output = {"output": output}

        if tracker_options.is_step:
            at_client.track_step(
                project_name=tracker_options.project_name,
                input=None,
                output=output,
                name=tracker_options.step_name,
                type=tracker_options.step_type,
                tags=tracker_options.tags,
                model=tracker_options.model,
                error_info=error_info,
            )

        elif tracker_options.is_trace:
            at_client.track_trace(
                project_name=tracker_options.project_name,
                input=None,
                output=output,
                name=tracker_options.trace_name,
                tags=tracker_options.tags,
                model=tracker_options.model,
                error_info=error_info
            )

        else:
            raise ValueError("Value error in tracker decorator after calling function. " \
        "Please check whether set is_trace=True or is_step=True in your tracker_options.One of them should be True.")


    @abstractmethod
    def start_inputs_args_preprocess(
        self,
        func: Callable,
        tracker_options: TrackerOptions | None,
        args: Tuple,
        kwargs: Dict[str, Any]
    ):
        ...
