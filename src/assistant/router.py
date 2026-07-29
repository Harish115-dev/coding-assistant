import socket
from assistant.offline_llm import is_ollama_running

def is_online() -> bool:
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False

def choose_mode() -> str:
    if is_online():
        return "online"  
    if is_ollama_running():
        return "offline" 
    
    raise RuntimeError(
        "No internet connection and Ollama isn't running. "
        "Start Ollama or connect to the internet to use the assistant."
    )
