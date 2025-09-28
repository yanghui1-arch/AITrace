<p align="center"><img src='./images/logo.webp'/></p>

# AI Trace
AI Trace: Track, log, and evaluate AI models. Supports OpenAI, Claude, Google API and custom PyTorch models.<br/>
Our goal is to make llm application more valuable and effortlessly improve llm capabilities.

# Quickstart
You can use pip install AT.
```bash
pip install aitrace
```
OR pip install from source.
```bash
git clone git@github.com:yanghui1-arch/AT.git
cd src
pip install -e .
```
Then you need to configure AT through CLI.
```bash
aitrace configure
```

Finally use `@track` to track your llm input and output
```python
from aitrace import track
from openai import OpenAI

class LLMClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        self._client = OpenAI(base_url=base_url, api_key=api_key)

    @track
    def plan(self, messages:list[dict], model:str) -> str:
        return self._client.chat.completions.create(messages=messages, model=model).choices[0].message.content
    
    @track
    def think(self, messages:list[dict], model:str) -> str:
        return self._client.chat.completions.create(messages=messages, model=model).choices[0].message.content

llm_client = LLMClient(base_url, api_key)

plan_result = llm_clinet.plan([
    {"role": "system", "content": "You are a good assistant."},
    {"role": "user", "content": "How to order a plane ticket?"}
], model="gpt-3.5-turbo-latest")

think_result = llm_clinet.think([
    {"role": "system", "content": "You are a good assistant."},
    {"role": "user", "content": "How to order a plane ticket?"},
    {"role": "assistant", "content": plan_result},
    {"role": "user", "content": "think one of plan."}
], model="gpt-3.5-turbo-latest")
```

# Development
AT project package manager is uv. If you are a beginner uver, please click uv link: [uv official link](https://docs.astral.sh/uv/guides/projects/#creating-a-new-project)
```bash
cd src
uv install
uv .venv/Script/activate
```