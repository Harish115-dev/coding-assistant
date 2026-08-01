from assistant.config import get_groq_client
MODEL = "llama-3.3-70b-versatile"

def ask(message: str, max_tokens: int = 500) -> str:
    client = get_groq_client()
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": message}],
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content
