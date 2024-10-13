from unittest import mock

from tests.plants.factories import PlantFactory
from tests.plants.io.factories import ArduinoPlantFactory


@mock.patch("plants.repositories.arduino._arduino")
def test_calls_arduino_io_retrieve(arduino_io_mock, arduino_plant_repository):
    # ARRANGE
    plant_1 = PlantFactory(name="plant_1")
    arduino_plant_1 = ArduinoPlantFactory(name="plant_1")

    arduino_plant_repository._cache = {plant_1.name: plant_1}
    arduino_io_mock.retrieve.return_value = arduino_plant_1

    # ACT
    arduino_plant_repository.get_plant(plant_1.name)

    # ASSERT
    arduino_io_mock.retrieve.assert_called_once_with(plant_1.name)


@mock.patch("plants.repositories.arduino._arduino")
def test_updates_cache(arduino_io_mock, arduino_plant_repository):
    # ARRANGE
    plant_1 = PlantFactory(name="plant_1")
    arduino_plant_1 = ArduinoPlantFactory(name="plant_1")

    arduino_plant_repository._cache = {plant_1.name: plant_1}
    arduino_io_mock.retrieve.return_value = arduino_plant_1

    # ACT
    arduino_plant_repository.get_plant(plant_1.name)

    # ASSERT
    assert arduino_plant_repository._cache[plant_1.name] == plant_1
