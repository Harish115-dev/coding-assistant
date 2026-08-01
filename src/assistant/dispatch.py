from rich.console import Console

console = Console()


def _get_ask_fn(mode: str):
    if mode == "groq":
        from assistant.llm import ask
    elif mode == "openrouter":
        from assistant.openrouter_llm import ask
    else:
        from assistant.offline_llm import ask
    return ask


def get_reply(prompt: str, max_tokens: int = None) -> tuple[str, str]:
    """
    Resolve a mode, call the corresponding provider's ask(), and fall back to
    offline (Ollama) if the online call fails for any reason.

    Returns (reply, mode_actually_used) — mode_actually_used may differ from
    the originally-chosen mode if a fallback occurred, so callers can display
    the right thing and record usage against the right mode.
    """
    from assistant.router import choose_mode
    from assistant.offline_llm import is_ollama_running

    mode = choose_mode()
    ask = _get_ask_fn(mode)

    console.print(f"[dim]({mode} mode)[/dim]")

    with console.status("[bold green]Thinking..."):
        try:
            reply = ask(prompt, max_tokens=max_tokens) if max_tokens else ask(prompt)
        except Exception as e:
            if mode == "offline":
                # Already offline and it still failed — nothing left to fall back to.
                console.print(f"[red]Offline model failed:[/red] {e}")
                raise

            if is_ollama_running():
                console.print(
                    f"[yellow]{mode} request failed ({e}), falling back to offline mode[/yellow]"
                )
                mode = "offline"
                ask = _get_ask_fn(mode)
                reply = ask(prompt, max_tokens=max_tokens) if max_tokens else ask(prompt)
            else:
                console.print(f"[red]{mode} request failed:[/red] {e}")
                raise

    return reply, mode