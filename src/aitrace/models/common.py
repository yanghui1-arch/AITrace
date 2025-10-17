from enum import Enum

class LLMProvider(Enum):
    OPENAI = 'openai'
    GOOGLE = 'google'
    ANTHROPIC = 'anthropic'
    DEEPSEEK = 'deepseek'
    QWEN = 'qwen'
    OLLAMA = 'ollama'
