from abc import ABC, abstractmethod

class TrackerOptions:
    ...

class BaseTracker(ABC):
    """ Base tracker to track all output
    Every tracker should be extended `BaseTracker` class.
    Following methods need to be implemented in subclass.
        * 
        *
        *

    Args:

    """

    def __init__(self, options: TrackerOptions | None = None):
        
        self.options = options

    def track(self):
        ...

    def __before_track(self):
        ...

    def __after_track(self):
        ...
