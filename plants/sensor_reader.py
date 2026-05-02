"""
Periodic sensor collection script.

Reads plant definitions from plants/db.json, registers each plant on the
Arduino (required after every MCU reset triggered by serial connect),
reads sensor data, and appends a timestamped JSON line to
sensor_readings.log.

Intended to be run by cron every 10 minutes.
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from config import Settings
from plants.io import arduino


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


def load_plants(pings_json_path: Path) -> list[dict]:
    with open(pings_json_path) as f:
        return json.load(f)


def sync_plants_with_arduino(
    plants: list[arduino.ArduinoPlant],
) -> None:
    for plant in plants:
        pins = None
        if "sensor" in plant:
            pins = {
                "soil": plant.soil_moisture,
                "dht": plant.sensor.dht_pin,
                "light": plant.sensor.light_pin,
            }

        arduino.create(name=plant["name"], pins=pins)

        logging.info(f"Registered plant: {plant['name']}")


def read_plants_sensors(
    plants: list[arduino.ArduinoPlant],
) -> list[arduino.ArduinoPlant]:
    arduino_plants = []

    for plant in plants:
        arduino_plant = arduino.retrieve(plant.name)

        if not arduino_plant:
            logging.warning(f"Failed to read plant: {plant.name}")
            continue

        arduino_plants.append(arduino_plant)
        logging.info(f"arduino_plant={arduino_plant.items()}")

    return arduino_plants


def main(
    plants: list[arduino.ArduinoPlant],
    sensor_log_path: Path,
) -> None:
    logging.info(f"Writing {len(plants)} plant's sensor readings to {sensor_log_path}")
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "readings": plants,
    }

    with open(sensor_log_path, "a") as f:
        f.write(json.dumps(entry) + "\n")

    logging.info("Wrote sensor readings")


def main(settings: Settings | None = None):
    logging.info("""
    ASCII ART FOR PLANT COMM - PERIODICAL SENSOR READING 
    """)

    settings = settings or Settings()

    loaded_plants = load_plants(pings_json_path=settings.plant_io.pins_json_path)
    sync_plants_with_arduino(loaded_plants)

    read_plants = read_plants_sensors(loaded_plants)
    main(read_plants)


if __name__ == "__main__":
    main()
