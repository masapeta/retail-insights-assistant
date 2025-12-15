from dotenv import load_dotenv
load_dotenv()

import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "openai/gpt-oss-120b"

def llm(prompt: str, system: str = None):
    messages=[]
    if system:
        messages.append({"role":"system","content":system})
    messages.append({"role":"user","content":prompt})
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"LLM Error: {e}"
