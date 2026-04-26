from unittest import mock

import pytest

from tests.plants.factories import PlantFactory, SensorFactory


@mock.patch("plants.repositories.arduino._arduino")
def test_calls_arduino_io_create(arduino_io_mock, arduino_plant_repository):
    # ARRANGE
    plant_1_sensor = SensorFactory(soil_pin=11, dht_pin=12, light_pin=13)
    plant_1 = PlantFactory(name="plant_1", sensor=plant_1_sensor)

    # ACT
    arduino_plant_repository.create(plant_1)

    # ASSERT
    expected_pins = {
        "soil": plant_1_sensor.soil_pin,
        "dht": plant_1_sensor.dht_pin,
        "light": plant_1_sensor.light_pin,
    }
    arduino_io_mock.create.assert_called_once_with(plant_1.name, pins=expected_pins)


@mock.patch("plants.repositories.arduino._arduino")
def test_updates_cache(arduino_io_mock, arduino_plant_repository):
    # ARRANGE
    plant_1 = PlantFactory(name="plant_1")

    # ACT
    arduino_plant_repository.create(plant_1)

    # ASSERT
    assert arduino_plant_repository._cache[plant_1.name] == plant_1


@mock.patch("plants.repositories.arduino._arduino")
def test_raises_runtime_error_when_arduino_io_returns_none(
    arduino_io_mock, arduino_plant_repository
):
    # ARRANGE
    plant_1 = PlantFactory(name="plant_1")
    arduino_io_mock.create.return_value = None

    # ACT / ASSERT
    with pytest.raises(RuntimeError):
        arduino_plant_repository.create(plant_1)
