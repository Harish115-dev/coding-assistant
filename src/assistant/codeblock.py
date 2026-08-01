
import re
def extract_code(text: str) -> str | None:
    matches = re.findall(r"```(?:python)?\n(.*?)```", text, re.DOTALL)
    if not matches:
        return None
    return max(matches, key=len).strip()