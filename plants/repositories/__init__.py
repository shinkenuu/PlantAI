import logging
from pathlib import Path

from config import settings
from plants.repositories._base import BasePlantRepository
from plants.repositories.arduino import ArduinoPlantRepository
from plants.repositories.file import FilePlantRepository

_instances: dict[str, BasePlantRepository] = {}


def get_plant_repository(
    backend: str = settings.plant_io.repository_backend, pins_path: Path | None = None
) -> BasePlantRepository:
    logging.info(f"Selected {backend=}")

    if backend in _instances:
        return _instances[backend]

    if backend.lower() == "arduino":
        repo = ArduinoPlantRepository()

        if pins_path is not None:
            repo.setup_plant_pins(pins_path=pins_path)
    else:
        repo = FilePlantRepository()

    _instances[backend] = repo
    return repo


def reset_plant_repository() -> None:
    """Clear all cached repository instances. Useful in tests."""
    _instances.clear()
