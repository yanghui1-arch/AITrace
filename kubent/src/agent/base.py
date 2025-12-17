from abc import ABC, abstractmethod
from pydantic import BaseModel

class Agent(BaseModel, ABC):
    name: str

    @abstractmethod
    async def run(self, *args, **kwargs):
        ...