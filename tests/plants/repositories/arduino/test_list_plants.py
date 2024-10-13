from unittest import mock

from tests.plants.factories import PlantFactory
from tests.plants.io.factories import ArduinoPlantFactory
# from tests.plants.repositories.arduino.assertions import plant_equals_arduino_plant


@mock.patch("plants.repositories.arduino._arduino")
def test_calls_arduino_io_list_(arduino_io_mock, arduino_plant_repository):
    # ARRANGE
    plants = PlantFactory.build_batch(2)
    arduino_plants = [ArduinoPlantFactory(name=plant.name) for plant in plants]

    arduino_plant_repository._cache = {plant.name: plant for plant in plants}
    arduino_io_mock.list_.return_value = arduino_plants

    # ACT
    arduino_plant_repository.list_plants()

    # ASSERT
    arduino_io_mock.list_.assert_called_once_with()


@mock.patch("plants.repositories.arduino._arduino")
def test_updates_cache(arduino_io_mock, arduino_plant_repository):
    # ARRANGE
    plants = PlantFactory.build_batch(1)
    arduino_plants = [
        ArduinoPlantFactory(name=plant.name) for plant in plants
    ]

    arduino_plant_repository._cache = {plant.name: plant for plant in plants}
    arduino_io_mock.list_.return_value = arduino_plants

    # ACT
    arduino_plant_repository.list_plants()

    # ASSERT
    for arduino_plant in arduino_plants:
        cached_plant = arduino_plant_repository._cache[arduino_plant["name"]]

        assert cached_plant.name == arduino_plant["name"]
        assert cached_plant.actual_sensor.soil_humidity == arduino_plant["soil_moisture"]
        assert cached_plant.actual_sensor.air_temperature == arduino_plant["temperature"]
        assert cached_plant.actual_sensor.air_humidity == arduino_plant["humidity"]
        assert cached_plant.actual_sensor.light_level == arduino_plant["light"]
