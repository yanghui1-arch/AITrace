import inspect
from datetime import datetime
from typing import Any, Dict, List

from openai import resources, AsyncStream
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk

from ...models import Step, LLMProvider
from ...track.options import TrackerOptions
from ...context.func_context import current_function_name_context
from ...helper import inspect_helper
from ...helper.llm import openai_helper
from ...client import SyncClient, get_cached_sync_client

raw_async_openai_create = resources.chat.completions.AsyncCompletions.create

def patch_async_openai_chat_completions(step: Step, tracker_options: TrackerOptions):
    async def patched_create(self, *args, **kwargs):
        frame = inspect.currentframe()
        caller = frame.f_back if frame else None
        caller_name = caller.f_code.co_name if caller else None
        # if caller function name is not func name.
        if caller_name != current_function_name_context.get():
            return await raw_async_openai_create(self, *args, **kwargs)

        resp = await raw_async_openai_create(self, *args, **kwargs)
        raw_openai_inputs = inspect_helper.parse_to_dict_input(raw_async_openai_create, args=(self, *args), kwargs=kwargs)
        raw_openai_inputs.pop('self', 'no self')
        async_openai_inputs: Dict[str, Any] = openai_helper.remove_chat_completion_input_fields(
            openai_chat_completion_params=raw_openai_inputs,
            ignore_fields=tracker_options.llm_ignore_fields,
        )

        if isinstance(resp, AsyncStream):
            print("Return ProxyAsyncStream")
            return ProxyAsyncStream(real_async_stream=resp, tracker_options=tracker_options, step=step, inputs=async_openai_inputs)

        # Maybe here can be patched also.
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
                tags=step.tags,
                input={"llm_inputs": async_openai_inputs},
                output={"llm_outputs": resp},
                error_info=step.error_info,
                model=step.model,
                usage=resp.usage,
                start_time=step.start_time,
                end_time=datetime.now()
            )
        return resp
    
    resources.chat.completions.AsyncCompletions.create = patched_create

class ProxyAsyncStream(AsyncStream):
    def __init__(
        self,
        real_async_stream: AsyncStream[ChatCompletionChunk],
        step: Step,
        inputs: Dict[str, Any],
        tracker_options: TrackerOptions
    ):
        self.real_async_stream: AsyncStream[ChatCompletionChunk] = real_async_stream
        self.step = step
        self.inputs = inputs
        self.tracker_options = tracker_options
        self._output: List[ChatCompletionChunk] = []

    async def __aiter__(self):
        async for chunk in self.real_async_stream:
            self._output.append(chunk)
            if chunk.choices[0].finish_reason == 'stop':
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
                    input={"llm_inputs": self.inputs},
                    output={"llm_outputs": llm_output},
                    error_info=self.step.error_info,
                    model=self.step.model,
                    usage=self.step.usage,
                    start_time=self.step.start_time,
                    end_time=datetime.now()
                )
            yield chunk
