from typing import List
from abc import ABC, abstractmethod

from .base import Agent

class ReActAgent(Agent, ABC):
    tags: List[str] = ['ReAct']

    @abstractmethod
    def act(self, *args, **kwargs):
        ...