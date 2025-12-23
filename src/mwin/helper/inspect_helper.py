import inspect
from typing import Callable, Tuple, Dict, Any

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
    if "self" in bound_args.arguments.keys():
        del bound_args.arguments["self"]
    
    return dict(bound_args.arguments)
