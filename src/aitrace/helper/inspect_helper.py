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
    
    return dict(bound_args.arguments)

if __name__ == '__main__':
    import functools
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            print(f"decorator {func.__name__}: {parse_to_dict_input(func, args, kwargs)}")
            return result
        return wrapper

    @decorator
    def init(test_init, k, ms, llm='', ticket={}, *args, **kwargs):
        ...

    init(1, 2, 3, llm='maga', ticket={"key": "value"})

    @decorator
    def post(test, b, quick, is_false=False):
        ...

    post(1, 2, 3, True)
