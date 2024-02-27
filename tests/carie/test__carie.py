from langchain_core.messages import HumanMessage
from pytest import fixture

from graphs.carie import create_graph
from tools.plants import list_plants


@fixture(scope="module")
def graph():
    return create_graph()


def test_single_tool_use(graph):
    # ARRANGE
    state = {"messages": [HumanMessage(content="Carie, tell me the name of the plants")]}
    expected_pieces = [plant.name.lower() for plant in list_plants()]

    # ACT
    result_state = graph.invoke(state)

    # ASSERT
    last_message_content = result_state["messages"][-1].content

    for expected_piece in expected_pieces:
        assert expected_piece in last_message_content.lower()
