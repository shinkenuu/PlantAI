from langgraph.graph import Graph

from plantai.agents import carie


def run_agent(agent: Graph, thread_id: str, state: dict | None = None, **kwargs):
    # kwargs = {
    # "interrupt_before": [
    #     "call_llm",
    #     "call_tool"
    # ]
    # }

    thread = {"configurable": {"thread_id": thread_id}}

    for event in agent.stream(state, thread, stream_mode="values", **kwargs):
        last_message = event["messages"][-1]
        last_message.pretty_print()
        yield event


def run_carie(thread_id: str, state: dict | None = None, **kwargs):
    carie_agent = carie.build_graph(llm_kwargs=kwargs)
    
    return list(
        run_agent(agent=carie_agent, thread_id=thread_id, state=state, **kwargs)
    )
