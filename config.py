from typing import Literal
from os import getenv

REPOSITORY_BACKEND: Literal["file", "arduino"] = getenv("REPOSITORY_BACKEND", "file")


ARDUINO_REPOSITORY_JSON_PATH = getenv("ARDUINO_REPOSITORY_JSON_PATH", "./arduino.json")
FILE_REPOSITORY_JSON_PATH = getenv("FILE_REPOSITORY_JSON_PATH", "./plants.json")

OPENAI_BASE_URL = getenv("OPENAI_BASE_URL", "http://127.0.0.1:8080/v1")