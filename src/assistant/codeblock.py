import difflib
import re

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