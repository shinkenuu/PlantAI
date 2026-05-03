from langgraph.graph.state import CompiledStateGraph
from plantai.agents.demeter.graph import build_graph


def test_build_graph_returns_compiled_graph():
    graph = build_graph()
    assert isinstance(graph, CompiledStateGraph)
    assert graph.name == "Demeter"
