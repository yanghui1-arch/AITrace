from typing import List, Dict
from pydantic import BaseModel, Field, model_validator
from openai import OpenAI, pydantic_function_tool
from openai.types.chat import ChatCompletionMessageParam, ChatCompletion, ChatCompletionFunctionToolParam
from .react import ReActAgent
from .tools.search import SearchGoogle
from ..env import Env

class Result(BaseModel):
    answer: str
    """Answer of Kubent"""

    chats: List[ChatCompletionMessageParam]
    """ChatCompletionParams list. It contains user's question, kubent's tool calling, kubent's thoughts, kubent's answer but not contains previous prompts."""

system_bg = f"""Your name is "Kubent". Kubent is a useful assistant to keep improve agent performance better.
Generally, Kubent will recieve one or multiple abstract agent process flow graphs. These graphs reflects how agent system works.
It's possible that more than two graphs works as the same. Kubent can think them as a pattern or a fixed route.

All we know, every agent system works for a certain purpose.
For example one people designs a phone agent that can give strange a phone and recommend its product. Another designs an office-word agent that can handle word documents.
Due to the complexity of various agent purposes, their process flow graph is different. In the same time, make their performance better will be different.
Kubent need to pose a concrete and specifically optimized for the task solution to make agent system performance upgrade about ~1% at least than before.
There are many tools you can use them. Sometimes Kubent will think considerate details, how to start next step and so on.

Finally Kubent will provide user with a specific enterprise-level solution. This solution must fulfill the following requirements:
> Describe Kubent's solution as precisely and explicitly as possible.
> Provide structured data of the modified agent system flowchart.
> Briefly summarize the differences between the modified flowchart and the original one.
> Explain to the user what problems the proposed solution can address.

Kubent will finish this round talk with [Finish] starting. Finish reason has three conditions.
Condition 1: Offer a specific enterprise-level solution.
Condition 2: Request user provide more details that you can't access by tools or your brain knowledge.
Condition 3: Think a great response to reply user.
"""

class Kubent(ReActAgent):
    name: str = "Kubent"
    model: str = "x-ai/grok-4-fast"
    tools: List[ChatCompletionFunctionToolParam] = Field(..., default_factory=list)
    engine: OpenAI = OpenAI()
    current_env: Env
    attempt: int = 10

    class Config:
        arbitrary_types_allowed=True

    @model_validator(mode="after")
    def load_tools_and_set_env_action_space(self):
        self.tools = [SearchGoogle().json_schema]
        for tool in self.tools:
            self.current_env.update_space_action(tool=tool)

        return self

    def run(self, question: str) -> Result:
        cnt = 0
        terminate = False
        obs = self.current_env.reset()
        act_info = {
            "step_finish_reason": "",
            "steps": 0,
            "num_tool_callings": 0, 
            "answer": ""
        }
        while terminate is False and cnt < self.attempt:
            obs, reward, terminate, act_info = self.act(question=question, obs=obs)
            cnt += 1

        if act_info.get("step_finish_reason") == "solved":
            chats:List[ChatCompletionMessageParam] = [{"role": "user", "content": question}] + obs + [{"role": "assistant", "content": act_info.get("answer")}]
            return Result(
                answer=act_info.get("answer"),
                chats=chats
            )
            
        else:
            chats:List[ChatCompletionMessageParam] = [{"role": "user", "content": question}] + obs + [{"role": "assistant", "content": f"Exceed max attempts: {self.attempt}"}]
            return Result(answer=f"Exceed max attempts: {self.attempt}", chats=chats)

    def act(self, question: str, obs: List[ChatCompletionMessageParam]) -> tuple[List[ChatCompletionMessageParam], float, bool, Dict[str, str]]:
        completion:ChatCompletion = self.engine.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_bg},
                {"role": "user", "content": question},
            ] + obs,
            tools=self.tools,
            parallel_tool_calls=True,
        )
        return self.current_env.step(llm_action=completion.choices[0].message)

    def register_tool(self, tool):
        try:
            new_tool:ChatCompletionFunctionToolParam = pydantic_function_tool(tool)
            self.tools.append(new_tool)
            self.current_env.update_space_action(tool=tool)
        except Exception as exce:
            print(f"[Error] Failed to register new tool for Kubent: {exce}")

    def change_env(self, new_env: Env):
        self.current_env = new_env

if __name__ == "__main__":
    env = Env(env_name="test")
    kubent = Kubent(current_env=env)
    solution = kubent.run(question=f"""Can you improve my process flow? My process flow is:
                step_id                     step_name                               parent_step_id
    019b0c98-8fd9-7617-9288-222147b71c87 llm_counts                       019b0c98-87e0-70d2-89ff-ddd8466224c2                                
    019b0c98-9e12-70a6-9d7a-1f1cbed7fd88 llm_test_my_class                019b0c98-87e0-70d2-89ff-ddd8466224c2  
    019b0c98-a36f-7eb7-8538-24bee2b18a5f llm_test_pass_class              019b0c98-87e0-70d2-89ff-ddd8466224c2          
    019b0c98-ab46-7a00-90fa-9f5bb5d2ac15 llm_test_zero_attr_class         019b0c98-87e0-70d2-89ff-ddd8466224c2      
    019b0c98-ab80-73d8-8f75-9eb4e6f4ec78 llm_test_several_conversations   019b0c98-87e0-70d2-89ff-ddd8466224c2                   
    019b0c98-b1fa-72b8-868b-db2973b553ec with_llm_sync_stream             019b0c98-87e0-70d2-89ff-ddd8466224c2      
    019b0c98-cf94-7f90-a8fc-f3284b0c69eb llm_async_not_stream                           null                
    019b0c98-ca3c-743c-906d-12621228a06f llm_stream                                     null   
    019b0c98-d636-7d40-ad7d-e5b51c890f4f async_not_stream_inner_1         019b0c98-cf94-7f90-a8fc-f3284b0c69eb                                                              
    019b0c99-1736-7e26-ae5b-f938b14d88d2 async_not_stream_inner_2         019b0c98-cf94-7f90-a8fc-f3284b0c69eb                  
    019b0c99-6c42-7b48-808a-d2599c9a61de llm_async_stream                               null             
    019b0c99-766c-7ae0-a50e-4dc9759a51b5 with_llm_async_stream                          null                     
    019b0c98-8ff1-7530-ab77-43899bab8322 llm_test_my_class                019b0c98-8fd9-7617-9288-222147b71c87                                              
    019b0c98-87e0-70d2-89ff-ddd8466224c2 llm_classification                                                                                             
    """)
    print(f"chains: {env.chains}")
    print(solution)