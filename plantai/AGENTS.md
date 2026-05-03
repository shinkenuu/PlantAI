# plantai/ — Agent Reference

> Coding agent quick-reference for the `plantai` agent orchestration package.

## Quick Start

```python
# Quick conversation with Demeter
from plantai.agents.demeter import talk
messages = talk("How is my plant Luna doing?")

# Full control with custom state
from langchain_core.messages import HumanMessage
from plantai.agents.demeter import run

state = {"messages": [HumanMessage("Is Luna thirsty?")]}
result = run(thread_id="my-thread", state=state)
```

---

## Package Structure

```
plantai/
├── __init__.py
├── agents/
│   ├── __init__.py              # stream_agent(), invoke_agent()
│   └── demeter/
│       ├── __init__.py          # run(), talk()
│       ├── graph.py             # build_graph(), _call_llm(), _branch_from_call_llm(), _SYSTEM_MESSAGE
│       └── tools.py             # TOOLS tuple, individual @tool functions
└── llms/
    ├── __init__.py              # get_ollama_llm, get_openai_llm
    ├── ollama.py                # get_llm() -> ChatOllama
    └── openai.py                # get_llm() -> ChatOpenAI, get_local_llm()
```

---

## Public API

### `plantai.agents` (Execution Helpers)

```python
from plantai.agents import stream_agent, invoke_agent

# Stream events (yields State dicts)
for event in stream_agent(
    agent=graph,
    state={"messages": [...]},
    thread_id="thread-1",
    trace=True,          # Opik tracing
):
    last_message = event["messages"][-1]
    last_message.pretty_print()

# Invoke (returns final State)
result = invoke_agent(
    agent=graph,
    state={"messages": [...]},
    thread_id="thread-1",
    trace=True,
)
```

Both functions:
- Generate a random `thread_id` if not provided (via `uuid4()`)
- Attach `OpikTracer(graph.get_graph(xray=True))` callback when `trace=True`
- Use `stream_mode="values"` for streaming

---

### `plantai.agents.demeter` (Demeter Entrypoints)

```python
from plantai.agents.demeter import run, talk

# talk() — convenience wrapper, returns messages
from langchain_core.messages import BaseMessage
messages: list[BaseMessage] = talk("How is Luna doing?")

# run() — full control, returns DemeterState
state = {"messages": [HumanMessage("Is Luna thirsty?")]}
result = run(thread_id="my-thread", state=state)
```

#### `run(thread_id, state, **kwargs)`

```python
def run(thread_id: str, state: dict, **kwargs) -> DemeterState: ...
```

- Builds graph with `build_graph(debug=True)`
- Calls `invoke_agent()` with the graph and state

#### `talk(query, **kwargs)`

```python
def talk(query: str, **kwargs) -> list[BaseMessage]: ...
```

- Wraps `query` in `HumanMessage`, passes to `run()` with `thread_id="_ask_demeter"`
- Returns the `messages` list from the final state

---

### `plantai.agents.demeter.graph` (Graph Construction)

```python
from plantai.agents.demeter.graph import build_graph, DemeterState, _SYSTEM_MESSAGE

# Build the agent graph
graph = build_graph(debug=False)    # returns compiled LangGraph with name "Demeter"
graph = build_graph(debug=True)     # enables debug mode
```

#### `DemeterState`

Extends `langgraph.graph.MessagesState` — standard LangGraph message state with `messages: list[BaseMessage]`.

#### Graph Topology

```
Nodes:
  - "call_llm"     → _call_llm(state)
  - "call_tool"    → ToolNode(TOOLS)

Edges:
  START → "call_llm"
  "call_tool" → "call_llm"
  "call_llm" → conditional → ["call_tool", END]
```

#### `_call_llm(state: MessagesState) -> dict`

```python
# Internal — builds LLM call with system prompt + last 7 messages
llm = get_ollama_llm().bind_tools(TOOLS)
messages = [SystemMessage(content=_SYSTEM_MESSAGE)] + state["messages"][-7:]
ai_message = llm.invoke(messages)
return {"messages": [ai_message]}
```

**Key detail**: Message window is **last 7 messages** (`state["messages"][-7:]`) to keep context manageable.

#### `_branch_from_call_llm(state: MessagesState) -> str`

```python
# Returns "call_tool" if last message has tool_calls, else "END"
last_message = state["messages"][-1]
return "call_tool" if last_message.tool_calls else END
```

#### `_SYSTEM_MESSAGE`

Full system prompt string embedded in the module. Governs Demeter's personality, data-driven behavior, and uncertainty signaling ("I guess").

---

### `plantai.agents.demeter.tools` (Tool Registry)

```python
from plantai.agents.demeter.tools import TOOLS

# TOOLS is a tuple of 9 LangChain @tool functions
```

#### Tool Signatures

