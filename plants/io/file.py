import json
import logging

from config import settings
from plants.schemas import Plant


def list_plants(*args) -> list[Plant]:
    logging.info(f"Reading plants in {settings.file_repository_json_path}")
    plants = []

    with open(settings.file_repository_json_path) as file:
        plants_json = json.load(file)

    plants = [Plant(**plant_json) for plant_json in plants_json]

    logging.info(f"Read {len(plants)} plants in {settings.file_repository_json_path}")
    return plants


def get_plant(name: str) -> Plant | None:
    logging.info(f"Retrieving plant with {name=}")

    if not name:
        logging.warning("No plant name provided")
        return None

    lower_name = name.lower()

    plants = list_plants()
    plant = next((plant for plant in plants if plant.name.lower() == lower_name), None)

    logging.info(f"Retrieved plant {plant}")
    return plant
