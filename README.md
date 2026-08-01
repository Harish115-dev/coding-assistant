# coding-assistant

A hybrid online/offline AI coding assistant. Uses free cloud LLMs (Groq or
OpenRouter) for strong reasoning, and falls back to a local model via
[Ollama](https://ollama.com) when you're offline or want to avoid rate limits.
Understands your actual codebase through built-in RAG — no need to paste
code by hand. Can also apply suggested fixes directly to your files, with a
diff preview and automatic backup before anything is overwritten.

Status: **Core functionality complete and tested.** Chat, fix, explain,
codebase indexing, multi-provider support, token budgeting, safe file-apply,
and global installation are all working end to end.

## Demo

![demo](demo.gif)

*Asking the assistant to explain an error, then fixing a bug directly in a file with a diff preview before applying.*

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

## Installing it: local vs. global

There are two ways to use this tool, and it matters which one you pick.

### Local only (what the Quick Start above gives you)

Following the Quick Start means `assistant` **only works from inside this
project's own folder**, and only while its `.venv` is activated. Your `.env`
file must also live in this same folder. This is fine if you only ever want
to use the assistant on this one project, or while developing the assistant
itself.

### Global — works from any project, any terminal

To use `assistant` on other projects too (a frontend app, a backend API,
anything else on your machine, or even no project at all) without activating
this project's `.venv` every time, install it globally instead.

**Step 1 — install pipx (one-time setup):**

```bash
pip install pipx
pipx ensurepath
```

Close and reopen your terminal after this — PATH changes need a fresh session.

**Step 2 — install the assistant globally:**

```bash
cd coding-assistant
pipx install .
```

**Step 3 — set up your API keys in the global config location** (not the
project's local `.env` — this one is read no matter which folder you're in):

```bash
notepad %USERPROFILE%\.coding-assistant\.env    # Windows
```

Notepad will offer to create the file — say yes, then paste:
GROQ_API_KEY=your_actual_key_here
OPENROUTER_API_KEY=your_actual_key_here
Save and close.

**Step 4 — use it anywhere:**

```bash
cd ~/projects/my-frontend-app
assistant index
assistant chat "how should I structure my components folder?"

cd ~/projects/my-backend-api
assistant index
assistant chat "why is this endpoint returning 500?"
```

Both online and offline modes work regardless of which folder you're in —
online just needs internet, offline just needs Ollama running in the
background, neither depends on being inside any particular project.

Each project you run `assistant index` in gets its own isolated codebase
index — working across multiple projects never mixes their code together.
Folders you haven't indexed simply have no extra context to pull in yet;
the assistant still answers normally, just without codebase-specific detail.

**Updating after code changes:** if you pull new changes or edit the
assistant's own source, refresh the global install with:

```bash
cd coding-assistant
pipx install . --force
```

## Codebase-aware answers (RAG)

Index your project so the assistant can pull in relevant context automatically:

```bash
assistant index
```

Then `chat`, `explain`, and `fix` will all search your indexed codebase and
include relevant snippets before answering — so questions about your own
code get real, specific answers instead of generic ones. Supports Python,
Markdown, JavaScript, TypeScript, JSON, HTML, and CSS files.

## Fixing code safely

```bash
assistant fix buggy.py
assistant fix buggy.py -m "only fix the search function, don't change anything else"
```

`fix` shows you a diff of the proposed change before touching anything, warns
if the suggested fix looks suspiciously truncated, and backs up the original
file to `<file>.bak` before applying — nothing gets overwritten without your
explicit confirmation.

## Diagnosing issues (read-only)

```bash
assistant explain "IndexError: list index out of range"
assistant explain -f buggy.py                # scan a whole file for bugs
assistant explain "some error" -f buggy.py   # correlate an error with a file
```

`explain` never writes to files — it's purely for understanding what's wrong.
Use `fix` when you actually want changes applied.

## Commands

```bash
assistant chat "<message>"                     # ask the assistant anything
assistant explain "<error>"                    # explain an error message
assistant explain -f <file>                    # scan a file for bugs (read-only)
assistant explain "<error>" -f <file>          # correlate an error with a file
assistant fix <file>                           # find bugs, show a diff, optionally apply
assistant fix <file> -m "<instructions>"       # same, with extra guidance
assistant index [directory]                    # index a codebase for RAG
assistant config show                          # view current settings
assistant config set                           # update preferences
assistant version                              # show installed version
assistant commands                             # list all commands
```

## Configuration

```bash
assistant config show
assistant config set --provider openrouter        # or "groq"
assistant config set --daily-budget-cap 50000     # tokens/day before forcing offline
```

## Development

```bash
pip install -e ".[dev]"
pytest tests/
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for more.

## Roadmap

- [x] Phase 0 — repo, CLI skeleton, config
- [x] Phase 1 — online MVP (`chat`, `fix`, `explain`)
- [x] Phase 2 — offline mode + router
- [x] Phase 3 — token budgeting
- [x] Phase 4 — codebase RAG (ChromaDB), multi-extension indexing
- [x] Multi-provider support — Groq + OpenRouter, switchable via config
- [x] Safe file-apply for `fix` — diff preview, backup, truncation guard
- [x] Per-project RAG isolation — each project gets its own codebase index
- [x] Global installation via pipx, with shared global config/keys
- [x] Test suite (pytest)
- [ ] Phase 7 — VS Code extension (stretch goal)

## License

MIT