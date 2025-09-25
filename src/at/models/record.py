
class Record:
    """Record is to record input for llm everytime.
    Record class is designed to check what input like be in some modules.
    What is a Record?
    For example:
     ----------                 -----------
    |   INPUT  |    ------->   |   Module  |
     ----------                 -----------

    <<<<<<<<<<             Status            >>>>>>>>>>
     RECORD_1:
     [
        SYSTEM:     You are a helpful assistant.
        USER:       Hello world.
        ASSISTANT:  Nice to meet you.
    ]
    
    ========== APPEND A NEW USER MESSAGE NOW ==========
    RECORD_1:
     [
        SYSTEM:     You are a helpful assistant.
        USER:       Hello world.
        ASSISTANT:  Nice to meet you.
    ]

    RECORD_2:
    [
        SYSTEM:     You are a helpful assistant.
        USER:       Hello world.
        ASSISTANT:  Nice to meet you.
        USER:       Nice to meet you too.          <--------- New user message
        ASSISTANT:  BALABALA....                   <--------- New assistant message
    ]
    ===================================================
    
    It's different with `Trace` class. Trace will merge new pair message into the same trace. Record is stored as a new record
    even when the previous parts are totally same.
    The mission of record is to make user can check whether a module input is expectation and it's easy to implement it.
    """

    def __init__(self):
        ...