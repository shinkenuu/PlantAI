from unittest import mock

from tests.plants.factories import PlantFactory


@mock.patch("plants.repositories.arduino._arduino")
def test_calls_arduino_io_retrieve(arduino_io_mock, arduino_plant_repository):
    # ARRANGE
    plant = PlantFactory.build(name="plant_1")
    arduino_io_mock.retrieve.return_value = plant

    # ACT
    arduino_plant_repository.get_plant("plant_1")

    # ASSERT
    arduino_io_mock.retrieve.assert_called_once_with("plant_1")


@mock.patch("plants.repositories.arduino._arduino")
def test_updates_cache(arduino_io_mock, arduino_plant_repository):
    # ARRANGE
    plant = PlantFactory.build(name="plant_1")
    arduino_io_mock.retrieve.return_value = plant

    # ACT
    arduino_plant_repository.get_plant("plant_1")

    # ASSERT
    assert arduino_plant_repository._cache["plant_1"] == plant


@mock.patch("plants.repositories.arduino._arduino")
def test_returns_none_when_arduino_has_no_plant(
    arduino_io_mock, arduino_plant_repository
):
    arduino_io_mock.retrieve.return_value = None

    result = arduino_plant_repository.get_plant("nonexistent")

    assert result is None
