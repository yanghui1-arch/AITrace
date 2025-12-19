if __name__ == '__main__':
    from src.mwin.models.common import LLMProvider
    from src.mwin.track import track
    from openai import OpenAI

    from pydantic import BaseModel
    class YourClass(BaseModel):
        y: int

    class Myclass(BaseModel):
        x: int = 123
        yourclass: YourClass = YourClass(y=2)

    class EmptyClass:

        def __init__(self):
            pass

    @track(
        project_name="aitrace_demo",
        tags=['test', 'demo'],
        track_llm=LLMProvider.OPENAI,    
    )
    def llm_classification(film_comment: str):
        prompt = "Please classify the film comment into happy, sad or others. Just tell me result. Don't output anything."
        cli = OpenAI(base_url='https://dashscope.aliyuncs.com/compatible-mode/v1', api_key='sk-fa1a965af7a74f7eaff9b2b90aaa101e')
        user_message = {"role": "user", "content": f"{prompt}\nfilm_comment: {film_comment}"}
        response = cli.chat.completions.create(
            messages=[user_message],
            model="qwen3-max",
            temperature=0.7,
        ).choices[0].message.content

        llm_counts(film_comment=film_comment)
        llm_test_my_class()
        llm_test_pass_class(Myclass())
        llm_test_zero_attr_class()
        llm_test_several_conversations(previous_messages_with_assistant=[user_message, {"role": "assistant", "content": response}])
        with_llm_sync_stream()
        return {
            "test_dict": "test"
        }
    
    @track(
        project_name="aitrace_demo",
        tags=['test', 'demo'],
        track_llm=LLMProvider.OPENAI,    
    )
    def llm_test_several_conversations(previous_messages_with_assistant: list):
        prompt = "Summarize conversation content by only 30 tokens."
        cli = OpenAI(base_url='https://dashscope.aliyuncs.com/compatible-mode/v1', api_key='sk-fa1a965af7a74f7eaff9b2b90aaa101e')

        response = cli.chat.completions.create(
            messages=[
                {"role": "system", "content": "you are good at summarizing conversation"}
            ] + previous_messages_with_assistant + [
                {"role": "user", "content": prompt}
            ],
            model="deepseek-v3"
        ).choices[0].message.content

        return response
    
    @track(
        project_name="aitrace_demo",
        tags=['test', 'demo'],
        track_llm=LLMProvider.OPENAI,    
    )
    def llm_test_zero_attr_class():
        return EmptyClass()
    
    @track(
        project_name="aitrace_demo",
        tags=['test', 'demo'],
        track_llm=LLMProvider.OPENAI,    
    )
    def llm_test_my_class():
        prompt = "It's a test my class. Don't output anything."
        cli = OpenAI(base_url='https://dashscope.aliyuncs.com/compatible-mode/v1', api_key='sk-fa1a965af7a74f7eaff9b2b90aaa101e')
        cli.chat.completions.create(
            messages=[{"role": "user", "content": f"{prompt}"}],
            model="qwen3-max"
        ).choices[0].message.content
        return Myclass()
    
    @track(
        project_name="aitrace_demo",
        tags=['test', 'demo'],
        track_llm=LLMProvider.OPENAI,    
    )
    def llm_test_pass_class(passing_class: Myclass):
        prompt = "It's a test my class. Don't output anything."
        cli = OpenAI(base_url='https://dashscope.aliyuncs.com/compatible-mode/v1', api_key='sk-fa1a965af7a74f7eaff9b2b90aaa101e')
        cli.chat.completions.create(
            messages=[{"role": "user", "content": f"{prompt}"}],
            model="qwen3-max"
        ).choices[0].message.content
        return "test_pass_class"
    
    @track(
        project_name="aitrace_demo",
        tags=['test', 'demo', 'second_demo'],
        track_llm=LLMProvider.OPENAI,
    )
    def llm_counts(film_comment: str):
        prompt = "Count the film comment words. just output word number. Don't output anything others."
        cli = OpenAI(base_url='https://dashscope.aliyuncs.com/compatible-mode/v1', api_key='sk-fa1a965af7a74f7eaff9b2b90aaa101e')
        llm_test_my_class()
        return cli.chat.completions.create(
            messages=[{"role": "user", "content": f"{prompt}\nfilm_comment: {film_comment}"}],
            model="qwen3-max"
        ).choices[0].message.content
    
    @track(
        project_name="aitrace_demo",
        tags=['test', 'demo', 'second_demo'],
        track_llm=LLMProvider.OPENAI,
    )
    def with_llm_sync_stream():
        prompt = "talk something."
        cli = OpenAI(base_url='https://dashscope.aliyuncs.com/compatible-mode/v1', api_key='sk-fa1a965af7a74f7eaff9b2b90aaa101e')
        print()
        with cli.chat.completions.create(
            messages=[{"role": "user", "content": f"{prompt}"}],
            model="qwen3-max",
            stream=True
        ) as stream:
            for chunk in stream:
                print(chunk.choices[0].delta.content, end="", flush=True)

        return stream

    from time import time
    start_time = time()


    import asyncio
    @track(
        project_name="aitrace_demo",
        tags=['test', 'demo'],
        track_llm=LLMProvider.OPENAI,    
    )
    async def llm_async_not_stream():
        from openai import AsyncOpenAI
        prompt = "Count the film comment words. just output word number. Don't output anything others."
        cli = AsyncOpenAI(base_url='https://dashscope.aliyuncs.com/compatible-mode/v1', api_key='sk-fa1a965af7a74f7eaff9b2b90aaa101e')
        
        response = await cli.chat.completions.create(
            messages=[{"role": "user", "content": f"{prompt}\nfilm_comment: let it go"}],
            model="qwen3-max"
        )
        print(f"llm_async_not_stream: {response.choices[0].message.content}")
        await async_not_stream_inner_1()
        await async_not_stream_inner_2()
        return response.choices[0].message.content
    
    @track(
        project_name="aitrace_demo",
        tags=['test', 'demo'],
        track_llm=LLMProvider.OPENAI,    
    )
    async def async_not_stream_inner_1():
        from openai import AsyncOpenAI
        prompt = "hello"
        cli = AsyncOpenAI(base_url='https://dashscope.aliyuncs.com/compatible-mode/v1', api_key='sk-fa1a965af7a74f7eaff9b2b90aaa101e')
        
        response = await cli.chat.completions.create(
            messages=[{"role": "user", "content": f"{prompt}\nfilm_comment: let it go"}],
            model="qwen3-max"
        )
        print(f"llm_async_not_stream: {response.choices[0].message.content}")
        return response.choices[0].message.content
    
    @track(
        project_name="aitrace_demo",
        tags=['test', 'demo'],
        track_llm=LLMProvider.OPENAI,    
    )
    async def async_not_stream_inner_2():
        from openai import AsyncOpenAI
        prompt = "nice to meet you"
        cli = AsyncOpenAI(base_url='https://dashscope.aliyuncs.com/compatible-mode/v1', api_key='sk-fa1a965af7a74f7eaff9b2b90aaa101e')
        
        response = await cli.chat.completions.create(
            messages=[{"role": "user", "content": f"{prompt}\nfilm_comment: let it go"}],
            model="qwen3-max"
        )
        print(f"llm_async_not_stream: {response.choices[0].message.content}")
        return response.choices[0].message.content
    
    @track(
        project_name="aitrace_test_stream",
        tags=['test', 'demo'],
        track_llm=LLMProvider.OPENAI,    
    )
    async def llm_async_stream():
        from openai import AsyncOpenAI
        prompt = "Say something about film comment just 50 tokens"
        cli = AsyncOpenAI(base_url='https://dashscope.aliyuncs.com/compatible-mode/v1', api_key='sk-fa1a965af7a74f7eaff9b2b90aaa101e')
        
        response = await cli.chat.completions.create(
            messages=[{"role": "user", "content": f"{prompt}\nfilm_comment: Steamly asyncio function"}],
            model="qwen3-max",
            stream=True,
            stream_options={"include_usage": True}
        )
        async for chunk in response:
            if len(chunk.choices):
                print(chunk.choices[0].delta.content, end="", flush=True)

        return response
    
    @track(
        project_name="aitrace_test_stream",
        tags=['test', 'demo'],
        track_llm=LLMProvider.OPENAI,    
    )
    async def with_llm_async_stream():
        from openai import AsyncOpenAI
        prompt = "Say something about film comment just 50 tokens"
        cli = AsyncOpenAI(base_url='https://dashscope.aliyuncs.com/compatible-mode/v1', api_key='sk-fa1a965af7a74f7eaff9b2b90aaa101e')
        
        async with await cli.chat.completions.create(
            messages=[{"role": "user", "content": f"{prompt}\nfilm_comment: Steamly asyncio function"}],
            model="qwen3-max",
            stream=True
        ) as stream:
            async for chunk in stream:
                print(chunk.choices[0].delta.content, end="", flush=True)

        return stream
    
    @track(
        project_name="aitrace_test_stream",
        tags=['test', 'demo'],
        track_llm=LLMProvider.OPENAI,    
    )
    def llm_stream():
        prompt = "Say something about film comment just 50 tokens"
        cli = OpenAI(base_url='https://dashscope.aliyuncs.com/compatible-mode/v1', api_key='sk-fa1a965af7a74f7eaff9b2b90aaa101e')
        completion = cli.chat.completions.create(
            messages=[{"role": "user", "content": f"{prompt}\nfilm_comment: Hello"}],
            model="qwen3-max",
            stream=True,
            stream_options={"include_usage": True}
        )
        # for chunk in completion:
        #     print(chunk.choices[0].delta.content, end="", flush=True)
        # print()
        llm_classification(prompt)
        return completion
    
    llm_classification("Wow! It sucks.")
    completion = llm_stream()
    asyncio.run(main=llm_async_not_stream())
    asyncio.run(main=llm_async_stream())
    asyncio.run(main=with_llm_async_stream())
    for chunk in completion:
        if len(chunk.choices) != 0:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print()
    print(f"Avg. consume time: {time() - start_time}")
    # llm_test_zero_attr_class()