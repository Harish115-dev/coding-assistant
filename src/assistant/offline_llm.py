import requests

OLLAMA_URL = "http://localhost:11434"

def is_ollama_running() -> bool:
    try:
        response = requests.get(OLLAMA_URL, timeout=2)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False


MODEL = "qwen2.5-coder:1.5b"

def ask(message:str)->str:
    response=requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": message}],
            "stream": False,
        },
        timeout=120,
    )
    response.raise_for_status()
    return response.json()["message"]["content"]