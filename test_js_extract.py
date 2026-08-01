from assistant.codeblock import extract_code

sample = """Here's the fix:

```javascript
function add(a, b) {
    return a + b;
}
```

That should work."""

print(extract_code(sample))