```python
# Plant listing
get_all_my_plants() -> list[str]

# Plant lookup
get_plant_scientific_name(plant_name: str) -> str

# Sensor readings
read_soil_humidity_sensor(plant_name: str) -> str
read_air_temperature_sensor(plant_name: str) -> str

# Care guides (from knowledge.care_guides)
get_watering_guide(scientific_name: str) -> str
get_sunlight_guide(scientific_name: str) -> str
get_fertilizing_guide(scientific_name: str) -> str
get_pruning_guide(scientific_name: str) -> str
get_propagation_guide(scientific_name: str) -> str
```

#### Internal Helpers

```python
_get_plant(plant_name: str) -> Plant | None
_get_plant_scientific_name(plant_name: str) -> str
```

Both use `get_plant_repository()` from `plants.repositories`.

---

### `plantai.llms` (LLM Factories)

```python
from plantai.llms import get_ollama_llm, get_openai_llm

# Ollama (local)
llm = get_ollama_llm()                          # qwen3:32b via ChatOllama
llm = get_ollama_llm(model="llama3.1:8b")       # custom model

# OpenAI (cloud or compatible)
llm = get_openai_llm()                          # qwen3:32b via ChatOpenAI
llm = get_openai_llm(model="gpt-4o")            # custom model
```

#### `plantai.llms.ollama`

```python
from plantai.llms.ollama import get_llm, QWEN3, _DEFAULT_MODEL_NAME

QWEN3                 = "qwen3:32b"
_DEFAULT_MODEL_NAME   = QWEN3

get_llm(model: str = QWEN3, **kwargs) -> ChatOllama
```

Passes all kwargs through to `ChatOllama` constructor (e.g., `base_url`, `temperature`).

#### `plantai.llms.openai`

```python
from plantai.llms.openai import get_llm, get_local_llm, QWEN3, _DEFAULT_MODEL_NAME

get_llm(model: str = QWEN3, **kwargs) -> ChatOpenAI
get_local_llm(
    model: str = QWEN3,
    base_url: str = "http://localhost:11434/v1",
    **kwargs
) -> ChatOpenAI
```

`get_local_llm()` sets `base_url` for local OpenAI-compatible endpoints (e.g., Ollama's OpenAI API).

---

## Configuration

LLM endpoints are configured via `config.settings`:

```python
from config import settings

settings.ollama_base_url    # "http://127.0.0.1:11434"
settings.openai_base_url    # "http://127.0.0.1:8080/v1"
```

Override via environment variables: `OLLAMA_BASE_URL`, `OPENAI_BASE_URL`.

---

## Wiring Diagram

```
plantai/agents/demeter/
    graph.py
        ├── _call_llm() ──→ plantai.llms.get_ollama_llm().bind_tools(TOOLS)
        └── _branch_from_call_llm() ──→ checks tool_calls on last message

    tools.py
        ├── get_all_my_plants() ──→ plants.repositories.get_plant_repository().list_plants()
        ├── get_plant_scientific_name() ──→ plants.repositories.get_plant_repository().get_plant()
        ├── read_soil_humidity_sensor() ──→ plants.repositories.get_plant_repository().get_plant()
        ├── read_air_temperature_sensor() ──→ plants.repositories.get_plant_repository().get_plant()
        ├── get_watering_guide() ──→ knowledge.care_guides (DodderDatabase → MongoDB)
        ├── get_sunlight_guide() ──→ knowledge.care_guides
        ├── get_fertilizing_guide() ──→ knowledge.care_guides
        ├── get_pruning_guide() ──→ knowledge.care_guides
        └── get_propagation_guide() ──→ knowledge.care_guides
```

---

## Testing

```bash
make test-agents    # DEEPEVAL_TELEMETRY_OPT_OUT="YES" uv run deepeval test run tests/plantai/agents -vv
```

### Test Helpers (`tests/plantai/agents/__init__.py`)

```python
from tests.plantai.agents import get_called_tool_calls, get_called_tools_contents

# Extract ToolCall objects from message history
tool_calls = get_called_tool_calls(messages: list[BaseMessage]) -> list[ToolCall]

# Extract tool return values
contents = get_called_tools_contents(messages: list[BaseMessage]) -> list[str]
```

### Test Pattern

Tests use `deepeval` with `FaithfulnessMetric` and `ToolCorrectnessMetric`:

```python
from deepeval import assert_test
from deepeval.metrics import FaithfulnessMetric, ToolCorrectnessMetric
from deepeval.test_case import LLMTestCase, ToolCall, ToolCallParams

test_case = LLMTestCase(
    input="Is Violet warm?",
    actual_output=messages[-1].content,
    context=[...],
    retrieval_context=get_called_tools_contents(messages),
    tools_called=get_called_tool_calls(messages),
    expected_tools=[
        ToolCall(name="read_air_temperature_sensor", input_parameters={"plant_name": "Violet"}),
    ],
)

assert_test(test_case=test_case, metrics=[faithfulness_metric, tool_correctness_metric])
```
