import inspect
from typing import Callable, Tuple, Dict, List, Any

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
from enum import Enum

class Provider(Enum):
    OPENAI = 'openai'
    GOOGLE = 'google'
    ANTHROPIC = 'anthropic'
    DEEPSEEK = 'deepseek'
    QWEN = 'qwen'
    OLLAMA = 'ollama'

# inspect llm inputs
def inspect_llm_inputs(func: Callable, provider: Provider | List[Provider]) -> Dict[str, Any]:
    if isinstance(provider, Provider):
        if provider == Provider.OPENAI:
            return inspect_openai_inputs(func=func)
        else:
            ...

    if isinstance(provider, List):
        inspect_info: Dict[str, Dict[str, Any]] = {}
        for _provider in provider:
            if _provider == Provider.OPENAI:
                inspect_info['openai_inputs'] = inspect_openai_inputs(func=func)
            else:
                ...

        return inspect_info

def inspect_openai_inputs(func: Callable) -> Dict[str, Any]:
    """inspect openai package"""
    
    """
    openai.chat.completions.create parameters list
        self,
        *,
        messages: Iterable[ChatCompletionMessageParam],
        model: Union[str, ChatModel],
        stream: bool,
        audio: Optional[ChatCompletionAudioParam] | Omit = omit,
        frequency_penalty: Optional[float] | Omit = omit,
        function_call: completion_create_params.FunctionCall | Omit = omit,
        functions: Iterable[completion_create_params.Function] | Omit = omit,
        logit_bias: Optional[Dict[str, int]] | Omit = omit,
        logprobs: Optional[bool] | Omit = omit,
        max_completion_tokens: Optional[int] | Omit = omit,
        max_tokens: Optional[int] | Omit = omit,
        metadata: Optional[Metadata] | Omit = omit,
        modalities: Optional[List[Literal["text", "audio"]]] | Omit = omit,
        n: Optional[int] | Omit = omit,
        parallel_tool_calls: bool | Omit = omit,
        prediction: Optional[ChatCompletionPredictionContentParam] | Omit = omit,
        presence_penalty: Optional[float] | Omit = omit,
        prompt_cache_key: str | Omit = omit,
        reasoning_effort: Optional[ReasoningEffort] | Omit = omit,
        response_format: completion_create_params.ResponseFormat | Omit = omit,
        safety_identifier: str | Omit = omit,
        seed: Optional[int] | Omit = omit,
        service_tier: Optional[Literal["auto", "default", "flex", "scale", "priority"]] | Omit = omit,
        stop: Union[Optional[str], SequenceNotStr[str], None] | Omit = omit,
        store: Optional[bool] | Omit = omit,
        stream_options: Optional[ChatCompletionStreamOptionsParam] | Omit = omit,
        temperature: Optional[float] | Omit = omit,
        tool_choice: ChatCompletionToolChoiceOptionParam | Omit = omit,
        tools: Iterable[ChatCompletionToolUnionParam] | Omit = omit,
        top_logprobs: Optional[int] | Omit = omit,
        top_p: Optional[float] | Omit = omit,
        user: str | Omit = omit,
        verbosity: Optional[Literal["low", "medium", "high"]] | Omit = omit,
        web_search_options: completion_create_params.WebSearchOptions | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    """


# inspect llm outputs 
def inspect_llm_outputs(func: Callable, provider: Provider | List[Provider]) -> Dict[str, Any]:
    if isinstance(provider, Provider):
        if provider == Provider.OPENAI:
            return inspect_openai_output(func=func)
        else:
            ...

    if isinstance(provider, List):
        inspect_info: Dict[str, Dict[str, Any]] = {}
        for _provider in provider:
            if _provider == Provider.OPENAI:
                inspect_info['openai_inputs'] = inspect_openai_output(func=func)
            else:
                ...
        
        return inspect_info

def inspect_openai_output(func: Callable) -> Dict[str, Any]:
    ...

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
