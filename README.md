<p align="center"><img src='./images/logo.webp'/></p>

# AI Trace
AI Trace: Track, log, and evaluate AI models. Supports OpenAI, Claude, Google API and custom PyTorch models.<br/>
Our goal is to make llm application more valuable and effortlessly improve llm capabilities.

# Quickstart
You can use pip install AT. (It's not implemented now.)
```bash
pip install aitrace
```
OR pip install from source.
```bash
git clone git@github.com:yanghui1-arch/AT.git
cd src
pip install -e .
```
Then you need to configure AT through CLI. (it can be ignored now. Skip it!)
```bash
aitrace configure
```

Finally use `@track` to track your llm input and output
```python
from aitrace import track
from openai import OpenAI

apikey = 'YOUR API KEY'


@track(
    project_name="aitrace_demo",
    tags=['test', 'demo'],
    track_llm=LLMProvider.OPENAI,    
)
def llm_classification(film_comment: str):
    prompt = "Please classify the film comment into happy, sad or others. Just tell me result. Don't output anything."
    cli = OpenAI(base_url='https://api.deepseek.com', api_key=apikey)
    cli.chat.completions.create(
        messages=[{"role": "user", "content": f"{prompt}\nfilm_comment: {film_comment}"}],
        model="deepseek-chat"
    ).choices[0].message.content
    llm_counts(film_comment=film_comment)
    return "return value"

@track(
    project_name="aitrace_demo",
    tags=['test', 'demo', 'second_demo'],
    track_llm=LLMProvider.OPENAI,
)
def llm_counts(film_comment: str):
    prompt = "Count the film comment words. just output word number. Don't output anything others."
    cli = OpenAI(base_url='https://api.deepseek.com', api_key=apikey)
    return cli.chat.completions.create(
        messages=[{"role": "user", "content": f"{prompt}\nfilm_comment: {film_comment}"}],
        model="deepseek-chat"
    ).choices[0].message.content

llm_classification("Wow! It sucks.")
```

Then it will output your llm trace. It is not supported to visualize now. I am developing it more and more quickly. Welcome to all contributions.

# Development
AT project package manager is uv. If you are a beginner uver, please click uv link: [uv official link](https://docs.astral.sh/uv/guides/projects/#creating-a-new-project)
```bash
cd src
uv install
uv .venv/Script/activate
```