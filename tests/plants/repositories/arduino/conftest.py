import pytest

from plants.repositories.arduino import ArduinoPlantRepository


@pytest.fixture
def arduino_plant_repository():
    arduino_plant_repository = ArduinoPlantRepository()
    return arduino_plant_repository
