import os
from dotenv import load_dotenv
import requests
from pathlib import Path

load_dotenv()
load_dotenv(Path.home() / ".coding-assistant" / ".env")


load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "meta-llama/llama-3.3-70b-instruct:free"

def ask(message: str, max_tokens: int = 500) -> str:
    if not OPENROUTER_API_KEY:
        raise ValueError(
            "OPENROUTER_API_KEY not found. Add it to your .env file — get one free at openrouter.ai/keys"
        )

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}"},
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": message}],
            "max_tokens": max_tokens,
        },
        timeout=60,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]