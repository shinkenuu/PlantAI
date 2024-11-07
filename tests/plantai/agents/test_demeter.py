from deepeval import assert_test
from deepeval.metrics import FaithfulnessMetric, ToolCorrectnessMetric
from deepeval.test_case import LLMTestCase
import pytest

from plantai.agents.demeter import talk as talk_to_demeter
from plants.io.file import get_plant
from tests.plantai.agents import get_called_tools_contents, get_called_tools_names


@pytest.mark.parametrize(
    "input, context, expected_tools",
    [
        (
            "Is Violet warm?",
            [f"Violet is {'' if get_plant('Violet').is_warm else 'not'} warm"],
            ["read_air_temperature_sensor"],
        ),
        (
            "Should I water Tilla?",
            [f"Peter is {'' if get_plant('Tilla').is_thirsty else 'not'} thirsty"],
            ["read_soil_humidity_sensor"],
        ),
        (
            "What is the best place for Lillian to be?",
            [
                "Lillian's scientific name is Epipremnum aureum",
                "Somewhere with indirect yet abundant sunlight",
            ],
            ["search_plant_sunlight_guide"],
        ),
    ],
)
def test_question_answering(input, context, expected_tools):
    # ARRANGE
    faithfulness_metric = FaithfulnessMetric()
    tool_correctness_metric = ToolCorrectnessMetric()

    # ACT
    messages = talk_to_demeter(query=input, trace=True)
    actual_output = messages[-1].content
    tools_called = get_called_tools_names(messages)
    retrieval_context = get_called_tools_contents(messages)

    test_case = LLMTestCase(
        input=input,
        actual_output=actual_output,
        context=context,
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
