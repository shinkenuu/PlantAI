from functools import lru_cache
import logging
from pathlib import Path

from config import settings
from plants.repositories._base import BasePlantRepository
from plants.repositories.arduino import ArduinoPlantRepository
from plants.repositories.file import FilePlantRepository


@lru_cache(maxsize=1)
def get_plant_repository(
    backend: str = settings.plant_io.repository_backend, pins_path: Path | None = None
) -> BasePlantRepository:
    logging.info(f"Selected {backend=}")

    if backend.lower() == "arduino":
        arduino_repository = ArduinoPlantRepository()
        arduino_repository.setup_plant_pins(pins_path=pins_path)
        return arduino_repository

    return FilePlantRepository()
