from unittest import mock

import pytest

from tests.plants.factories import PlantFactory


@mock.patch("plants.repositories.arduino._arduino")
def test_calls_arduino_io_create(arduino_io_mock, arduino_plant_repository):
    # ARRANGE
    plant = PlantFactory(name="plant_1")
    arduino_io_mock.create.return_value = plant

    # ACT
    arduino_plant_repository.create(plant)

    # ASSERT
    arduino_io_mock.create.assert_called_once_with(plant.name, pinout=plant.pinout)


@mock.patch("plants.repositories.arduino._arduino")
def test_updates_cache(arduino_io_mock, arduino_plant_repository):
    # ARRANGE
    plant = PlantFactory(name="plant_1")
    arduino_io_mock.create.return_value = plant

    # ACT
    arduino_plant_repository.create(plant)

    # ASSERT
    assert arduino_plant_repository._cache[plant.name] == plant


@mock.patch("plants.repositories.arduino._arduino")
def test_raises_runtime_error_when_arduino_io_returns_none(
    arduino_io_mock, arduino_plant_repository
):
    # ARRANGE
    plant = PlantFactory(name="plant_1")
    arduino_io_mock.create.return_value = None

    # ACT / ASSERT
    with pytest.raises(RuntimeError):
        arduino_plant_repository.create(plant)


@mock.patch("plants.repositories.arduino._arduino")
def test_raises_value_error_when_plant_has_no_pinout(
    arduino_io_mock, arduino_plant_repository
):
    # ARRANGE
    plant = PlantFactory(name="plant_1", pinout=None)
    arduino_io_mock.create.return_value = None

    # ACT / ASSERT
    with pytest.raises(ValueError):
        arduino_plant_repository.create(plant)
