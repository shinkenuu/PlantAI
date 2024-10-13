"""
An connected Arduino is required to run these tests. Please refer to Arduino section in README.md 
"""

import pytest

from plants.io import arduino


@pytest.mark.arduino
@pytest.mark.parametrize(
    "operation, operation_args, expected_operation_result",
    [
        (arduino.list_, [], []),
        (arduino.create, ("Plant 1",), {"name": "Plant 1"}),
        (arduino.create, ("Plant 2",), {"name": "Plant 2"}),
        # retrieving existing plants
        (arduino.list_, [], [{"name": "Plant 1"}, {"name": "Plant 2"}]),
        # retrieve existing plant
        (arduino.retrieve, ("Plant 1",), {"name": "Plant 1"}),
        # delete created plant
        (arduino.delete, ("Plant 1",), {"id": "_id"}),
        # retrieve deleted plant
        (arduino.retrieve, ("Plant 1",), {"error": "plant named Plant 1 not found"}),
        # retrieve another existing plant
        (arduino.retrieve, ("Plant 2",), {"name": "Plant 2"}),
        # list all plants after deletion
        (arduino.list_, [], [{"name": "Plant 2"}]),
    ],
)
def test_arduino(operation, operation_args, expected_operation_result):
    # ARRANGE

    # ACT
    actual_operation_result = operation(*operation_args)

    # ASSERT
    if isinstance(expected_operation_result, list):
        _assert_multiple_plants(actual_operation_result, expected_operation_result)
    else:
        _assert_single_plant(actual_operation_result, expected_operation_result)


def _assert_single_plant(actual_plant, expected_plant):
    assert actual_plant.items() >= expected_plant.items()


def _assert_multiple_plants(actual_plants, expected_plants):
    assert len(actual_plants) == len(expected_plants)

    for actual_plant, expected_plant in zip(actual_plants, expected_plants):
        _assert_single_plant(actual_plant, expected_plant)
