from langchain_core.messages import HumanMessage

from graphs.carie.nodes import tool_selection
from tools.plants import get_plant, list_plants


def test_list_plants():
    # ARRANGE
    state = {
        "messages": [HumanMessage(content="Carie, tell me the name of plants")],
        "selected_tool": None,
    }

    expected_selected_tool = {
        list_plants: {
            "args": [],
            "kwargs": {},
        }
    }

    # ACT
    result_state = tool_selection(state)

    # ASSERT
    assert result_state["selected_tool"] == expected_selected_tool


def test_get_plant():
    # ARRANGE
    state = {
        "messages": [
            HumanMessage(content="Carie, what is the status of plant named John?")
        ],
        "selected_tool": None,
    }

    acceptables_selected_tool = [
        {
            get_plant: {
                "args": ["John"],
                "kwargs": {},
            }
        },
        {
            get_plant: {
                "args": [],
                "kwargs": {"name": "John"},
            }
        },
    ]

    # ACT
    result_state = tool_selection(state)

    # ASSERT
    assert result_state["selected_tool"] in acceptables_selected_tool
