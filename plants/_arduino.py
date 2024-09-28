"""
This is a wannabe Singleton.
Due to the fact that a mere instantiation of Serial
 with the Arduino port resets the MCU (losing all stored plants).
See https://forum.arduino.cc/t/python-wont-read-serial-data-the-same-way-that-the-arduino-serial-monitor-does/502633
"""

import json
import logging
from time import sleep

from serial import Serial

# Increase when facing errors AND the L Led (pin 13) blinks once then fades
RESET_DELAY = 1

# Change these according to your Arduino setup
port = "/dev/ttyACM0"
baud_rate = 115200
timeout = 5  # Increase empirically when DEBUG tells there is no bytes waiting for either Tx and Rx

_serial = None


def list_() -> list[dict]:
    logging.info("Listing plants with Arduino")

    plants = _communicate(command="?", plant_name="")
    plants = plants.get("plants", [])

    logging.debug(f"Listed {len(plants)} plants with Arduino")
    return plants


def retrieve(name: str) -> dict | None:
    logging.info(f"Retrieving plant with {name=}")

    if not name:
        raise ValueError("No plant name provided")

    plant = _communicate(command="=", plant_name=name)

    logging.debug(f"Retrieved plant {plant}")
    return plant


def create(name: str) -> dict:
    logging.info(f"Creating plant with {name=}")

    if not name:
        raise ValueError("No plant name provided")

    plant = _communicate(command="+", plant_name=name)

    logging.debug(f"Created plant {plant}")
    return plant


def delete(name: str) -> dict:
    logging.info(f"Deleting plant with {name=}")

    if not name:
        raise ValueError("No plant name provided")

    plant = _communicate(command="-", plant_name=name)

    logging.debug(f"Deleted plant {plant}")
    return plant


def _communicate(command: str, plant_name: str) -> dict | list[dict]:
    message_to_serial = command + plant_name
    _tx(message=message_to_serial)

    message_from_serial = _rx()
    message_json = json.loads(message_from_serial)

    return message_json


def _tx(message: str) -> int | None:
    logging.debug(f"Writing to Arduino '{message}'")
    _serial = _ensure_connection()

    logging.debug(f"Arduino TX has {_serial.out_waiting} bytes waiting")

    if _serial.out_waiting > 0:
        logging.error("Arduino TX was not empty. The previous message was lost")
        _serial.reset_output_buffer()

    message_bytes = message.encode("utf-8")
    n_written_bytes = _serial.write(message_bytes)

    logging.debug(f"Wrote {n_written_bytes} bytes to Arduino")
    return n_written_bytes


def _rx() -> str:
    logging.debug("Reading from Arduino")
    _serial = _ensure_connection()

    logging.debug(f"Arduino RX has {_serial.in_waiting} bytes waiting")

    message_bytes = _serial.read_until()
    message = message_bytes.decode()

    logging.debug(f"Read from Arduino: {message}")
    return message


def _ensure_connection(
    port: str = port,
    baud_rate: int = baud_rate,
    timeout: float = timeout,
):
    global _serial

    if not _serial:
        _serial = Serial(port=port, baudrate=baud_rate, timeout=timeout)
        sleep(RESET_DELAY)

    return _serial
