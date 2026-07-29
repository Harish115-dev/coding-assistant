import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

CONFIG_DIR = Path.home() / ".coding-assistant"

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_groq_client() -> Groq:
    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY not found. Add it to your .env file — get one free at console.groq.com/keys"
        )
    return Groq(api_key=GROQ_API_KEY)

