from typing import Annotated

from langchain_core.tools import tool

from plants.repositories import get_plant_repository
from plants.schemas import Plant
from knowledge.care import get_care_guide


@tool
def get_all_my_plants(*args) -> list[str]:
    """Returns all your plant's names and scientific names."""

    repository = get_plant_repository()
    plants = repository.list_plants()
    return [f"{plant.name} - {plant.scientific_name}" for plant in plants]


@tool
def get_plant_scientific_name(plant_name: Annotated[str, "Given name of the plant you want the scientific name of"]) -> str:
    """Returns plant's scientific name."""

    return _get_plant_scientific_name(plant_name=plant_name)


# SENSORS


@tool
def read_soil_humidity_sensor(plant_name: Annotated[str, "Given name of the plant you want to read the soil humidity"]) -> str:
    """Returns plant's soil humidity sensor reading."""

    plant = _get_plant(plant_name)

    if not plant.actual_sensor:
        return f"{plant.name} has sensors disabled"

    sensor_reading = (
        f"{plant.name}'s soil humidity is {plant.actual_sensor.soil_humidity}. "
        f"Ideally it should be between {plant.ideal_min_sensor.soil_humidity} and {plant.ideal_max_sensor.soil_humidity}"
    )

    return sensor_reading


@tool
def read_air_temperature_sensor(plant_name: Annotated[str, "Given name of the plant you want to read the temperature"]) -> str:
    """Returns plant's air temperature sensor reading."""

    plant = _get_plant(plant_name)

    if not plant.actual_sensor:
        return f"{plant.name} has sensors disabled"

    sensor_reading = (
        f"{plant.name}'s air temperature is {plant.actual_sensor.air_temperature} Celsius. "
        f"Ideally it should be between {plant.ideal_min_sensor.air_temperature} and {plant.ideal_max_sensor.air_temperature}"
    )

    return sensor_reading


# KNOWLEDGE


@tool
def search_plant_watering_guide(plant_name: Annotated[str, "Given name of the plant you want the watering guide for"]) -> str:
    """Returns plant's expert watering instructions"""

    plant_scientific_name = _get_plant_scientific_name(plant_name)
    care_guide = get_care_guide(plant_scientific_name)
    guide = care_guide.get("watering", "")
    return guide


@tool
def search_plant_sunlight_guide(plant_name: Annotated[str, "Given name of the plant you want the sunlight guide for"]) -> str:
    """Returns plant's expert sunlight instructions"""

    plant_scientific_name = _get_plant_scientific_name(plant_name)
    care_guide = get_care_guide(plant_scientific_name)
    guide = care_guide.get("sunlight", "")
    return guide


@tool
def search_plant_pruning_guide(plant_name: Annotated[str, "Given name of the plant you want the pruning guide for"]) -> str:
    """Returns plant's expert pruning instructions"""

    plant_scientific_name = _get_plant_scientific_name(plant_name)
    care_guide = get_care_guide(plant_scientific_name)
    guide = care_guide.get("pruning", "")
    return guide


# ---


def _get_plant(plant_name: str) -> Plant | None:
    repository = get_plant_repository()
    plant = repository.get_plant(plant_name)
    return plant


def _get_plant_scientific_name(plant_name: str) -> str:
    repository = get_plant_repository()
    plant = repository.get_plant(plant_name)
    return plant.scientific_name


TOOLS = (
    get_all_my_plants,
    # get_plant_scientific_name,
    # sensors
    read_soil_humidity_sensor,
    read_air_temperature_sensor,
    # knowledge
    search_plant_watering_guide,
    search_plant_sunlight_guide,
    search_plant_pruning_guide,
)
