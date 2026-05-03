import logging

from plants.io import arduino
from schemas import Plant


def sync_plants_with_arduino(
    plants: list[Plant],
) -> None:
    for plant in plants:
        if not plant.sensor:
            logging.warning("Not syncing plant {plant} without sensor set")
            continue

        pins = {
            "soil": plant.sensor.soil_pin,
            "dht": plant.sensor.dht_pin,
            "light": plant.sensor.light_pin,
        }

        arduino.create(name=plant.name, pins=pins)


def read_plants_sensors(
    plants: list[arduino.Plant],
) -> list[arduino.Plant]:
    arduino_plants = []

    for plant in plants:
        arduino_plant = arduino.retrieve(plant.name)

        if not arduino_plant:
            logging.warning(f"Failed to read plant: {plant.name}")
            continue

        arduino_plants.append(arduino_plant)

    return arduino_plants
