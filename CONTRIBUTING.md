# Contributing to coding-assistant

Thanks for considering a contribution! This project is a hybrid online/offline
AI coding assistant, and contributions of any size are welcome.

## Getting started

```bash
git clone https://github.com/Harish115-dev/coding-assistant.git
cd coding-assistant
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -e ".[dev]"
cp .env.example .env
# add your GROQ_API_KEY and/or OPENROUTER_API_KEY to .env
```

## Running tests

```bash
pytest tests/
```

## Project structure
src/assistant/
├── cli.py # command definitions (chat, explain, fix, index, config)
├── router.py # decides online vs offline mode
├── llm.py # Groq client
├── openrouter_llm.py # OpenRouter client
├── offline_llm.py # Ollama client
├── rag.py # codebase indexing and semantic search
├── tokens.py # token estimation and budget tracking
├── config.py # settings and secrets
└── codeblock.py # code extraction, diffing, apply-to-file logic

## Making changes

1. Open an issue first for anything beyond a small fix, so we can discuss the approach
2. Add or update tests in `tests/` for any behavior change
3. Run `pytest tests/` before submitting — all tests should pass
4. Keep commits focused — one logical change per commit where possible

## Reporting bugs

Open a GitHub issue with:
- What you ran (the exact command)
- What you expected vs. what happened
- Your OS and Python version

## Questions?

Open an issue — happy to help.