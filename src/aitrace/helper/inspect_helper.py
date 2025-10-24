import sys
import inspect
from dataclasses import dataclass
from types import FrameType
from typing import Callable, Tuple, Dict, List, Any

from openai.types.chat.chat_completion import ChatCompletion

from .._exception import CallingSDKNotFoundException
from ..models.common import LLMProvider

def parse_to_dict_input(
    func: Callable,
    args: Tuple,
    kwargs: Dict[str, Any]
) -> Dict[str, Any]:
    """parse args and kwargs to a dict type input
    
    Args:
        args(Tuple): arguments tuple. args tuple maybe empty.
        kwargs(Dict[str, Any]): keyword arguemnts. kwargs dict maybe empty.
    
    Returns:
        Dict[str, Any]: input with dict type
    """
    
    sig = inspect.signature(func)
    
    # Create binding of arguments to parameters
    bound_args = sig.bind(*args, **kwargs)
    bound_args.apply_defaults()
    
    return dict(bound_args.arguments)


#################################################################
#                 inspect about llm                             #
#################################################################
@dataclass
class TrackLLMFunction:
    name: str
    provider: LLMProvider
    inputs: Dict[str, Any] | None = None
    output: ChatCompletion | None = None

    # TODO: Offer a function to exclude Omit and NOTGIVEN

# TODO: it maybe not safe from threading or coroutine view.
#       later can design it as a ContextVar        

# Store llm execution result and prior sys tracking traces.
# to_track_llm_funcs stores result based on who ends llm execution more quick. It's not a queue.
to_track_llm_funcs: List[TrackLLMFunction] = []
sys_traces: List[Callable] = []

# inspect llm inputs
def start_trace_llm(func_name: str, provider: LLMProvider):
    track_llm_function = TrackLLMFunction(name=func_name, provider=provider)

    if provider == LLMProvider.OPENAI:
        start_trace_openai(track_llm_function=track_llm_function)
    else:
        ...

# TODO: The bug of the same function name in different packages or classes. 
#       Some of them are needed to track llm but the rest don't need.
def start_trace_openai(track_llm_function: TrackLLMFunction):
    """start trace openai"""

    def trace_openai(frame: FrameType, event, arg):
        global to_track_llm_funcs
        caller_name: str = frame.f_back.f_code.co_name if frame.f_back else ''
        executing_func_name: str = frame.f_code.co_name
        locals_ = frame.f_locals

        if event == 'return':
            if executing_func_name == 'create' and 'self' in locals_:
                cls_name = type(locals_['self']).__name__
                module_name = type(locals_['self']).__module__
                print(f"cls_name: {cls_name}, module_name: {module_name}")
                if cls_name == 'Completions' and module_name.startswith('openai'):
                    track_llm_function.output = arg
                    to_track_llm_funcs.append(track_llm_function)
            # other openai sdk
            else:
                ...

        if event != 'call':
            return trace_openai
        
        # if caller_name == track_llm_function.name:
        #     print(f"caller_name: {caller_name}")
        #     print(f"executing_function_name: {executing_func_name}")
        if executing_func_name == 'create' and 'self' in locals_:
            cls_name = type(locals_['self']).__name__
            module_name = type(locals_['self']).__module__
            if cls_name == 'Completions' and module_name.startswith('openai'):
                llm_inputs = {k: v for k, v in frame.f_locals.items() if k != 'self'}
                track_llm_function.inputs = llm_inputs
        # other openai sdk
        else:
            ...
        
        return trace_openai
    
    current_sys_trace = sys.gettrace()
    if current_sys_trace:
        sys_traces.append(current_sys_trace)

    sys.settrace(trace_openai)

def stop_trace_llm(func_name: str) -> TrackLLMFunction:
    """Stop trace llm given a function
    It means the root function with sys_traces length is 0.
    
    Args:
        func_name(str): which function name should be stopped to track llm inputs and outputs.

    Returns:
        TrackLLMFunction: return a matched tracked llm function class.
    
    Raises:
        CallingSDKNotFoundException: when not found function name in the storage list. Generally happens when aitrace code designs.
    """

    if len(sys_traces):
        trace = sys_traces.pop()
        sys.settrace(trace)
    else:
        sys.settrace(None)
    
    global to_track_llm_funcs

    match_track_llm_func: List[TrackLLMFunction] = [track_llm_func for track_llm_func in to_track_llm_funcs if track_llm_func.name == func_name]
    if not match_track_llm_func:
        raise CallingSDKNotFoundException()
    
    track_llm_func_in_this_trace = match_track_llm_func[0]
    to_track_llm_funcs.remove(track_llm_func_in_this_trace)
    return track_llm_func_in_this_trace

if __name__ == '__main__':
    # import functools
    # def decorator(func):
    #     @functools.wraps(func)
    #     def wrapper(*args, **kwargs):
    #         result = func(*args, **kwargs)
    #         print(f"decorator {func.__name__}: {parse_to_dict_input(func, args, kwargs)}")
    #         return result
    #     return wrapper

    # @decorator
    # def init(test_init, k, ms, llm='', ticket={}, *args, **kwargs):
    #     ...

    # init(1, 2, 3, llm='maga', ticket={"key": "value"})

    # @decorator
    # def post(test, b, quick, is_false=False):
    #     ...

    # post(1, 2, 3, True)

    start_trace_openai(TrackLLMFunction(name='demotest', provider=LLMProvider.OPENAI))
    print("START")
    from time import sleep
    sleep(2)
    print("END")
