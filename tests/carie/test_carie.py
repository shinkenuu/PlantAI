
from langchain_core.messages import HumanMessage
import pytest

from plantai.agents import run_agent
from plantai.agents.carie import build_graph as create_carie_agent
from plants import get_plant
from tests.carie.affirmation import is_true_affirmation


@pytest.fixture(scope="module")
def carie_agent():
    return create_carie_agent(llm_kwargs={"temperature": 0.0})


@pytest.mark.parametrize(
    "human_message, context, expected_affirmation",
    [
        (
            HumanMessage(content="Is Violet warm?"),
            str(get_plant("violet")),
            get_plant("violet").is_warm,
        ),
        (
            HumanMessage(content="Should I water Peter?"),
            str(get_plant("peter")),
            get_plant("peter").is_thirsty,
        ),
        (
            HumanMessage(content="Tilla, would you like to eat more?"),
            str(get_plant("tilla")),
            get_plant("tilla").is_hungry,
        ),
    ],
)
def test_carie_plant_interpretation(
    human_message: HumanMessage,
    context: str,
    expected_affirmation: bool,
    carie_agent,
):
    # ARRANGE
    # mock.patch("plants.tools.plants.list_plants", return_value=available_plants)

    state = {"messages": [human_message]}

    # ACT
    carie_events = list(run_agent(carie_agent, thread_id="test", state=state))

    # ASSERT
    last_event = carie_events[-1]
    last_event_message_content = last_event["messages"][-1].content
    last_event_affirmation = is_true_affirmation(context=context, statement=last_event_message_content)
    assert last_event_affirmation == expected_affirmation
