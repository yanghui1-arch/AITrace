from pydantic import BaseModel

class ATConfig(BaseModel):
    apikey: str
    url: str
    use_local: bool