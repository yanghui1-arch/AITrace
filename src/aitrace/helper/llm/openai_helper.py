from typing import List

from openai.resources.chat.completions.completions import Completions
from openai._types import NOT_GIVEN, NotGiven, not_given, omit, Omit

def remove_chat_completion_input_fields(
    openai_chat_completion: Completions,
    ignore_fields: List,
    is_ignore_omit: bool = True,
    is_ignore_not_given: bool = True,
):
    """Remove OpenAI chat completion inputs fields
    ChatCompletion is used for openai.chat.completions.create(ChatCompletion)

    Args:
        openai_chat_completion(Completions): openai chat completion parameters.
        ignore_fileds(List): which part caller want to remove
        is_ignore_omit(bool): whether ignore Omit. Default to `True`.
        is_ignore_not_given(bool): whether ignore NOTGIVEN. Default to `True`.
    """
    ...