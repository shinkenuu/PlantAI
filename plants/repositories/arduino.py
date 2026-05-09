from plants import arduino as _arduino
from plants.repositories._base import BasePlantRepository
from plants.schemas import Plant


class ArduinoPlantRepository(BasePlantRepository):
    def __init__(self) -> None:
        self._cache: dict[str, Plant] = {}

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
        if not plant.pinout:
            raise ValueError("Plant must have pinout set to be created")

        arduino_plant = _arduino.create(plant.name, pinout=plant.pinout)

        if not arduino_plant:
            raise RuntimeError("Failed to create arduino plant")

        self._cache[plant.name] = plant
        return plant

    def delete(self, name: str) -> Plant | None:
        cached_plant = self._cache.get(name)

        arduino_plant = _arduino.delete(name)

        if not arduino_plant:
            raise RuntimeError("Failed to delete arduino plant")

        self._cache.pop(name, None)
        return cached_plant

    def _update_cache(self, arduino_plant: _arduino.Plant) -> Plant:
        self._cache[arduino_plant.name] = arduino_plant
        return arduino_plant
