import json
import logging
from pathlib import Path

from plants.io import arduino as _arduino
from plants.repositories._base import BasePlantRepository
from plants.schemas import Plant


class ArduinoPlantRepository(BasePlantRepository):
    def __init__(self) -> None:
        self._cache: dict[str, Plant] = {}

    def setup_plant_pins(self, pins_path: Path):
        logging.info(f"Reading plant's pins in {pins_path}")

        with open(pins_path) as file:
            pins = json.load(file)

        logging.info(f"Read {len(pins)} plants in {pins_path}")

        for plant_json in pins:
            plant = Plant(**plant_json)
            self.create(plant)

    def get_plant(self, name: str, avoid_cache: bool = False) -> Plant:
        if not avoid_cache and name in self._cache:
            return self._cache[name]

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
        sensor_pins = None

        if plant.sensor:
            sensor_pins = {
                "soil": plant.sensor.soil_pin,
                "dht": plant.sensor.dht_pin,
                "light": plant.sensor.light_pin,
            }

        arduino_plant = _arduino.create(plant.name, pins=sensor_pins)

        if not arduino_plant:
            raise RuntimeError("Failed to create arduino plant")

        self._cache[plant.name] = plant
        return plant

    def delete(self, name: str) -> Plant:
        arduino_plant = _arduino.delete(name)

        if not arduino_plant:
            raise RuntimeError("Failed to delete arduino plant")

        self._cache.pop(name, None)
        return arduino_plant

    def _update_cache(self, arduino_plant: _arduino.ArduinoPlant) -> Plant:
        plant = self._cache[arduino_plant["name"]]
        merge_plant_with_arduino_plant(plant, arduino_plant)
        return plant


def merge_plant_with_arduino_plant(plant: Plant, arduino_plant: _arduino.ArduinoPlant):
    plant.actual_sensor.soil_humidity = arduino_plant["soil_moisture"]
    plant.actual_sensor.air_temperature = arduino_plant["temperature"]
    plant.actual_sensor.air_humidity = arduino_plant["humidity"]
    plant.actual_sensor.light_level = arduino_plant["light"]
