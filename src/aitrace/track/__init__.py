from .at_track import AITraceTracker

__all__ = [
    'track_step',
    'track_trace',
]

tracker = AITraceTracker()

track = tracker.track
