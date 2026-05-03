# plantai/ — Documentation Plan

## Goal

Produce `README.md` and `AGENTS.md` for the `plantai/` package so that both human developers and coding agents can quickly understand its purpose, structure, and APIs.

## Deliverables

1. **`README.md`** — Human-friendly overview: what the package does, the agent architecture (LangGraph), LLM backends, tool integration, and entrypoints.
2. **`AGENTS.md`** — Agent-focused reference: import paths, graph construction, state shape, tool registry, LLM factory functions, and gotchas for code generation.

## Scope Summary (what to document)

| Module | Key Artifacts |
|---|---|
| `plantai/agents/__init__.py` | `stream_agent()`, `invoke_agent()` — LangGraph execution helpers with Opik tracing |
| `plantai/agents/demeter/__init__.py` | `run()`, `talk()` — High-level Demeter agent entrypoints |
| `plantai/agents/demeter/graph.py` | `DemeterState`, `build_graph()`, `_call_llm()`, `_branch_from_call_llm()` — LangGraph StateGraph with tool-calling loop |
| `plantai/agents/demeter/tools.py` | `TOOLS` tuple — 9 LangChain tools bridging `plants/` and `knowledge/` |
| `plantai/llms/__init__.py` | Re-exports `get_ollama_llm`, `get_openai_llm` |
| `plantai/llms/ollama.py` | `get_llm()` — Returns `ChatOllama`, default model `qwen3:32b` |
| `plantai/llms/openai.py` | `get_llm()`, `get_local_llm()` — Returns `ChatOpenAI`, supports local OpenAI-compatible endpoints |

## Cross-cutting concerns

- **System prompt**: Embedded in `graph.py` as `_SYSTEM_MESSAGE` — governs Demeter's behavior, uncertainty signaling ("I guess"), and data-driven care advice.
- **Tool calling loop**: `START → call_llm → (call_tool → call_llm)* → END` via conditional edges.
- **Dependencies**: `plantai/` depends on `plants/` (data), `knowledge/` (care guides), and optionally `opik` (tracing).
- **Entrypoints**: `orange.py` (Ollama on OrangePi), `prototype.py` (Demeter demo with tracing).
- **Testing**: `tests/plantai/agents/` uses `deepeval` with `FaithfulnessMetric` and `ToolCorrectnessMetric`.

## Notes for Writers

- Emphasize the separation: `plantai/` owns agent orchestration; `plants/` owns data; `knowledge/` owns care guides.
- Document the graph topology clearly (nodes, edges, conditional branching).
- List all 9 tools with their signatures and which modules they come from.
- Call out the message windowing (`state["messages"][-7:]`) in `_call_llm`.
