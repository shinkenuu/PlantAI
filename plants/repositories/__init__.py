import logging

from config import settings
from plants.repositories._base import BasePlantRepository
from plants.repositories.arduino import ArduinoPlantRepository
from plants.repositories.file import FilePlantRepository

_instances: dict[str, BasePlantRepository] = {}


def get_plant_repository(
    repository_backend: str = settings.repository_backend,
) -> BasePlantRepository:
    logging.info(f"Selected {repository_backend=}")

    if repository_backend in _instances:
        return _instances[repository_backend]

    if repository_backend.lower() == "arduino":
        repo = ArduinoPlantRepository()
        repo.restore_plants_from_json()
    else:
        repo = FilePlantRepository()

    _instances[repository_backend] = repo
    return repo


def reset_plant_repository() -> None:
    """Clear all cached repository instances. Useful in tests."""
    _instances.clear()
