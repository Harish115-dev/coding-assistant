import typer
from rich.console import Console
from rich.markdown import Markdown

console = Console()
app = typer.Typer()




@app.command()
def version() -> None:
    """Show the installed version."""
    console.print("coding-assistant v0.1.0")

#chat command


@app.command()
def chat(
    message: str = typer.Argument(..., help="What you want to ask the assistant."),
) -> None:
    """Chat with the assistant about your code."""
    from assistant.router import choose_mode
    from assistant.tokens import estimate_tokens, record_usage
    from assistant.rag import search

    mode = choose_mode()

    context_chunks = search(message)
    context = "\n\n".join(f"# From {c['source']}\n{c['text']}" for c in context_chunks)
    prompt = (
        f"Here is relevant context from the user's codebase:\n\n{context}\n\n"
        f"Question: {message}"
    )

    if mode == "groq":
        from assistant.llm import ask
    elif mode == "openrouter":
        from assistant.openrouter_llm import ask
    else:
        from assistant.offline_llm import ask

    console.print(f"[dim]({mode} mode)[/dim]")

    with console.status("[bold green]Thinking..."):
        reply = ask(prompt)

    if mode in ("groq", "openrouter"):
        record_usage(estimate_tokens(prompt) + estimate_tokens(reply))

    console.print(Markdown(reply))

#explain command

@app.command()
def explain(
    error: str = typer.Argument(..., help="Paste the error message to explain."),
) -> None:
    """Explain an error message in plain terms."""
    from assistant.router import choose_mode
    from assistant.tokens import estimate_tokens, record_usage
    from assistant.rag import search

    context_chunks = search(error)
    context = "\n\n".join(f"# From {c['source']}\n{c['text']}" for c in context_chunks)

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
        f"Relevant codebase context:\n{context}\n\n"
        f"Error:\n{error}"
    )

    console.print(f"[dim]({mode} mode)[/dim]")

    with console.status("[bold green]Thinking..."):
        reply = ask(prompt)

    if mode in ("groq", "openrouter"):
        record_usage(estimate_tokens(prompt) + estimate_tokens(reply))

    console.print(Markdown(reply))

#fix command
@app.command()
def fix(
    file: str = typer.Argument(..., help="Path to the file with the bug."),
    message: str = typer.Option(None, "--message", "-m", help="Extra instructions for the fix."),
) -> None:
    """Debug and suggest a fix for a file."""
    from pathlib import Path
    from assistant.router import choose_mode
    from assistant.tokens import estimate_tokens, record_usage
    from assistant.rag import search
    from assistant.codeblock import extract_code, make_diff
    import shutil

    path = Path(file)
    if not path.exists():
        console.print(f"[red]File not found:[/red] {file}")
        raise typer.Exit(code=1)

    code = path.read_text()

    context_chunks = search(code)
    context = "\n\n".join(f"# From {c['source']}\n{c['text']}" for c in context_chunks)

    mode = choose_mode()

    if mode == "groq":
        from assistant.llm import ask
    elif mode == "openrouter":
        from assistant.openrouter_llm import ask
    else:
        from assistant.offline_llm import ask

    extra_instruction = f"\nAdditional instructions from the user: {message}" if message else ""

    prompt = (
        "Here is a code file. Find any bugs and suggest a fix. "
        "Return the COMPLETE corrected file — do not use placeholders like '# ...' or "
        "'# rest unchanged' to skip any part of the file, even if unchanged. "
        "The full file must be included in your response."
        f"{extra_instruction}\n\n"
        f"Relevant codebase context:\n{context}\n\n"
        f"File: {file}\n```\n{code}\n```"
    )

    console.print(f"[dim]({mode} mode)[/dim]")

    with console.status("[bold green]Thinking..."):
        reply = ask(prompt)

    if mode in ("groq", "openrouter"):
        record_usage(estimate_tokens(prompt) + estimate_tokens(reply))

    console.print(Markdown(reply))

    fixed_code = extract_code(reply)
    if fixed_code is None:
        console.print("[yellow]No code block found in the response — nothing to apply.[/yellow]")
        return

    length_ratio = len(fixed_code) / max(len(code), 1)
    if length_ratio < 0.5:
        console.print(
            f"[bold red]Warning:[/bold red] the suggested fix is {int(length_ratio * 100)}% "
            "the length of your original file. This often means the model truncated or "
            "used placeholders instead of returning the full file."
        )

    diff = make_diff(code, fixed_code, file)
    if not diff.strip():
        console.print("[dim]No actual changes detected between original and suggested code.[/dim]")
        return

    console.print("\n[bold]Proposed changes:[/bold]")
    console.print(Markdown(f"```diff\n{diff}\n```"))

    apply = typer.confirm("\nApply this fix to the file?")
    if not apply:
        console.print("[dim]No changes made.[/dim]")
        return

    backup_path = path.with_suffix(path.suffix + ".bak")
    shutil.copy(path, backup_path)
    path.write_text(fixed_code)

    console.print(f"[green]Fix applied.[/green] Original backed up to {backup_path}")

#config command

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


@app.command()
def index(
    directory: str = typer.Argument(".", help="Directory to index (defaults to current folder)."),
) -> None:
    """Index a codebase so chat/fix/explain can use it as context."""
    from assistant.rag import index_directory

    with console.status("[bold green]Indexing codebase..."):
        count = index_directory(directory)

    console.print(f"[green]Indexed {count} chunks from {directory}[/green]")