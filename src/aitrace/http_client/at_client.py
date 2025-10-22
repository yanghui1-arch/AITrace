import httpx
import functools

class AITrace:
    """AITrace class is to communicate with server.
    Currently support track step, trace and conversation.
    """

    def __init__(self):
        pass

    def track_trace(self, ):
        pass

    def track_step(self, ):
        pass

    def track_conversation(self, ):
        pass


@functools.lru_cache()
def get_cached_client() -> AITrace:
    client = AITrace()

    return client