from langchain_core.tools import tool

import plants


@tool
def list_plants(*args) -> list[str]:
    """Lists available plants.

    Returns:
        A list with available Plant instances.
    """
    plants_ = plants.list_plants()
    return [str(plant) for plant in plants_]


@tool
def get_plant(name: str) -> str:
    """Gets a Plant by its name.

    Args:
        (name:str) the name of the Plant to be detailed.

    Returns:
        (Plant) matching `name` or None if there is no match.
    """
    plant = plants.get_plant(name)
    return str(plant)


@tool
def is_plant_thirsty(plant_name: str) -> str:
    """Check if a plant is thirsty.

    Args:
        (name:str) the name of the Plant to check for thirst.

    Returns:
        (str) "true" if plant is thirsty, "false" otherwise.
    """
    plant = plants.get_plant(plant_name)
    return str(plant.is_thirsty)


@tool
def is_plant_cold(plant_name: str) -> str:
    """Check if a plant is cold.

    Args:
        (name:str) the name of the Plant to check for cold.

    Returns:
        (str) "true" if plant is cold, "false" otherwise.
    """
    plant = plants.get_plant(plant_name)
    return str(plant.is_cold)


@tool
def is_plant_warm(plant_name: str) -> str:
    """Check if a plant is warm.

    Args:
        (name:str) the name of the Plant to check for warmth.

    Returns:
        (str) "true" if plant is warm, "false" otherwise.
    """
    plant = plants.get_plant(plant_name)
    return str(plant.is_warm)


@tool
def is_plant_hungry(plant_name: str) -> str:
    """Check if a plant is hungry.

    Args:
        (name:str) the name of the Plant to check for hunger.

    Returns:
        (str) "true" if plant is hungry, "false" otherwise.
    """
    plant = plants.get_plant(plant_name)
    return str(plant.is_hungry)
