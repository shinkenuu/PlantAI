# CLAUDE.md — PlantAI

> Context file for AI coding assistants (Claude, Copilot, etc.).
> Keep this up to date as the project evolves.

---

## What this project is

PlantAI is a LangGraph-based AI agent that monitors houseplants through an Arduino
sensor rig and answers natural-language questions about their health. The agent
(called **Demeter**) can read sensor data, query external plant databases, and
converse about care routines. It runs locally against Ollama or an OpenAI-compatible
endpoint.

---

## Repo layout

```
plantai/
├── agents/
│   └── demeter.py       # LangGraph agent — the core of the system
├── plants/
│   ├── models.py        # Plant domain models (Pydantic)
│   └── repository.py   # File / Arduino / MongoDB backends
├── llms.py              # LLM factory helpers (get_ollama_llm, get_openai_llm)
config.py                # pydantic-settings Settings singleton (reads .env)
prototype.py             # Dev entrypoint — talks to Demeter via text prompt
orange.py                # Alt entrypoint — passes explicit LLM + state dict
Makefile                 # lint / test shortcuts
pyproject.toml           # Project metadata, deps, optional extras
.env.example             # Copy to .env and fill in credentials
```

---

## Environment setup

```bash
# 1. Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Clone and sync dependencies
git clone https://github.com/shinkenuu/PlantAI
cd PlantAI
uv sync                        # core deps only
uv sync --extra ollama         # + Ollama LangChain integration
uv sync --extra openai         # + OpenAI LangChain integration
uv sync --extra tracing        # + Opik observability
uv sync --group dev            # + dev tools (pytest, ruff, mypy, deepeval)

# 3. Configure secrets — never edit config.py directly
cp .env.example .env
$EDITOR .env                   # fill in DODDER_DATABASE_URI, API keys, etc.

# 4. Smoke test
uv run python prototype.py
```

All configuration is read from `.env` via `config.py` → `Settings` (pydantic-settings).
**Do not hardcode credentials anywhere in source.**

---

## Configuration reference

All values are set via environment variables (or `.env`). The authoritative list
lives in `config.py`; this table is a quick reference.

| Variable | Default | Description |
|---|---|---|
| `REPOSITORY_BACKEND` | `file` | `file` · `arduino` · (future: `mongodb`) |
| `FILE_REPOSITORY_JSON_PATH` | `./plants/io/local_plants.json` | Plant data for the file backend |
| `ARDUINO_REPOSITORY_JSON_PATH` | `./plants/io/arduino.json` | Sensor JSON written by the Arduino sketch |
| `OPENAI_BASE_URL` | `http://127.0.0.1:8080/v1` | OpenAI-compatible endpoint (e.g. LM Studio) |
| `OLLAMA_BASE_URL` | `http://127.0.0.1:11434` | Ollama server |
| `TREFLE_API_KEY` | _(none)_ | Trefle plant database API key |
| `PERENUAL_API_KEY` | _(none)_ | Perenual plant database API key |
| `DODDER_DATABASE_URI` | _(none — required in prod)_ | MongoDB connection URI |

---

## Common tasks

```bash
# Lint + autofix
make lint
# equivalent: uv tool run ruff check . --fix && uv tool run ruff format .

# Run plant unit tests (no hardware, no LLM calls)
make test-plants
# equivalent: uv run pytest -vvv tests/plants -m "not arduino"

# Run agent evals (requires deepeval, no Arduino)
make test-agents
# equivalent: DEEPEVAL_TELEMETRY_OPT_OUT=YES uv run deepeval test run tests/plantai/agents -vv

# Type check
uv run mypy plantai config.py --ignore-missing-imports

# Run the main agent interactively
uv run python prototype.py

# Run the low-level agent with an explicit LLM + state dict
uv run python orange.py
```

---

## Architecture

