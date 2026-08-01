from assistant.codeblock import make_diff

original = "def add(a, b):\n    return a - b\n"
fixed = "def add(a, b):\n    return a + b\n"

print(make_diff(original, fixed, "example.py"))