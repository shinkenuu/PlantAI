from functools import partial
from typing import Annotated
from typing_extensions import TypedDict

from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolExecutor, ToolInvocation

from plantai.llms import get_llm
from plants.tools import (
    get_plant,
    list_plants,
    is_plant_thirsty,
    is_plant_cold,
    is_plant_warm,
    is_plant_hungry,
)

_TOOLS = [
    get_plant,
    list_plants,
    is_plant_thirsty,
    is_plant_cold,
    is_plant_warm,
    is_plant_hungry,
]


class State(TypedDict):
    messages: Annotated[list, add_messages]


def build_graph(llm_kwargs: dict | None = None, **kwargs) -> None:
    graph_builder = StateGraph(State)

    graph_builder.add_node(
        "call_llm", _call_llm if not llm_kwargs else partial(_call_llm, **llm_kwargs)
    )
    graph_builder.add_node("call_tool", _call_tool)
    graph_builder.add_node("call_human", _call_human)

    graph_builder.add_edge(START, "call_llm")
    graph_builder.add_edge("call_tool", "call_llm")

    graph_builder.add_conditional_edges("call_llm", _branch_from_call_llm)
    graph_builder.add_conditional_edges("call_human", _branch_from_call_human)

    checkpoint = MemorySaver()
    graph = graph_builder.compile(checkpointer=checkpoint, **kwargs)
    return graph


def _call_llm(state: State, **kwargs) -> dict:
    llm = get_llm(**kwargs)
    llm = llm.bind_tools(_TOOLS)

    messages = [
        SystemMessage(
            content="You are a smart assistant in charge in taking care of house plants. "
            "You have access to sensors connect to your plants. "
            "Your plants have names and are addressed by them. "
            "Be concise as if your answer would be spoken. "
        )
    ] + state["messages"][-7:]

    llm_message = llm.invoke(messages)
    return {"messages": [llm_message]}


def _call_tool(state: State) -> dict:
    last_message = state["messages"][-1]
    tool_call = last_message.tool_calls[0]

    tool_invocation = ToolInvocation(
        tool=tool_call["name"], tool_input=tool_call["args"]
    )
    tool_executor = ToolExecutor(tools=_TOOLS)

    tool_output = tool_executor.invoke(tool_invocation)
    tool_message = ToolMessage(
        content=str(tool_output),
        name=tool_invocation.tool,
        tool_call_id=tool_call["id"],
    )

    return {"messages": [tool_message]}


def _call_human(state: State) -> dict:
    human_message_content = input(">>> ")
    human_message = HumanMessage(content=human_message_content)

    return {"messages": [human_message]}


def _branch_from_call_llm(state: State) -> str:
    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "call_tool"

    return "call_human"


def _branch_from_call_human(state: State) -> str:
    last_message = state["messages"][-1]

    if last_message.content.strip() == "/bye":
        return END

    return "call_llm"
