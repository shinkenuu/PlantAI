from langchain_core.tools import tool

from knowledge import care


@tool
def get_plant_watering_guide(plant_scientific_name: str) -> str:
    """Gets detailed instructions for watering a specific plant"""

    if not plant_scientific_name:
        raise ValueError("No plant scientific name provided")

    guide = care.get_care_guide(plant_scientific_name=plant_scientific_name)
    return guide.get("watering", "")


@tool
def get_plant_sunlight_guide(plant_scientific_name: str) -> str:
    """Gets detailed instructions for sunlight for a specific plant"""

    if not plant_scientific_name:
        raise ValueError("No plant scientific name provided")

    guide = care.get_care_guide(plant_scientific_name=plant_scientific_name)
    return guide.get("sunlight", "")


@tool
def get_plant_pruning_guide(plant_scientific_name: str) -> str:
    """Gets detailed instructions for pruning a specific plant"""
    
    if not plant_scientific_name:
        raise ValueError("No plant scientific name provided")

    guide = care.get_care_guide(plant_scientific_name=plant_scientific_name)
    return guide.get("pruning", "")
