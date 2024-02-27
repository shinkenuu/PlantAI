import operator
from typing import TypedDict, Annotated, Sequence

from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, END

from .nodes import tool_selection


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]


def create_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("nop", tool_selection)

    workflow.set_entry_point("nop")

    workflow.add_edge("nop", END)

    graph = workflow.compile()
    return graph
