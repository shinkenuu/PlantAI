from unittest import mock

from langchain_core.messages import HumanMessage
import pytest

from plantai.agents import run_agent
from plantai.agents.carie import build_graph as create_carie_agent
from plantai.llms import get_ollama_llm
from plants.io.file import get_plant
from tests.carie.affirmation import is_true_affirmation


@pytest.fixture(scope="module")
def ollama_llm():
    llm = get_ollama_llm(temperature=0.0)
    return llm


@pytest.fixture(scope="module")
def carie_agent(ollama_llm):
    return create_carie_agent(llm=ollama_llm)


@pytest.mark.llm
@pytest.mark.parametrize(
    "human_message_content, context, expected_affirmation",
    [
        (
            "Is Violet warm?",
            str(get_plant("violet")),
            get_plant("violet").is_warm,
        ),
        (
            "Should I water Peter?",
            str(get_plant("peter")),
            get_plant("peter").is_thirsty,
        ),
        (
            "Tilla, would you like to eat more?",
            str(get_plant("tilla")),
            get_plant("tilla").is_hungry,
        ),
    ],
)
@mock.patch("plantai.agents.carie.input", create=True, return_value="/bye")
def test_carie_plant_interpretation(
    input_mock,
    human_message_content: str,
    context: str,
    expected_affirmation: bool,
    carie_agent,
):
    # ARRANGE
    state = {"messages": [HumanMessage(content=human_message_content)]}

    # ACT
    carie_events = list(run_agent(carie_agent, thread_id="test", state=state))

    # ASSERT
    last_event = carie_events[-1]
    last_event_message_content = last_event["messages"][-1].content
    last_event_affirmation = is_true_affirmation(
        context=context, statement=last_event_message_content
    )
    assert last_event_affirmation == expected_affirmation
