import json

from config import FILE_REPOSITORY_JSON_PATH
from plants.schemas import Plant, Sensor



def list_plants(*args) -> list[Plant]:
    plants_json = None

    with open(FILE_REPOSITORY_JSON_PATH) as file:
        plants_json = json.load(file)

    plants = []

    for plant_json in plants_json:
        plant_json["actual_sensor"] = Sensor(**plant_json["actual_sensor"])
        plant_json["ideal_min_sensor"] = Sensor(**plant_json["ideal_min_sensor"])
        plant_json["ideal_max_sensor"] = Sensor(**plant_json["ideal_max_sensor"])

        plant = Plant(**plant_json)
        plants.append(plant)

    return plants


def get_plant(name: str) -> Plant | None:
    if not name:
        return None

    lower_name = name.lower()

    plants = list_plants()
    plant = next((plant for plant in plants if plant.name.lower() == lower_name), None)

    return plant
