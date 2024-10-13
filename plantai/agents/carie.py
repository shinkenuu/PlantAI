from functools import partial

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode

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


def build_graph(llm: BaseChatModel, **kwargs) -> None:
    graph_builder = StateGraph(MessagesState)

    call_llm = partial(_call_llm, llm=llm)
    call_tool = ToolNode(_TOOLS)

    graph_builder.add_node("call_llm", call_llm)
    graph_builder.add_node("call_tool", call_tool)
    graph_builder.add_node("call_human", _call_human)

    graph_builder.add_edge(START, "call_llm")
    graph_builder.add_edge("call_tool", "call_llm")

    graph_builder.add_conditional_edges("call_llm", _branch_from_call_llm)
    graph_builder.add_conditional_edges("call_human", _branch_from_call_human)

    checkpoint = MemorySaver()
    graph = graph_builder.compile(checkpointer=checkpoint, **kwargs)
    return graph


def _call_llm(state: MessagesState, llm: BaseChatModel) -> dict:
    llm_with_tools = llm.bind_tools(_TOOLS)

    messages = [
        SystemMessage(
            content="You are a smart assistant in charge in taking care of house plants. "
            "You have access to sensors connect to your plants. "
            "Your plants have names and are addressed by them. "
            "Be concise as if your answer would be spoken. "
        )
    ] + state["messages"][-7:]

    llm_message = llm_with_tools.invoke(messages)
    return {"messages": [llm_message]}


def _call_human(state: MessagesState) -> dict:
    human_message_content = input(">>> ")
    human_message = HumanMessage(content=human_message_content)

    return {"messages": [human_message]}


def _branch_from_call_llm(state: MessagesState) -> str:
    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "call_tool"

    return "call_human"


def _branch_from_call_human(state: MessagesState) -> str:
    last_message = state["messages"][-1]

    if last_message.content.strip() == "/bye":
        return END

    return "call_llm"
