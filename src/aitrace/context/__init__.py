from .storage import aitrace_storage_context

__all__ = [
    "add_storage_step",
    "pop_storage_step",
    "set_storage_trace",
    "pop_storage_trace",
]

add_storage_step = aitrace_storage_context.add_step
pop_storage_step = aitrace_storage_context.pop_step
set_storage_trace = aitrace_storage_context.set_trace
pop_storage_trace = aitrace_storage_context.pop_trace
