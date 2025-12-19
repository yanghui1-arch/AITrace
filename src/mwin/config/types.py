from pydantic import BaseModel


class ATConfig(BaseModel):
    """Central config object for aitrace.

    Provide defaults so first-run without a config file works
    and interactive configure flow can prefill values.
    """

    apikey: str | None = None
    url: str = "http://www.petmate.fun"
    use_local: bool = False
