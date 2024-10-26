from unittest import mock

from deepeval import assert_test
from deepeval.metrics import FaithfulnessMetric, ToolCorrectnessMetric
from deepeval.test_case import LLMTestCase
import pytest

from plantai.agents import ask_carie
from plantai.llms import get_ollama_llm
from plants.io.file import get_plant
from tests.plantai.agents import get_called_tool_names


@pytest.fixture(scope="module")
def llm():
    llm = get_ollama_llm()
    return llm


@pytest.mark.parametrize(
    "input, retrieval_context, expected_tools",
    [
        (
            "Is Violet warm?",
            [f"Violet is {'' if get_plant('Violet').is_warm else 'not'} warm"],
            ["is_plant_warm"],
        ),
        (
            "Should I water Peter?",
            [f"Peter is {'' if get_plant('Peter').is_thirsty else 'not'} thirsty"],
            ["is_plant_thirsty"],
        ),
        (
            "Tilla, would you like to eat more?",
            [f"Tilla is {'' if get_plant('Tilla').is_hungry else 'not'} hungry"],
            ["is_plant_hungry"],
        ),
    ],
)
@mock.patch("plantai.agents.carie.input", create=True, return_value="/bye")
def test_carie(_, input, retrieval_context, expected_tools, llm):
    # ARRANGE
    faithfulness_metric = FaithfulnessMetric()
    tool_correctness_metric = ToolCorrectnessMetric()

    # ACT
    last_event = ask_carie(query=input, llm=llm)[-1]
    actual_output = last_event["messages"][-2].content
    tools_called = get_called_tool_names(last_event["messages"])

    test_case = LLMTestCase(
        input=input,
        actual_output=actual_output,
        retrieval_context=retrieval_context,
        tools_called=tools_called,
        expected_tools=expected_tools,
    )

    # ASSERT
    assert_test(
        test_case=test_case,
        metrics=[
            faithfulness_metric,
            tool_correctness_metric,
        ],
    )
