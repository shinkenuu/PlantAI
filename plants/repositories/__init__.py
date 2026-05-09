import logging
from pathlib import Path

from config import settings
from plants.repositories._base import BasePlantRepository
from plants.repositories.arduino import ArduinoPlantRepository
from plants.repositories.file import FilePlantRepository

_instances: dict[str, BasePlantRepository] = {}


def get_plant_repository(
    backend: str = settings.plant_io.repository_backend,
    plants_path: Path = settings.plant_io.plants_json_path,
) -> BasePlantRepository:
    logging.info(f"Selected {backend=}")

    if backend in _instances:
        return _instances[backend]

    repo = FilePlantRepository(file_path=plants_path)

    if backend.lower() == "arduino":
        plants = repo.list_plants()
        repo = ArduinoPlantRepository()

        for plant in plants:
            repo.create(plant)

    _instances[backend] = repo
    return repo


def reset_plant_repository() -> None:
    """Clear all cached repository instances. Useful in tests."""
    _instances.clear()
