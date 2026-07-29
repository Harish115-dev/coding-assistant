# coding-assistant

A hybrid online/offline AI coding assistant. Works with a cloud LLM when you
want the strongest reasoning, and falls back to a local model via
[Ollama](https://ollama.com) when you're offline or want to avoid token costs.

Status: **Phase 0 — project scaffolding.** Commands below are stubs; real
functionality lands in Phase 1 onward.

## Quick start

```bash
git clone <your-repo-url>
cd coding-assistant
pip install -e .
```

### Online mode (needs an API key)

```bash
cp .env.example .env
# edit .env and add your GROQ_API_KEY
assistant chat "why does this function throw a KeyError?"
```

### Offline mode (needs Ollama)

```bash
# install Ollama from https://ollama.com, then:
ollama pull qwen2.5-coder
assistant chat "why does this function throw a KeyError?"
```

## Configuration

```bash
assistant config show          # view current settings
assistant config set --mode-preference offline_first
```

## Roadmap

- [x] Phase 0 — repo, CLI skeleton, config
- [ ] Phase 1 — online MVP (`chat`, `fix`, `explain`)
- [ ] Phase 2 — offline mode + router
- [ ] Phase 3 — token budgeting
- [ ] Phase 4 — codebase RAG (ChromaDB)
- [ ] Phase 5 — confidence-based escalation
- [ ] Phase 6 — packaging + polish
- [ ] Phase 7 — VS Code extension

## License

MIT
