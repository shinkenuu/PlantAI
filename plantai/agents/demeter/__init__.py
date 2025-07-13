from langchain_core.messages import BaseMessage, HumanMessage

from plantai.agents import invoke_agent
from plantai.agents.demeter.graph import build_graph


def run(thread_id: str, state: dict, **kwargs):
    demeter_agent = build_graph(debug=True)
    return invoke_agent(agent=demeter_agent, state=state, thread_id=thread_id, **kwargs)


def talk(query: str, **kwargs) -> list[BaseMessage]:
    state = {"messages": [HumanMessage(content=query)]}
    events = run(thread_id="_ask_demeter", state=state, **kwargs)
    return events["messages"]
