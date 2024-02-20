from langgraph.graph import StateGraph, END

from graphs.states import AgentState
from graphs.nodes import eddie, progmancer
from graphs.routers import query_router


def experimental_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("nop", lambda _: None)
    workflow.add_node("eddie", eddie)
    workflow.add_node("progmancer", progmancer)

    workflow.set_entry_point("nop")

    workflow.add_edge("eddie", END)
    workflow.add_edge("progmancer", END)

    workflow.add_conditional_edges(
        "nop",
        query_router,
        {"eddie": "eddie", "progmancer": "progmancer"},
    )

    app = workflow.compile()
    return app
