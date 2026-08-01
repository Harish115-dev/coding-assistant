import requests

OLLAMA_URL = "http://localhost:11434"

def is_ollama_running() -> bool:
    try:
        response = requests.get(OLLAMA_URL, timeout=2)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False


MODEL = "qwen2.5-coder:1.5b"

def ask(message: str, max_tokens: int = 500) -> str:
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": message}],
                "stream": False,
                "options": {"num_predict": max_tokens},
            },
            timeout=120,
        )
        response.raise_for_status()
        return response.json()["message"]["content"]
    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Couldn't reach Ollama at localhost:11434. Make sure Ollama is installed "
            "and running (try 'ollama serve'), or connect to the internet to use online mode instead."
        )