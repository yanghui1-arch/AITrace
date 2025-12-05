"""Use monkey patch to track openai completions more elegant.
The design transfers sdk complexity to the server complexity.
It's difficult to identify when the `openai.Stream` would be consumed.
In the function whenever `openai.Stream` is consumed and `ChatCompletions` is created AITrace will post it as a step to enrich
existing step, whose id is the same as the patched step. If there is no such step in the server, it will create a new one step
to store.
The benefit of design is split the function IO and LLM IO.
"""

import inspect
from datetime import datetime
from types import TracebackType
from typing import Any, List, Dict
from typing_extensions import Self, override
from openai import resources, Stream
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk
from ..stream import PatchStreamResponse
from ...track.options import TrackerOptions
from ...models import Step, LLMProvider
from ...helper import inspect_helper
from ...helper.llm import openai_helper
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
        raw_openai_inputs = inspect_helper.parse_to_dict_input(raw_openai_create, args=(self, *args), kwargs=kwargs)
        raw_openai_inputs.pop('self', 'no self')
        openai_inputs: Dict[str, Any] = openai_helper.remove_chat_completion_input_fields(
            openai_chat_completion_params=raw_openai_inputs,
            ignore_fields=tracker_options.llm_ignore_fields,
        )

        if isinstance(resp, Stream):
            return ProxyStream(real_stream=resp, tracker_options=tracker_options, step=step, inputs=openai_inputs)

        # No steam calling openai
        model = openai_inputs.get('model', step.model)
        tags = step.tags
        if model is not None:
            tags += [model]

        if tracker_options.track_llm == LLMProvider.OPENAI:
            # log
            client: SyncClient = get_cached_sync_client()
            client.log_step(
                project_name=tracker_options.project_name,
                step_name=step.name,
                step_id=step.id,
                trace_id=step.trace_id,
                parent_step_id=step.parent_step_id,
                step_type=step.type,
                tags=tags,
                input={"llm_inputs": openai_inputs},
                output={"llm_outputs": resp},
                error_info=step.error_info,
                model=model,
                usage=resp.usage,
                start_time=step.start_time,
                end_time=datetime.now()
            )
        return resp
    
    resources.chat.completions.Completions.create = patched_create

class ProxyStream(Stream):
    def __init__(
        self,
        real_stream: Stream[ChatCompletionChunk],
        tracker_options: TrackerOptions,
        step: Step,
        inputs: Dict[str, Any],
    ):
        """Initialize ProxyOpenAIStream
        Wrapper openai.chat.completion.create(stream=True)
        """

        self._real_stream: Stream[ChatCompletionChunk] = real_stream
        self._output:List[ChatCompletionChunk] = []
        self.tracker_options = tracker_options
        self.step = step
        self.inputs = inputs
        self.model = inputs.get('model', step.model)
        self.tags = step.tags
        if self.model is not None:
            self.tags += [self.model]

    @override
    def __next__(self):
        chunk = self._real_stream.__next__()
        if chunk.choices[0].finish_reason == 'stop':
            llm_output = ''.join([output.choices[0].delta.content for output in self._output])
            patch_stream_response = PatchStreamResponse(role="assistant", content=llm_output)
            client: SyncClient = get_cached_sync_client()
            client.log_step(
                project_name=self.tracker_options.project_name,
                step_name=self.step.name,
                step_id=self.step.id,
                trace_id=self.step.trace_id,
                parent_step_id=self.step.parent_step_id,
                step_type=self.step.type,
                tags=self.tags,
                input={"llm_inputs": self.inputs},
                output={"llm_outputs": patch_stream_response.model_dump(exclude_none=True)},
                error_info=self.step.error_info,
                model=self.model,
                usage=self.step.usage,
                start_time=self.step.start_time,
                end_time=datetime.now()
            )
        return chunk

    @override
    def __iter__(self):
        for chunk in self._real_stream:
            self._output.append(chunk)
            if chunk.choices[0].finish_reason == 'stop':
                # post log request or push into storage context and then _ALREADY_PATCH=False
                #                       ↑---- need think carefully.
                llm_output = ''.join([output.choices[0].delta.content for output in self._output])
                patch_stream_response = PatchStreamResponse(role="assistant", content=llm_output)
                client: SyncClient = get_cached_sync_client()
                client.log_step(
                    project_name=self.tracker_options.project_name,
                    step_name=self.step.name,
                    step_id=self.step.id,
                    trace_id=self.step.trace_id,
                    parent_step_id=self.step.parent_step_id,
                    step_type=self.step.type,
                    tags=self.tags,
                    input={"llm_inputs": self.inputs},
                    output={"llm_outputs": patch_stream_response.model_dump(exclude_none=True)},
                    error_info=self.step.error_info,
                    model=self.model,
                    usage=self.step.usage,
                    start_time=self.step.start_time,
                    end_time=datetime.now()
                )
                print(f"[LOG]: proxy log step successfully: {llm_output}")
                
            yield chunk

    @override
    def __enter__(self):
        return super().__enter__()
    
    @override
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close()

    @override
    def close(self) -> None:
        """
        Close the response and release the connection.

        Automatically called if the response body is read to completion.
        """
        self._real_stream.response.close()

    def __getattr__(self, name):
        return getattr(self._real_stream, name)
    