```
User prompt
    │
    ▼
demeter.talk(prompt)          # prototype.py entrypoint
    │
    ▼
LangGraph agent (Demeter)
    ├── reads plant state      via PlantRepository (file | arduino | mongo)
    ├── calls tools            Trefle API · Perenual API · sensor reads
    └── streams answer         back to caller
```

**Key design decisions:**

- **LangGraph for orchestration.** The agent graph lives in `plantai/agents/demeter.py`.
  Nodes are pure functions; state is a typed `TypedDict`. Add new capabilities by
  adding nodes and edges — don't mutate the graph at runtime.

- **Two entrypoints, one agent API.** `prototype.py` calls `demeter.talk(prompt, trace=True)`;
  `orange.py` calls `demeter.talk(thread_id=..., llm=..., state=...)`. These exercise
  different code paths. The canonical public signature lives in `demeter.py` — keep
  both callers in sync when you change it.

- **Repository pattern for plant I/O.** `PlantRepository` is an abstract base;
  concrete backends live in the same file. Swap `REPOSITORY_BACKEND` in `.env`
  to switch without touching agent code.

- **Opik for tracing.** Import-time tracing decorators are applied when `trace=True`
  is passed. Requires `uv sync --extra tracing`. Opt out by leaving `PERENUAL_API_KEY`
  and `TREFLE_API_KEY` empty — the agent degrades gracefully.

---

## Test markers

| Marker | Meaning | Requires |
|---|---|---|
| _(no marker)_ | Pure unit test | Nothing |
| `arduino` | Reads from real serial port | Connected Arduino |
| `llm` | Makes real LLM calls | Running Ollama / OpenAI endpoint |

Always skip `arduino` and `llm` in CI:
```bash
uv run pytest -m "not arduino and not llm"
```

---

## Adding a new plant tool (agent capability)

1. Create `plantai/tools/my_tool.py` with a `@tool`-decorated function.
2. Import and register it in the Demeter graph in `plantai/agents/demeter.py`.
3. Add a unit test in `tests/plants/` or `tests/plantai/agents/` depending on scope.
4. If the tool needs a new API key, add it to `Settings` in `config.py` and `.env.example`.

---

## Conventions

- **Formatter / linter:** `ruff` (check + format). Run `make lint` before committing.
  Config lives in `pyproject.toml` under `[tool.ruff]` (add it if not present).
- **Type hints:** All public functions in `plantai/` must have full type annotations.
  Run `mypy` to verify.
- **No secrets in source.** All credentials go in `.env` (gitignored). Use `Settings`
  from `config.py` to access them.
- **No top-level side effects.** Scripts (`prototype.py`, `orange.py`) must guard
  runnable code with `if __name__ == "__main__"`.
- **Commit style:** conventional commits preferred (`feat:`, `fix:`, `chore:`, etc.).

---

## External dependencies worth knowing

| Package | Why it's here |
|---|---|
| `langgraph` | Agent orchestration graph |
| `langchain-ollama` | Ollama LLM integration (optional extra) |
| `langchain-openai` | OpenAI-compatible LLM integration (optional extra) |
| `pydantic` / `pydantic-settings` | Data models + typed config from env |
| `pyserial` | Arduino serial communication |
| `pymongo` | MongoDB plant persistence |
| `opik` | LLM call tracing / observability (optional extra) |
| `deepeval` | Agent evaluation framework (dev only) |
| `ruff` | Linter + formatter (dev only) |
| `mypy` | Static type checker (dev only) |

---

## Known sharp edges

- **`orange.py` and `prototype.py` use different `demeter.talk()` call signatures.**
  Both are intentional (different invocation modes) but fragile — if you change the
  agent API, update both callers and the docstring in `demeter.py`.
- **Arduino backend is synchronous and blocks.** Don't call it from async contexts
  without wrapping in `asyncio.to_thread`.
- **`DODDER_DATABASE_URI` has a default with dummy credentials in `config.py`.**
  This is a dev convenience only. In any deployed environment, set the env var
  explicitly — do not rely on the default.