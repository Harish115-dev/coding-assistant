import os
from dotenv import load_dotenv
import requests


load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "openrouter/free"


def ask(message: str) -> str:
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
    "max_tokens": 500,
},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]