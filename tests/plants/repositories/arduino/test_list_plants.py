from unittest import mock

from tests.plants.factories import PlantFactory


@mock.patch("plants.repositories.arduino._arduino")
def test_calls_arduino_io_list_(arduino_io_mock, arduino_plant_repository):
    # ARRANGE
    plants = PlantFactory.build_batch(2)
    arduino_io_mock.list_.return_value = plants

    # ACT
    arduino_plant_repository.list_plants()

    # ASSERT
    arduino_io_mock.list_.assert_called_once_with()


@mock.patch("plants.repositories.arduino._arduino")
def test_updates_cache(arduino_io_mock, arduino_plant_repository):
    # ARRANGE
    plants = PlantFactory.build_batch(2)
    arduino_io_mock.list_.return_value = plants

    # ACT
    arduino_plant_repository.list_plants()

    # ASSERT
    for plant in plants:
        cached = arduino_plant_repository._cache[plant.name]
        assert cached.name == plant.name
        assert cached.soil_moisture == plant.soil_moisture
        assert cached.temperature == plant.temperature
        assert cached.humidity == plant.humidity
        assert cached.light == plant.light


@mock.patch("plants.repositories.arduino._arduino")
def test_returns_empty_list_when_arduino_has_no_plants(
    arduino_io_mock, arduino_plant_repository
):
    arduino_io_mock.list_.return_value = []

    result = arduino_plant_repository.list_plants()

    assert result == []
