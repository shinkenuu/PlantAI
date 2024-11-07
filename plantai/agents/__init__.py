from uuid import uuid4

from langgraph.graph import Graph
from opik.integrations.langchain import OpikTracer


def stream_agent(
    agent: Graph, state: dict, thread_id: str = None, trace: bool = False, **kwargs
):
    config = {
        "configurable": {"thread_id": thread_id or str(uuid4())},
        "callbacks": [OpikTracer(project_name=agent.name)] if trace else [],
    }

    for event in agent.stream(state, config, stream_mode="values", **kwargs):
        last_message = event["messages"][-1]
        last_message.pretty_print()
        yield event


def invoke_agent(
    agent: Graph, state: dict, thread_id: str = None, trace: bool = False, **kwargs
):
    config = {
        "configurable": {"thread_id": thread_id or str(uuid4())},
        "callbacks": [OpikTracer(project_name=agent.name)] if trace else [],
    }

    return agent.invoke(state, config, **kwargs)
