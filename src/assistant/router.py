import socket
from assistant.offline_llm import is_ollama_running
from assistant.tokens import get_today_usage
from assistant.config import get_daily_budget_cap



def is_online() -> bool:
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False

def choose_mode() -> str:
    cap = get_daily_budget_cap()
    if get_today_usage() >=cap:
        if is_ollama_running():
            return "offline"
        raise RuntimeError(
            f"Daily budget cap ({cap} tokens) reached, "
            "and Ollama isn't running to fall back to. Start Ollama or wait until tomorrow."
        )

    if is_online():
        return "online"  
    if is_ollama_running():
        return "offline" 
    
    raise RuntimeError(
        "No internet connection and Ollama isn't running. "
        "Start Ollama or connect to the internet to use the assistant."
    )
