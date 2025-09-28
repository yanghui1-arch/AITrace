from src.at.track.base import BaseTracker

track = BaseTracker().track

@track
def request(inputs:list[dict]):
    return "123"

request([{"role": "user", "content": "content"}])