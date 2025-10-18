from dataclasses import dataclass
from typing import List, Dict, Any


from openai._types import NOT_GIVEN, NotGiven, not_given, omit, Omit


def remove_chat_completion_input_fields(
    openai_chat_completion_params: Dict[str, Any],
    ignore_fields: List[str] | None,
    is_ignore_omit: bool = True,
    is_ignore_not_given: bool = True,
    is_ignore_none: bool = True,
) -> Dict[str, Any]:
    """Remove OpenAI chat completion inputs fields
    ChatCompletion is used for openai.chat.completions.create(ChatCompletion)

    Args:
        openai_chat_completion(Completions): openai chat completion parameters.
        ignore_fileds(List): which part caller want to remove
        is_ignore_omit(bool): whether ignore Omit. Default to `True`.
        is_ignore_not_given(bool): whether ignore NOTGIVEN. Default to `True`.
        is_ignore_none(bool): whether ignore None. Default to `True`.

    Returns:
        Dict[str, Any]: remove keys that caller defines.
    """
    
    keys = openai_chat_completion_params.keys()
    if ignore_fields:
        for ignore_field in ignore_fields:
            if ignore_field not in keys:
                import warnings
                warnings.warn(f"WARNING: The ignore_field you pass `{ignore_field}` doesn't exist in openai.chat.completions.create() parameters.")

            openai_chat_completion_params.pop(ignore_field, "Not exists")

    for k in list(openai_chat_completion_params.keys()):
        if (
            (is_ignore_omit and openai_chat_completion_params[k] == omit )
            or (is_ignore_not_given and (openai_chat_completion_params[k] == not_given or openai_chat_completion_params[k] == NOT_GIVEN))
            or (is_ignore_none and openai_chat_completion_params[k] is None)
        ):
            openai_chat_completion_params.pop(k)
    return openai_chat_completion_params
