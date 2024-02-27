import json

from .schemas import Plant

_PLANTS_JSON_FILE_PATH = "./plants.json"


def list_plants() -> list[Plant]:
    """Lists available plants.

    Returns:
        A list with available Plant instances.
    """
    plants_json = None

    with open(_PLANTS_JSON_FILE_PATH) as file:
        plants_json = json.load(file)

    plants = [Plant(**plant_json) for plant_json in plants_json]
    return plants


def get_plant(name: str) -> Plant | None:
    """Gets a Plant by its name.

    Args:
        name: the name of the Plant to be detailed.

    Returns:
        Plant matching `name` or None if there is no match.
    """
    if not name:
        return None

    lower_name = name.lower()

    plants = list_plants()
    plant = next((plant for plant in plants if plant.name.lower() == lower_name), None)

    return plant
