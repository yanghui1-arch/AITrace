
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

    def __init__(self):
        pass
    