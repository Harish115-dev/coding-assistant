import os
from pathlib import Path
from dotenv import load_dotenv

CONFIG_DIR = Path.home() / ".coding-assistant"

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")