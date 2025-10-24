from typing import Callable, Any, Tuple, Dict, List
from abc import ABC, abstractmethod
from datetime import datetime, timezone, timedelta
import functools

from .options import TrackerOptions
from .. import context
from ..models.key_models import StepType, Step, Trace, Track
from ..models.common import LLMProvider
from ..helper import args_helper
from ..client import sync_client


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
        project_name: str,
        func_name: str | Callable | None = None,
        tags: List[str] | None = None,
        step_type: StepType = StepType.CUSTOMIZED,
        step_name: str | None = None,
        model: str | None = None,
        track_llm: LLMProvider | None = None,
        llm_ignore_fields: List[str] | None = None,
    ) -> Callable:
        """track step decorator
        Track step in calling modules. If use decorator to track step, the step and the trace id will be always a whole new ones.
        In other words, you cannot set the step id and its belonging trace id. It's recommended to be used in a simple demo.

        Args:
            project_name(str): current work project name.
            func_name(str | Callable | None): caller can set it they want to name with 'str' type. If caller doesn't set, it will be `Callable`.
            tags(List[str] | None): tags of tracking steps. Default to `None`.
            step_type(StepType): step type. Default to `StepType.CUSTOMIZED`.
            step_name(str | None): step name. Default to `None`.
            model(str | None): using model name. Default to `None`. If you are using llama you can set the field to `llama`.
            track_llm(LLMProvider | None): track a certain llm. Default to `None`. 
                                            If `track_llm` is not `None`, AITrace will track provider's api.
            llm_ignore_fields(List[str] | None): a list of llm ignore fields name. Default to `None`.
            
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
            llm_ignore_fields=llm_ignore_fields,
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
        
        if not tracker_options.step_name:
            tracker_options.step_name = func.__name__

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
                output = {'output': output}

            end_args = args_helper.EndArguments(
                tags=tracker_options.tags,
                output=output,
                project_name=tracker_options.project_name,
                model=tracker_options.model,
                error_info=error_info,
            )

        current_step: Step | None = context.pop_storage_step()
        if not current_step:
            # TODO: Log the error information and create a new step to prevent executing exception.
            current_step: Step = args_helper.create_new_step(
                project_name=tracker_options.project_name,
                input=end_args.llm_input,
                name=tracker_options.step_name,
                type=tracker_options.step_type,
                tags=tracker_options.tags,
                model=tracker_options.model,
            )
        # update current step
        # TODO: improve update and try to encapsulate it
        if end_args.llm_input is not None:
            func_inputs = current_step.input
            llm_inputs = end_args.llm_input
            current_step.input = {'func_inputs': func_inputs, 'llm_inputs': llm_inputs}
            current_step.model = llm_inputs.get('model', None)

        current_step.output = end_args.output
        current_step.error_info = end_args.error_info
        
        # TODO: add usage and redefine Step class usage type
        current_step.usage = end_args.usage

        # update trace
        if not context.get_storage_current_trace_data():
            current_trace = args_helper.create_new_trace(
                project_name=tracker_options.project_name,
                input=end_args.llm_input,
                name=tracker_options.trace_name,
                tags=tracker_options.tags,
                model=tracker_options.model,
            )
            context.set_storage_trace(current_trace=current_trace)
        
        current_trace: Trace = context.get_storage_current_trace_data()
        if not current_trace.tracks:
            current_trace.tracks = []
        # TODO: add a selectable region to track.
        current_trace.tracks.append(Track(_step=current_step, call_timestamp=datetime.now(timezone(timedelta(hours=8)))))

        # TODO: improve current trace final output
        # The easist way to record current trace output. But it's not for the final output just every step output.
        if error_info is None:
            current_trace.output = end_args.output
        else:
            current_trace.output = None
            current_trace.error_info = error_info

        context.set_storage_trace(current_trace=current_trace)
        # print(f"current_trace: {current_trace}")
        print(f"current step: {current_step}")

        # TODO: Post a request to server
        client: sync_client.SyncClient = sync_client.get_cached_sync_client()

        client.log_step(
            project_name=current_step.project_name,
            step_name=current_step.name,
            step_id=str(current_step.id),
            trace_id=str(current_step.trace_id),
            parent_step_id=str(current_step.parent_step_id),
            step_type=current_step.type,
            tags=current_step.tags,
            input=current_step.input,
            output=current_step.output,
            error_info=current_step.error_info,
            model=current_step.model,
            usage=current_step.usage,
        )

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
