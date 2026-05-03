# plantai — Agent Orchestration Layer

The `plantai` package is the **AI orchestration layer** of PlantAI. It implements LangGraph-based agent workflows with LLM tool-calling loops, connecting the plant data layer (`plants/`) and knowledge layer (`knowledge/`) into an intelligent plant-care assistant.

The primary agent is **Demeter** — a conversational plant-care expert that answers questions about your plants using sensor data and care guides.

---

## Directory Layout

```
plantai/
├── __init__.py
├── agents/
│   ├── __init__.py              # stream_agent(), invoke_agent()
│   └── demeter/
│       ├── __init__.py          # run(), talk() — entrypoints
│       ├── graph.py             # LangGraph StateGraph, system prompt, nodes
│       └── tools.py             # TOOLS tuple — 9 LangChain tools
└── llms/
    ├── __init__.py              # Re-exports get_ollama_llm, get_openai_llm
    ├── ollama.py                # ChatOllama factory (local Ollama)
    └── openai.py                # ChatOpenAI factory (OpenAI or compatible)
```

---

## Agent Architecture

### Demeter Agent

Demeter is a **tool-calling LangGraph agent** that provides personalized plant-care advice. The graph topology:

```
START → call_llm ──┬──→ END
              │
              └──→ call_tool → call_llm  (loop)
```

1. **`call_llm`** node: Sends the conversation (system prompt + last 7 messages) to the LLM with tools bound. Returns the AI message.
2. **Conditional edge**: If the AI message contains `tool_calls`, route to `call_tool`. Otherwise, route to `END`.
3. **`call_tool`** node: Executes all requested tools via LangGraph's `ToolNode`, then loops back to `call_llm`.

The graph uses `MemorySaver` as a checkpointer for conversation state persistence across threads.

### System Prompt

Demeter's system prompt (embedded in `graph.py`) enforces:
- **Personalized care** — Address plants by name, tailor advice to conditions
- **Data-driven recommendations** — Always use sensor data when available
- **Expert-backed fallback** — Consult care guides when sensor data is absent
- **Uncertainty signaling** — Use "I guess" when advice is not based on tools or sensor data
- **Friendly, concise tone**

---

## Tools

Demeter has **9 tools** registered in `plantai.agents.demeter.tools.TOOLS`:

### Plant Data Tools (from `plants/`)

| Tool | Signature | Description |
|---|---|---|
| `get_all_my_plants()` | `() -> list[str]` | List all plants with names and scientific names |
| `get_plant_scientific_name(plant_name)` | `(str) -> str` | Look up scientific name by given name |

### Sensor Tools (from `plants/`)

| Tool | Signature | Description |
|---|---|---|
| `read_soil_humidity_sensor(plant_name)` | `(str) -> str` | Current soil humidity + ideal range |
| `read_air_temperature_sensor(plant_name)` | `(str) -> str` | Current air temperature + ideal range |

### Care Guide Tools (from `knowledge/`)

| Tool | Signature | Description |
|---|---|---|
| `get_watering_guide(scientific_name)` | `(str) -> str` | Watering guidance from PictureThisAI + Perenual |
| `get_sunlight_guide(scientific_name)` | `(str) -> str` | Sunlight guidance from PictureThisAI + Perenual |
| `get_fertilizing_guide(scientific_name)` | `(str) -> str` | Fertilizing guidance from PictureThisAI |
| `get_pruning_guide(scientific_name)` | `(str) -> str` | Pruning guidance from PictureThisAI + Perenual |
| `get_propagation_guide(scientific_name)` | `(str) -> str` | Propagation guidance from PictureThisAI |

---

## LLM Backends

### Ollama (Local)

```python
from plantai.llms import get_ollama_llm

llm = get_ollama_llm(model="qwen3:32b")  # default model
llm = get_ollama_llm(model="llama3.1:8b", base_url="http://192.168.1.100:11434")
```

Returns a `ChatOllama` instance from `langchain_ollama`.

### OpenAI (Cloud or Compatible)

```python
from plantai.llms import get_openai_llm

llm = get_openai_llm()                              # OpenAI API
llm = get_openai_llm(model="gpt-4o")                # specific model
```

Returns a `ChatOpenAI` instance from `langchain_openai`.

### Local OpenAI-Compatible Endpoint

```python
from plantai.llms.openai import get_local_llm

llm = get_local_llm(
    model="qwen3:32b",
    base_url="http://localhost:11434/v1",
)
```

---

## Entrypoints

### `plantai.agents.demeter.talk(query)`

Convenience function for quick conversations:

```python
from plantai.agents.demeter import talk

messages = talk("How is Violet doing today?")
# Returns list[BaseMessage] with full conversation
```

### `plantai.agents.demeter.run(thread_id, state)`

Full control over the agent execution:

```python
from langchain_core.messages import HumanMessage
from plantai.agents.demeter import run

state = {"messages": [HumanMessage("Is Luna thirsty?")]}
result = run(thread_id="conversation-1", state=state)
# Returns final DemeterState dict
```

### `plantai.agents.invoke_agent(agent, state, ...)`

Generic agent invoker with Opik tracing support:

```python
from plantai.agents import invoke_agent

result = invoke_agent(
    agent=my_graph,
    state={"messages": [...]},
    thread_id="my-thread",
    trace=True,   # enables Opik tracing
)
```

### `plantai.agents.stream_agent(agent, state, ...)`

Streaming variant — yields events as they arrive:

```python
from plantai.agents import stream_agent

for event in stream_agent(agent=my_graph, state=state, trace=True):
    # event is a DemeterState dict with latest values
    pass
```

---

## Entrypoint Scripts

| Script | Description |
|---|---|
| `orange.py` | Carie agent with Ollama LLM — designed for OrangePi deployment |
| `prototype.py` | Demeter demo — runs a sample query with Opik tracing |

```bash
uv run prototype.py        # Run Demeter demo
uv run orange.py           # Run Carie on OrangePi
```

---

## Dependencies

| Dependency | Purpose |
|---|---|
| `langgraph` | Agent graph orchestration (StateGraph, ToolNode, checkpointer) |
| `langchain-ollama` | Ollama chat model integration |
| `langchain-openai` | OpenAI chat model integration |
| `opik` | LLM tracing and observability (optional) |
| `plants/` | Plant data layer (repository, schemas, I/O) |
| `knowledge/` | Care guide tools (MongoDB-backed) |

---

## Testing

Agent tests use **deepeval** for LLM evaluation:

```bash
make test-agents            # Run deepeval tests
```

Tests validate:
- **Faithfulness** — Output is faithful to tool return values
- **Tool correctness** — Right tools called with correct parameters

Test patterns use parametric inputs simulating real user queries (e.g., "Is Violet warm?", "How often should I water Lillian?").
