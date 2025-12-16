import json
from typing import Literal, List, Dict, Callable
from pydantic import BaseModel
from openai.types.chat import ChatCompletionMessage, ChatCompletionMessageToolCallUnion

class Action(BaseModel):
    func: Callable
    type: Literal['think', 'search', 'command', 'general_function'] = 'general_function'
    
    def is_search(self):
        return self.type == 'search'
    
    def is_command(self):
        return self.type == 'command'
    
    def is_general_function(self):
        return self.type == 'general_function'
    
    def is_think(self):
        return self.type == 'think'

class Env(BaseModel):
    action_spaces: Dict[str, Action]
    _chains: List[Dict[str, str]] = []
    steps: int = 0
    num_tool_callings: int = 0
    num_search: int = 0
    obs: str
    answer: str | None = None

    def reset(self) -> str:
        self.steps = 0
        self.num_search = 0
        self.num_tool_callings = 0
        self.obs = ""
        self.answer =  None
        return self.obs
    
    def step(self, llm_action: ChatCompletionMessage, terminate_signal: str | None = None) -> tuple[str, float, bool, Dict[str, str]]:
        reward = 0
        terminate = False
        if terminate_signal is None:
            terminate_signal = "[Finish]"

        content:str | None = llm_action.content
        tool_calls:List[ChatCompletionMessageToolCallUnion] | None = llm_action.tool_calls
        if content is not None:
            if content.startswith(terminate_signal):
                terminate = True
                self.answer = content[len(terminate_signal): ]
                self.obs += f"[Finish] {self.answer}"
                self._chains.append(
                    {"action_name": "<finish>", "action_result": f"[Finish] {self.answer}"}
                )
                return self.obs, reward, terminate, self._get_info()
            else:
                self.obs = f"[Think #{self.steps}] {content}" + "\n"
                self._chains.append(
                    {"action_name": "<think>", "action_result": f"[Think #{self.steps}] {content}" + "\n"}
                )
                return self.obs, reward, terminate, self._get_info()

        if tool_calls is not None:
            for tool_call in tool_calls:
                tool_name = tool_call.function.name
                act:Action = self.action_spaces.get(tool_name, None)
                if act is not None:
                    func = act.func
                    arguments = tool_call.function.arguments
                    self.obs += f"[Action #{self.num_tool_callings}] Execute tool \"{tool_name}\" with arguments {arguments}" + "\n"
                    result = "None"
                    try:
                        arguments_json: Dict = json.loads(arguments)
                        result = func(**arguments_json)
                        result_str = str(result)
                        self.obs += f"[Observation #{self.num_tool_callings}] Execute tool {tool_name}. Result: {result_str}" + "\n"
                    except json.JSONDecodeError as jde:
                        self.obs += f"[Observation #{self.num_tool_callings}] Failed to execute tool {self.num_tool_callings} in step {self.steps}, which tool name is {tool_name}, because argument is not a valid json. Invalid arguments: {arguments}" + "\n"
                        result = "Invalid arguments."
                    finally:
                        self.num_tool_callings += 1
                        self._chains.append(
                            {"action_name": tool_name, "action_result": result}
                        )
                else:
                    self.obs += f"[Observation #{self.num_tool_callings}] Call invaild tool: {tool_name} which can not found in agent action space." + "\n"
                    self.num_tool_callings += 1
                    self._chains.append(
                        {"action_name": tool_name, "action_result": f"[Observation #{self.num_tool_callings}] Call invaild tool: {tool_name} which can not found in agent action space." + "\n"}
                    )

        return self.obs, reward, terminate, self._get_info()

    def _get_info(self):
        return {"steps": self.steps, "num_tool_callings": self.num_tool_callings, "answer": self.answer}
