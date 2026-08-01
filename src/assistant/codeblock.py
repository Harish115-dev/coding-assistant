import difflib
import re
from pathlib import Path
import shutil
import typer
from rich.console import Console
from rich.markdown import Markdown

console = Console()

# extracting code

def extract_code(text: str) -> str | None:
    matches = re.findall(r"```(?:python)?\n(.*?)```", text, re.DOTALL)
    if not matches:
        return None
    return max(matches, key=len).strip()

def make_diff(original:str,fixed:str,filename:str="file")->str:
    original_lines=original.splitlines(keepends=True)
    fixed_lines=fixed.splitlines(keepends=True)
    diff = difflib.unified_diff(
        original_lines,
        fixed_lines,
        fromfile=f"{filename} (original)",
        tofile=f"{filename} (fixed)",
    )
    return "".join(diff)



def offer_to_apply(path: Path, reply: str) -> None:
    original_code = path.read_text()
    fixed_code = extract_code(reply)

    if fixed_code is None:
        return

    length_ratio = len(fixed_code) / max(len(original_code), 1)
    if length_ratio < 0.5:
        console.print(
            f"[bold red]Warning:[/bold red] the suggested code is {int(length_ratio * 100)}% "
            "the length of the original file. This often means the model truncated or "
            "used placeholders instead of returning the full file."
        )

    diff = make_diff(original_code, fixed_code, str(path))
    if not diff.strip():
        return

    console.print("\n[bold]Proposed changes:[/bold]")
    console.print(Markdown(f"```diff\n{diff}\n```"))

    apply = typer.confirm(f"\nApply this to {path}?")
    if not apply:
        console.print("[dim]No changes made.[/dim]")
        return

    backup_path = path.with_suffix(path.suffix + ".bak")
    shutil.copy(path, backup_path)
    path.write_text(fixed_code)

    console.print(f"[green]Applied.[/green] Original backed up to {backup_path}")