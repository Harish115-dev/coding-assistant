from assistant.codeblock import extract_code


def test_extract_code_python_tagged():
    text = "Here:\n```python\nprint(1)\n```\nDone."
    assert extract_code(text) == "print(1)"


def test_extract_code_javascript_tagged():
    text = "Here:\n```javascript\nconsole.log(1);\n```\nDone."
    assert extract_code(text) == "console.log(1);"