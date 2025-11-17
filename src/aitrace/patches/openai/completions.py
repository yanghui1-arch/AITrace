"""Use monkey patch to track openai Stream[ChatCompletionChunk] more elegant.
The function will replace return value of openai stream as ProxyOpenAIStream so that
AITrace can track stream generator content as a complete content and then post 
request to server.
Callers use `Stream` in two conditions.
1. In the function generate `Stream` and then consume it
2. In the function generate `Stream` but not consume it and return it for others 
to consume.
Considering two conditions, AITrace decide to store the Stream as a string at the
begining. Then it will be two probabilities.
1. Caller decorate function without consuming `Stream`
2. Calelr decorate function with consuming `Stream`
Probabilities 1 results in storage context has been empty after consuming `Stream`.
Probabilities 2 results in the step, which is the owner of `Stream`, is still in
the storage context.
Prob1 ProxyOpenAIStream should pass it directly to the server and server should replace
the step's output with the `ProxyOpenAIStream._output`. Therefore ProxyOpenAIStream
need a start_time attribute and func_name which makes server replacing.
Prob2 ProxyOpenAIStream should manually replacing step output with 
`ProxyOpenAIStream._output`.
"""

import inspect
from datetime import datetime
from typing import List
from openai import resources, Stream
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk
from ...track.options import TrackerOptions
from ...models import Step, Trace, LLMProvider
from ... import context
from ...context.func_context import current_function_name_context
from ...client import get_cached_sync_client, SyncClient

raw_openai_create = resources.chat.completions.Completions.create

def patch_openai_chat_completions(step: Step, tracker_options: TrackerOptions, func_name: str):
    """Patch openai chat completions in the step.
    The function is convenient to track llm output in the step which is seperate with the `ATTracker` class.
    Before calling tracked function AITrace has to decide which step's openai call should be patched to track.
    
    Args:
        step(Step): step which need to patch openai chat completions
        tracker_options(TrackerOptions): tracker options.
        func_name(str): tracked func_name
    """
    
    def patched_create(self, *args, **kwargs):
        frame = inspect.currentframe()
        caller = frame.f_back if frame else None
        caller_name = caller.f_code.co_name if caller else None
        # if caller function name is not func name.
        if caller_name != current_function_name_context.get():
            return raw_openai_create(self, *args, **kwargs)

        resp = raw_openai_create(self, *args, **kwargs)
        if isinstance(resp, Stream):
            return ProxyChatCompletionChunkStream(real_stream=resp, tracker_options=tracker_options, step=step)

        # Maybe here can be patched also.
        return resp
    
    resources.chat.completions.Completions.create = patched_create

class ProxyChatCompletionChunkStream(Stream):
    def __init__(
        self,
        real_stream: Stream[ChatCompletionChunk],
        tracker_options: TrackerOptions,
        step: Step,
    ):
        """Initialize ProxyOpenAIStream
        Wrapper openai.chat.completion.create(stream=True)
        """

        self._real_stream: Stream[ChatCompletionChunk] = real_stream
        self._output:List[ChatCompletionChunk] = []
        self.tracker_options = tracker_options
        self.step = step

    def __iter__(self):
        for chunk in self._real_stream:
            self._output.append(chunk)
            if chunk.choices[0].finish_reason == 'stop':
                # post log request or push into storage context and then _ALREADY_PATCH=False
                #                       ↑---- need think carefully.
                llm_output = ''.join([output.choices[0].delta.content for output in self._output])
                client: SyncClient = get_cached_sync_client()
                client.log_step(
                    project_name=self.tracker_options.project_name,
                    step_name=self.step.name,
                    step_id=self.step.id,
                    trace_id=self.step.trace_id,
                    parent_step_id=self.step.parent_step_id,
                    step_type=self.step.type,
                    tags=self.step.tags,
                    input=self.step.input,
                    output={"llm_outputs": llm_output},
                    error_info=self.step.error_info,
                    model=self.step.model,
                    usage=self.step.usage,
                    start_time=self.step.start_time,
                    end_time=datetime.now()
                )
                print(f"[LOG]: proxy log step successfully: {llm_output}")
                # post request for update
                ...
                
            yield chunk

    def __getattr__(self, name):
        return getattr(self._real_stream, name)
    
