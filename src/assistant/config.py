import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

CONFIG_DIR = Path.home() / ".coding-assistant"

load_dotenv()  # local .env, if present (useful during development)
load_dotenv(CONFIG_DIR / ".env")  # global .env, for when installed globally via pipx

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def get_groq_client() -> Groq:
    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY not found. Add it to your .env file — get one free at console.groq.com/keys"
        )
    return Groq(api_key=GROQ_API_KEY)


import json

PREFS_FILE = CONFIG_DIR / "preferences.json"
DEFAULT_DAILY_BUDGET_CAP = 50000


def get_daily_budget_cap() -> int:
    if not PREFS_FILE.exists():
        return DEFAULT_DAILY_BUDGET_CAP
    try:
        with open(PREFS_FILE, "r") as f:
            prefs = json.load(f)
        return prefs.get("daily_budget_cap", DEFAULT_DAILY_BUDGET_CAP)
    except (json.JSONDecodeError, OSError):
        return DEFAULT_DAILY_BUDGET_CAP


def set_daily_budget_cap(cap: int) -> None:
    prefs = {}
    if PREFS_FILE.exists():
        try:
            with open(PREFS_FILE, "r") as f:
                prefs = json.load(f)
        except (json.JSONDecodeError, OSError):
            prefs = {}
    prefs["daily_budget_cap"] = cap

    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(PREFS_FILE, "w") as f:
        json.dump(prefs, f, indent=2)


def get_provider() -> str:
    if not PREFS_FILE.exists():
        return "groq"
    try:
        with open(PREFS_FILE, "r") as f:
            prefs = json.load(f)
        return prefs.get("provider", "groq")
    except (json.JSONDecodeError, OSError):
        return "groq"


def set_provider(provider: str) -> None:
    valid = {"groq", "openrouter"}
    if provider not in valid:
        raise ValueError(f"provider must be one of {valid}, got '{provider}'")

    prefs = {}
    if PREFS_FILE.exists():
        try:
            with open(PREFS_FILE, "r") as f:
                prefs = json.load(f)
        except (json.JSONDecodeError, OSError):
            prefs = {}
    prefs["provider"] = provider

    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(PREFS_FILE, "w") as f:
        json.dump(prefs, f, indent=2)