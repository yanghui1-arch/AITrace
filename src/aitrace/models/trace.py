from typing import Dict, List
from datetime import datetime

class Trace:
    """LLM Trace
    Trace contains a complete conversation consisting of `system`, `user`, `assistant` and `tool`
    It's a chain of conversation from beginning to the ending.
    For example:

    <<<<<<<<<<             Status            >>>>>>>>>>
    TRACE_1:
    [
        SYSTEM: You are a helpful assistant.
        USER: Hello world.
        ASSISTANT: Nice to meet you.
    ]

    ========== APPEND A NEW USER MESSAGE NOW ==========
    <<<<<<<<<<             Status            >>>>>>>>>>
    TRACE_1:
    [
        SYSTEM:     You are a helpful assistant.
        USER:       Hello world.
        ASSISTANT:  Nice to meet you.
        USER:       Nice to meet you too.          <--------- New user message
        ASSISTANT:  BALABALA....                   <--------- New assistant message
    ]
    ===================================================
    
    Aboving example shows what trace could be called a same trace. They will be appended in a same trace
    when a new <Optional[system], user, assitant, Optional[tool]> pair comes in.

    Judge which trace the new pair should be attributed depends on `TrackOptions`. Default method is 
    the new pair should be included in the trace when and only when the previous conversations except current pair are the same
    """

    def __init__(
        self,
        tags:List[str] | None = None,
        llm_input_output: List[Dict] | None = None,
        provider: str | None = None,
        consume_tokens: int | None = None,
        last_updated_time:datetime = datetime.now()
    ):
        """Initialize trace
        
        Args:
            tags(List[str] | None): trace tags. Default to `None`.
            llm_input_output(List[Dict] | None): a list of dict that llm input and output. Default to `None`. 
            provider(str | None): llm provider name. Default to `None`.
            consume_tokens(int | None): consume tokens of the trace.
            last_updated_time(datetime): latest update time of trace. Default to `current datetime in caller's zone.`
        """
        
        if llm_input_output is None:
            import warnings
            warnings.warn("You create a trace that llm_input_output is None.")
        
        self.llm_input_output = llm_input_output
        self._provider = provider
        self.last_updated_time = last_updated_time
        self.tags = tags
        self.consume_tokens = consume_tokens

    @property
    def provider(self):
        return self._provider
    