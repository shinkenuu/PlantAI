import json
import logging
from pathlib import Path

from plants.io import arduino as _arduino
from plants.repositories._base import BasePlantRepository
from plants.schemas import Plant, Sensor


class ArduinoPlantRepository(BasePlantRepository):
    def __init__(self) -> None:
        self._cache: dict[str, Plant] = {}

    def setup_plant_pins(self, pins_path: Path):
        logging.info(f"Reading plant's pins in {pins_path}")

        with open(pins_path) as file:
            pins = json.load(file)

        logging.info(f"Read {len(pins)} plants in {pins_path}")

        for plant_pinout in pins:
            sensor_pinout = plant_pinout.pop("sensor")
            sensor = Sensor.model_validate(sensor_pinout)

            plant = Plant(sensor=sensor, **plant_pinout)

            self.create(plant)

    def get_plant(self, name: str) -> Plant | None:
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

    def delete(self, name: str) -> _arduino.ArduinoPlant:
        arduino_plant = _arduino.delete(name)

        if not arduino_plant:
            raise RuntimeError("Failed to delete arduino plant")

        self._cache.pop(name, None)
        return arduino_plant

    def _update_cache(self, arduino_plant: _arduino.Plant) -> Plant:
        plant = self._cache[arduino_plant["name"]]

        if plant.sensor:
            plant.sensor.update_from(arduino_plant)

        return plant
