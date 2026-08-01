from assistant.tokens import estimate_tokens


def test_estimate_tokens_short_text():
    assert estimate_tokens("hello world") == 2


def test_estimate_tokens_scales_with_length():
    assert estimate_tokens("a" * 1000) == 250


def test_estimate_tokens_empty_string():
    assert estimate_tokens("") == 0