from deepeval import assert_test
from deepeval.metrics import FaithfulnessMetric, ToolCorrectnessMetric
from deepeval.test_case import LLMTestCase, ToolCall, ToolCallParams
import pytest

from plantai.agents.demeter import talk as talk_to_demeter
from plants.io.file import get_plant
from tests.plantai.agents import get_called_tool_calls, get_called_tools_contents


@pytest.mark.parametrize(
    "input, context, expected_tools",
    [
        (
            "Is Violet warm?",
            [f"Violet is {'' if get_plant('Violet').is_warm else 'not'} warm"],
            [
                ToolCall(
                    name="read_air_temperature_sensor",
                    input_parameters={"plant_name": "Violet"},
                )
            ],
        ),
        (
            "Should I water Tilla?",
            [f"Peter is {'' if get_plant('Tilla').is_thirsty else 'not'} thirsty"],
            [
                ToolCall(
                    name="read_soil_humidity_sensor",
                    input_parameters={"plant_name": "Tilla"},
                )
            ],
        ),
        (
            "What is the best place for Lillian to be?",
            [
                "Lillian's scientific name is Epipremnum aureum",
                "Somewhere with indirect yet abundant sunlight",
            ],
            [
                ToolCall(
                    name="search_plant_sunlight_guide",
                    input_parameters={"plant_name": "Lillian"},
                )
            ],
        ),
    ],
)
def test_question_answering(input, context, expected_tools):
    # ARRANGE
    faithfulness_metric = FaithfulnessMetric()
    tool_correctness_metric = ToolCorrectnessMetric(
        evaluation_params=[
            ToolCallParams.TOOL,
            ToolCallParams.INPUT_PARAMETERS,
        ],
    )

    # ACT
    messages = talk_to_demeter(query=input, trace=True)
    actual_output = messages[-1].content
    tools_called = get_called_tool_calls(messages)
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
