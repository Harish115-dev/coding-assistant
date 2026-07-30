import json
from datetime import date
from pathlib import Path


def estimate_tokens(text: str) -> int:
    return len(text) // 4

USAGE_FILE = Path.home() / ".coding-assistant" / "usage.json"

def _load_usage()->dict:
    if not USAGE_FILE.exists():
        return {}
    try:
        with open(USAGE_FILE, "r") as f:
            return json.load(f)
        
    except (json.JSONDecodeError, OSError):
        return {}

def record_usage(tokens:int)->None:
    usage=_load_usage()
    today = str(date.today())
    usage[today] = usage.get(today, 0) + tokens

    USAGE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(USAGE_FILE, "w") as f:
        json.dump(usage, f, indent=2)


def get_today_usage() -> int:
    usage = _load_usage()
    return usage.get(str(date.today()), 0)

    