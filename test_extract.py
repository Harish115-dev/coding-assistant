from assistant.codeblock import extract_code

sample = """Here's the fix:

```python
def add(a, b):
    return a + b
```

That should work."""

print(extract_code(sample))