import json
import logging

from config import ARDUINO_REPOSITORY_JSON_PATH
from plants.io import arduino as _arduino
from plants.repositories._base import BasePlantRepository
from plants.schemas import Plant


class ArduinoPlantRepository(BasePlantRepository):
    def __init__(self) -> None:
        self._cache = {}

    def restore_plants_from_json(self, json_path: str = ARDUINO_REPOSITORY_JSON_PATH):
        logging.info(f"Reading plants in {json_path}")

        with open(json_path) as file:
            plants_json = json.load(file)

        logging.info(f"Read {len(plants_json)} plants in {json_path}")

        for plant_json in plants_json:
            plant = Plant(**plant_json)
            self.create(plant)

    def get_plant(self, name: str) -> Plant:
        arduino_plant = _arduino.retrieve(name)

        if not arduino_plant:
            return None

        plant = self._update_cache(arduino_plant)
        return plant

    def list_plants(self, *args) -> list[Plant]:
        arduino_plants = _arduino.list_()

        if not arduino_plants:
            return []

        plants = [self._update_cache(arduino_plant) for arduino_plant in arduino_plants]
        return plants

    def create(self, plant: Plant) -> Plant:
        arduino_plant = _arduino.create(plant.name)

        if not arduino_plant:
            raise RuntimeError("Failed to create arduino plant")

        self._cache[plant.name] = plant
        return plant

    # def delete(self, name: str) -> Plant:
    #     arduino_plant = _arduino.delete(name)

    #     if not arduino_plant:
    #         raise RuntimeError("Failed to delete arduino plant")

    #     self._cache.pop(name, None)
    #     return arduino_plant

    def _update_cache(self, arduino_plant: _arduino.ArduinoPlant) -> Plant:
        plant = self._cache[arduino_plant["name"]]
        merge_plant_with_arduino_plant(plant, arduino_plant)
        return plant


def merge_plant_with_arduino_plant(plant: Plant, arduino_plant: _arduino.ArduinoPlant):
    plant.actual_sensor.soil_humidity = arduino_plant["soil_moisture"]
    plant.actual_sensor.air_temperature = arduino_plant["temperature"]
    plant.actual_sensor.air_humidity = arduino_plant["humidity"]
    plant.actual_sensor.light_level = arduino_plant["light"]
