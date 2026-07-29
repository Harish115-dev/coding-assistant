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
    from assistant.llm import ask

    with console.status("[bold green]Thinking..."):
        reply = ask(message)

    console.print(reply)

@app.command()
def explain(
    error:str =typer.Argument(...,help="Paste the error message to explain."),)->None:
    """Chat with the assistant about your code."""
    from assistant.llm import ask

    prompt = (
        "Explain this error message in plain, simple terms for a developer. "
        "Say what likely caused it and how to fix it. Be concise.\n\n"
        f"Error:\n{error}")

    with console.status("[bold green]Thinking..."):
        reply = ask(prompt)

    console.print(reply)


@app.command()
def fix(file:str=typer.Argument(...,help="Path to the file with the bug."))->None:
    from pathlib import Path
    from assistant.llm import ask

    path = Path(file)
    if not path.exists():
        console.print(f"[red]File not found:[/red] {file}")
        raise typer.Exit(code=1)

    code = path.read_text()

    prompt = (
        "Here is a code file. Find any bugs and suggest a fix. "
        "Be concise and show the corrected code.\n\n"
        f"File: {file}\n```\n{code}\n```"
    )
    with console.status("[bold green]Thinking..."):
        reply = ask(prompt)

    console.print(reply)



if __name__ == "__main__":
    app()