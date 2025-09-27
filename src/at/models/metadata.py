
class MetaData:
    """Meta data attached to record and trace
    All useful fields about llm usage such as consume tokens, using model, decay latency and so on.
    """

    def __init__(
        self,
        consume_tokens:int | None = None,
        model: str | None = None,
        decay_latency: float | None = None,
        
    ):
        self._consume_tokens = consume_tokens
        self._model = model
        self._decay_latency = decay_latency

    @property
    def consume_token(self) -> int | None:
        return self._consume_tokens
    
    @property
    def model(self) -> str | None:
        return self._model
    
    @property
    def decay_latency(self) -> float | None:
        return self._decay_latency
