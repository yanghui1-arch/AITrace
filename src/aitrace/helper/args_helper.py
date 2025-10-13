from dataclasses import dataclass
from typing import Optional, Any, List, Dict

@dataclass
class BaseArguments:
    def to_kwargs(self, ignore_keys: Optional[List[str]] = None) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        ignore_keys = [] if ignore_keys is None else ignore_keys
        for key, value in self.__dict__.items():
            if (value is not None) and (key not in ignore_keys):
                result[key] = value

        return result

@dataclass
class StartArguments(BaseArguments):

    func_name: str
    tags: List[str] | None = None
    input: Dict[str, Any] | None = None
    project_name: str | None = None
    model: str | None = None
    usage: int | None = None

@dataclass
class EndArguments(BaseArguments):

    tags: List[str] | None = None
    input: Dict[str, Any] | None = None
    output: Dict[str, Any] | None = None
    project_name: str | None = None
    model: str | None = None
    error_info: str | None = None
    usage: int | None = None
