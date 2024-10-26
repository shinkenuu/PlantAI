from langchain_core.messages import HumanMessage
from langchain_core.language_models import BaseChatModel
from langgraph.graph import Graph

from plantai.agents import carie


def run_agent(agent: Graph, thread_id: str, state: dict | None = None, **kwargs):
    thread = {"configurable": {"thread_id": thread_id}}

    for event in agent.stream(state, thread, stream_mode="values", **kwargs):
        last_message = event["messages"][-1]
        last_message.pretty_print()
        yield event


def run_carie(thread_id: str, llm: BaseChatModel, state: dict | None = None, **kwargs):
    carie_agent = carie.build_graph(llm=llm)

    return list(
        run_agent(agent=carie_agent, thread_id=thread_id, state=state, **kwargs)
    )


def ask_carie(query: str, llm: BaseChatModel, **kwargs):
    state = {"messages": [HumanMessage(content=query)]}
    events = run_carie(thread_id="_ask_carie", llm=llm, state=state, **kwargs)

    return events
