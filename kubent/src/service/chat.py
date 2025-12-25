from openai import OpenAI

TITLE_PROMPT = "You are good at summarizing user's question in a simple and clear way. Your response should be as possible as less but more clear"

def title(message: str):
    openai_client = OpenAI()
    model = "openai/gpt-oss-120b:free"
    completion = openai_client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": TITLE_PROMPT}, {"role": "user", "content": message}]
    )
    return completion.choices[0].message.content
    