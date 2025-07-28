from deepeval import assert_test
from deepeval.metrics import FaithfulnessMetric, ToolCorrectnessMetric
from deepeval.test_case import LLMTestCase, ToolCall, ToolCallParams
import pytest

from knowledge.care_guides import get_watering_guide, get_sunlight_guide
from plantai.agents.demeter import talk as talk_to_demeter
from plantai.agents.demeter.tools import (
    get_plant_scientific_name,
    read_soil_humidity_sensor,
    read_air_temperature_sensor,
)
from tests.plantai.agents import get_called_tool_calls, get_called_tools_contents


@pytest.mark.parametrize(
    "input, context, expected_tools",
    [
        (
            "Is Violet warm?",
            [
                get_plant_scientific_name("Lillian"),
                get_watering_guide("Spathiphyllum wallisii"),
            ],
            [
                ToolCall(
                    name="read_air_temperature_sensor",
                    input_parameters={"plant_name": "Violet"},
                )
            ],
        ),
        (
            "How often should I water Lillian?",
            [
                get_plant_scientific_name("Lillian"),
                get_watering_guide("Spathiphyllum wallisii"),
            ],
            [
                ToolCall(
                    name="get_plant_scientific_name",
                    input_parameters={"plant_name": "Lillian"},
                ),
                ToolCall(
                    name="care_guides.get_watering_guide",
                    input_parameters={"scientific_name": "Spathiphyllum wallisii"},
                ),
            ],
        ),
        (
            "Should I water Tilla?",
            ["Tilla is not thirsty"],
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
                "Epipremnum aureum thrive with indirect yet abundant sunlight",
            ],
            [
                ToolCall(
                    name="get_plant_scientific_name",
                    input_parameters={"plant_name": "Lillian"},
                ),
                ToolCall(
                    name="get_sunlight_guide",
                    input_parameters={"scientific_name": "Spathiphyllum wallisii"},
                ),
            ],
        ),
        (
            "Ivy's soil moisture feels high. Did I water it too much?",
            [
                get_plant_scientific_name("Ivy"),
                read_soil_humidity_sensor("Ivy"),
                get_watering_guide("Hedera helix"),
            ],
            [
                ToolCall(
                    name="get_plant_scientific_name",
                    input_parameters={"plant_name": "Ivy"},
                ),
                ToolCall(
                    name="read_soil_humidity_sensor",
                    input_parameters={"plant_name": "Ivy"},
                ),
                ToolCall(
                    name="care_guides.get_watering_guide",
                    input_parameters={"scientific_name": "Hedera helix"},
                ),
            ],
        ),
        (
            "Whats up with Cleo?",
            [
                read_soil_humidity_sensor("Cleo"),
                read_air_temperature_sensor("Cleo"),
            ],
            [
                ToolCall(
                    name="read_soil_humidity_sensor",
                    input_parameters={"plant_name": "Cleo"},
                ),
                ToolCall(
                    name="read_air_temperature_sensor",
                    input_parameters={"plant_name": "Cleo"},
                ),
            ],
        ),
        (
            "Is Tilla thirsty?",
            [
                read_soil_humidity_sensor("Tilla"),
                get_plant_scientific_name("Tilla"),
                get_watering_guide("Tillandsia cyanea"),
            ],
            [
                ToolCall(
                    name="read_soil_humidity_sensor",
                    input_parameters={"plant_name": "Tilla"},
                ),
                ToolCall(
                    name="get_plant_scientific_name",
                    input_parameters={"plant_name": "Tilla"},
                ),
                ToolCall(
                    name="get_watering_guide",
                    input_parameters={"scientific_name": "Tillandsia cyanea"},
                ),
            ],
        ),
        (
            "Describe the ideal place for Draco",
            [
                get_plant_scientific_name("Draco"),
                # Asking for more info i.e plant is a seedling, are there any signs of disease, etc.
                get_watering_guide("Crassula perforata"),
                get_sunlight_guide("Crassula perforata"),
            ],
            [
                ToolCall(
                    name="get_plant_scientific_name",
                    input_parameters={"plant_name": "Draco"},
                ),
                ToolCall(
                    name="get_watering_guide",
                    input_parameters={"scientific_name": "Crassula perforata"},
                ),
                ToolCall(
                    name="get_sunlight_guide",
                    input_parameters={"scientific_name": "Crassula perforata"},
                ),
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
