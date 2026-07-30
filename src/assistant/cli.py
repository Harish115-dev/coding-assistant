import typer
from rich.console import Console

console = Console()
app = typer.Typer()




@app.command()
def version() -> None:
    """Show the installed version."""
    console.print("coding-assistant v0.1.0")


@app.command()
def chat(
    message:str =typer.Argument(...,help="What you want to ask the assistant."),)->None:
    """Chat with the assistant about your code."""
    from assistant.router import choose_mode
    from assistant.tokens import estimate_tokens, record_usage
    mode = choose_mode()


    if mode == "groq":
        from assistant.llm import ask
    elif mode == "openrouter":
        from assistant.openrouter_llm import ask
    else:
        from assistant.offline_llm import ask

    console.print(f"[dim]({mode} mode)[/dim]")

    with console.status("[bold green]Thinking..."):
        reply = ask(message)
    if mode in ("groq", "openrouter"):
        record_usage(estimate_tokens(message) + estimate_tokens(reply))
    console.print(reply)


@app.command()
def explain(
    error: str = typer.Argument(..., help="Paste the error message to explain."),
) -> None:
    """Explain an error message in plain terms."""
    from assistant.router import choose_mode
    from assistant.tokens import estimate_tokens, record_usage  

    mode = choose_mode()
    if mode == "groq":
        from assistant.llm import ask
    elif mode == "openrouter":
        from assistant.openrouter_llm import ask
    else:
        from assistant.offline_llm import ask

    prompt = (
        "Explain this error message in plain, simple terms for a developer. "
        "Say what likely caused it and how to fix it. Be concise.\n\n"
        f"Error:\n{error}"
    )

    console.print(f"[dim]({mode} mode)[/dim]")

    with console.status("[bold green]Thinking..."):
        reply = ask(prompt)

    if mode in ("groq", "openrouter"): 
        record_usage(estimate_tokens(prompt) + estimate_tokens(reply))

    console.print(reply)



@app.command()
def fix(
    file: str = typer.Argument(..., help="Path to the file with the bug."),
) -> None:
    """Debug and suggest a fix for a file."""
    from pathlib import Path
    from assistant.router import choose_mode
    from assistant.tokens import estimate_tokens, record_usage  


    path = Path(file)
    if not path.exists():
        console.print(f"[red]File not found:[/red] {file}")
        raise typer.Exit(code=1)

    code = path.read_text()

    mode = choose_mode()

    if mode == "groq":
        from assistant.llm import ask
    elif mode == "openrouter":
        from assistant.openrouter_llm import ask
    else:
        from assistant.offline_llm import ask

    prompt = (
        "Here is a code file. Find any bugs and suggest a fix. "
        "Be concise and show the corrected code.\n\n"
        f"File: {file}\n```\n{code}\n```"
    )

    console.print(f"[dim]({mode} mode)[/dim]")

    with console.status("[bold green]Thinking..."):
        reply = ask(prompt)
    
    if mode in ("groq", "openrouter"): 
        record_usage(estimate_tokens(prompt) + estimate_tokens(reply))

    console.print(reply)




config_app = typer.Typer(help="View or update assistant preferences.")
app.add_typer(config_app, name="config")

@config_app.command("set")
def config_set(
    daily_budget_cap: int = typer.Option(None, help="Max tokens/day before forcing offline mode."),
    provider: str = typer.Option(None, help="Online provider: groq or openrouter"),
) -> None:
    """Update assistant preferences."""
    from assistant.config import set_daily_budget_cap, set_provider

    if daily_budget_cap is not None:
        set_daily_budget_cap(daily_budget_cap)
        console.print(f"[green]daily_budget_cap set to {daily_budget_cap}[/green]")

    if provider is not None:
        set_provider(provider)
        console.print(f"[green]provider set to {provider}[/green]")
    
@config_app.command("show")
def config_show() -> None:
    """Show current preferences."""
    from assistant.config import get_daily_budget_cap, get_provider

    console.print(f"daily_budget_cap: {get_daily_budget_cap()}")
    console.print(f"provider: {get_provider()}")
@app.command()
def commands() -> None:
    """List all available commands."""
    from rich.table import Table

    table = Table(title="coding-assistant commands")
    table.add_column("Command", style="cyan")
    table.add_column("Description")

    table.add_row("chat \"<message>\"", "Chat with the assistant about your code")
    table.add_row("explain \"<error>\"", "Explain an error message in plain terms")
    table.add_row("fix <file>", "Debug and suggest a fix for a file")
    table.add_row("version", "Show the installed version")
    table.add_row("commands", "List all available commands")
    table.add_row("config show", "Show current preferences")
    table.add_row("config set", "Update preferences (--provider, --daily-budget-cap)")

    console.print(table)