from functools import lru_cache

from config import REPOSITORY_BACKEND
from plants.repositories._base import BasePlantRepository
from plants.repositories.arduino import ArduinoPlantRepository
from plants.repositories.file import FilePlantRepository


@lru_cache(maxsize=1)
def get_plant_repository(
    repository_backend: str = REPOSITORY_BACKEND,
) -> BasePlantRepository:
    if repository_backend.lower() == "arduino":
        arduino_repository = ArduinoPlantRepository()
        arduino_repository.restore_plants_from_json()
        return arduino_repository

    return FilePlantRepository()
