from typing import Any
from pydantic import BaseModel

def safe_serialize(obj: Any) -> Any:
    """safe serialize all customized classes
    
    Args:
        obj(Any): any type data or class

    Returns:
        Any: obj or data after being safely searialized 
    """

    # None
    if obj is None:
        return None
    
    # basic type
    if isinstance(obj, (str, int, float, bool)):
        return obj
    
    # pydantic
    if isinstance(obj, BaseModel):
        return obj.model_dump()
    
    # dict
    if isinstance(obj, dict):
        return {k: safe_serialize(v) for k, v in obj.items()}
    
    # list or tuple
    if isinstance(obj, (list, tuple)):
        return [safe_serialize(item) for item in obj]
    
    # customized class with `__dict__` function
    if hasattr(obj, '__dict__') and obj.__dict__:
        return safe_serialize(obj.__dict__)
    
    # other information
    try:
        return str(obj)
    except:
        return f'<CAN NOT SERIALIZED TYPE: {type(obj).__name__}>'