# coding-assistant

A hybrid online/offline AI coding assistant. Uses free cloud LLMs (Groq or
OpenRouter) for strong reasoning, and falls back to a local model via
[Ollama](https://ollama.com) when you're offline or want to avoid rate limits.
Understands your actual codebase through built-in RAG — no need to paste
code by hand.

Status: **Phase 6 — polish.** Core functionality (chat, fix, explain,
codebase indexing, multi-provider support, token budgeting) is complete and
working.

## Quick start

```bash
git clone https://github.com/Harish115-dev/coding-assistant.git
cd coding-assistant
pip install -e .
```

### Online mode (needs a free API key)

```bash
cp .env.example .env
# edit .env and add GROQ_API_KEY and/or OPENROUTER_API_KEY
assistant chat "why does this function throw a KeyError?"
```

Get a free key at [console.groq.com/keys](https://console.groq.com/keys) or
[openrouter.ai/keys](https://openrouter.ai/keys) — no card required for either.

### Offline mode (needs Ollama)

```bash
# install Ollama from https://ollama.com, then:
ollama pull qwen2.5-coder
assistant chat "why does this function throw a KeyError?"
```

The assistant automatically falls back to your local Ollama model when
there's no internet connection or your daily token budget is used up.

## Codebase-aware answers (RAG)

Index your project so the assistant can pull in relevant context automatically:

```bash
assistant index
```

Then `chat`, `explain`, and `fix` will all search your indexed codebase and
include relevant snippets before answering — so questions about your own
code get real, specific answers instead of generic ones.

## Commands

```bash
assistant chat "<message>"       # ask the assistant anything
assistant explain "<error>"      # explain an error message in plain terms
assistant fix <file>             # find and fix bugs in a file
assistant index [directory]      # index a codebase for RAG (defaults to current folder)
assistant config show            # view current settings
assistant config set             # update preferences (--provider, --daily-budget-cap)
assistant version                # show installed version
assistant commands                # list all commands
```

## Configuration

```bash
assistant config show
assistant config set --provider openrouter        # or "groq"
assistant config set --daily-budget-cap 50000     # tokens/day before forcing offline
```

## Roadmap

- [x] Phase 0 — repo, CLI skeleton, config
- [x] Phase 1 — online MVP (`chat`, `fix`, `explain`)
- [x] Phase 2 — offline mode + router
- [x] Phase 3 — token budgeting
- [x] Phase 4 — codebase RAG (ChromaDB), multi-extension indexing
- [x] Multi-provider support — Groq + OpenRouter, switchable via config
- [ ] Phase 6 — packaging + polish (in progress)
- [ ] Phase 7 — VS Code extension (stretch goal)

## License

MIT