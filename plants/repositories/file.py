import json
import logging
from pathlib import Path

from plants.repositories._base import BasePlantRepository
from plants.schemas import Plant


class FilePlantRepository(BasePlantRepository):
    """
    Used to load configuration of Arduino's memory
    and mockup when there is no Arduino connected
    """

    def __init__(self, file_path: Path) -> None:
        if not file_path.exists():
            raise FileNotFoundError(str(file_path))

        self._file_path = file_path

    def get_plant(self, name: str) -> Plant | None:
        logging.info(f"Getting plant with {name=}")

        plants = self._load_from_file()
        plant = next((plant for plant in plants if plant.name == name), None)

        logging.info(f"Got {plant=}")
        return plant

    def list_plants(self, *args) -> list[Plant]:
        logging.info("Listing plants")

        plants = self._load_from_file()

        logging.info(f"Listed {len(plants)} plants")
        return plants

    def create(self, plant: Plant) -> Plant:
        logging.info(f"Creating {plant=}")
        if not plant.pinout:
            raise ValueError("Plant must have pinout set to be created")

        plants = self._load_from_file()
        plants.append(plant)
        self._dump_to_file(plants)

        logging.info(f"Created {plant=}")
        return plant

    def delete(self, name: str) -> Plant | None:
        logging.info(f"Deleting plant with {name=}")

        plants = self._load_from_file()
        remaining_plants = [plant for plant in plants if plant.name != name]

        if len(plants) > len(remaining_plants):
            self._dump_to_file(remaining_plants)
            logging.info(f"Deleted plant with {name=}")
            return

        logging.warning(f"Couldnt find plant with {name=} to delete")

    def _load_from_file(self) -> list[Plant]:
        logging.debug(f"Loading plants from {self._file_path}")

        file_text = self._file_path.read_text()
        file_json = json.loads(file_text)
        plants = [Plant.model_validate(loaded_plant) for loaded_plant in file_json]

        logging.debug(f"Loaded {len(plants)} plants from {self._file_path}")
        return plants

    def _dump_to_file(self, plants: list[Plant]) -> None:
        logging.debug(f"Dumping {len(plants)} plants to {self._file_path}")

        serialized_plants = [plant.model_dump() for plant in plants]
        serialized_plants = json.dumps(serialized_plants)

        logging.debug(f"Dumped {len(plants)} plants to {self._file_path}")
        self._file_path.write_text(serialized_plants)
