from typing import Callable, Any, Tuple, Dict, List
from abc import ABC, abstractmethod
import functools

from .options import TrackerOptions, Provider
from ..models.key_models import StepType, Step, Trace
from ..helper import args_helper, inspect_helper
from ..core.aitrace import at_client
from .. import context


class BaseTracker(ABC):
    """ Base tracker to track all output
    Any decorated with tracker can be considered as a step.
    Every tracker should be extended `BaseTracker` class.
    Following methods need to be implemented in subclass.
        * start_inputs_args_preprocess: preprocess start input before calling function

    Args:
        provider(Optional[str]): provider name
    """

    def __init__(self):
        self.provider: str | None = None
 
    def track(
        self,
        func_name: str | Callable,
        project_name: str,
        tags: List[str] | None = None,
        step_type: StepType = StepType.CUSTOMIZED,
        step_name: str | None = None,
        model: str | None = None,
        track_llm: Provider | List[Provider] | None = None
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
            track_llm(Provider | List[Provider] | None): track a certain llm. Default to `None`. 
                                                    If `track_llm` is not `None`, AITrace will track provider's api.
            
        Returns:
            Callable: decorator
        """

        tracker_options = TrackerOptions(
            project_name=project_name,
            tags=tags,
            step_type=step_type,
            step_name=step_name,
            model=model,
            track_llm=track_llm,
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
                self._after_calling_function(
                    func=func, 
                    output=result, 
                    error_info=error_info, 
                    tracker_options=tracker_options
                )
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
        """ prepare and store input into storage context before calling function.

        Args:
            func(Callable): func
            tracker_options(TrackerOptions): tracker options
            args(Tuple): passing func arguments. If no arguments, the dictionary is empty.
            kwargs(Dict[str, Any]): passing func keywords arguements. If no keywords arguments, the dictionary is empty.
        """
        
        try:
            start_arguments:args_helper.StartArguments = self.start_inputs_args_preprocess(
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
        
        if not context.get_storage_current_trace_data():
            current_trace = args_helper.create_new_trace(
                project_name=tracker_options.project_name,
                input=start_arguments.input,
                name=tracker_options.trace_name,
                tags=tracker_options.tags,
                model=tracker_options.model,
            )
            context.set_storage_trace(current_trace=current_trace)

        new_step: Step = args_helper.create_new_step(
            project_name=tracker_options.project_name,
            input=start_arguments.input,
            name=tracker_options.step_name,
            type=tracker_options.step_type,
            tags=tracker_options.tags,
            model=tracker_options.model,
            usage=start_arguments.usage,
        )
        
        # add step to context
        context.add_storage_step(new_step=new_step)

    def _after_calling_function(
        self,
        func: Callable,
        output: Any,
        error_info: str | None,
        tracker_options: TrackerOptions
    ):
        """ prepare and log output after track function
        
        Arg:
            output(Any): output from decorated function.
            error_info(str | None): error information during executing decorated function.
            tracker_options(TrackerOption): tracker options.
        """

        try:
            end_args: args_helper.EndArguments = self.end_output_exception_preprocess(
                func=func,
                output=output,
                error_info=error_info,
                tracker_options=tracker_options
            )
        except Exception as e:
            print(str(e))

            if output and isinstance(output, Dict) is False:
                output['output'] = output

            end_args = args_helper.EndArguments(
                tags=tracker_options.tags,
                output=output,
                project_name=tracker_options.project_name,
                model=tracker_options.model,
                error_info=error_info,
            )

        if tracker_options.is_step:
            #TODO: pop the latest step
            at_client.track_step(
                project_name=tracker_options.project_name,
                input=None,
                output=end_args.output,
                name=tracker_options.step_name,
                type=tracker_options.step_type,
                tags=tracker_options.tags,
                model=tracker_options.model,
                error_info=error_info,
                usage=end_args.usage,
            )

        elif tracker_options.is_trace:
            at_client.track_trace(
                project_name=tracker_options.project_name,
                input=None,
                output=end_args.output,
                name=tracker_options.trace_name,
                tags=tracker_options.tags,
                model=tracker_options.model,
                error_info=error_info,
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

    @abstractmethod
    def end_output_exception_preprocess(
        self,
        func: Callable,
        output: Any,
        error_info: str | None,
        tracker_options: TrackerOptions,
    ):
        ...
