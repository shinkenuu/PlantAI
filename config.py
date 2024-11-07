from typing import Literal
from os import getenv

REPOSITORY_BACKEND: Literal["file", "arduino"] = getenv("REPOSITORY_BACKEND", "file")


ARDUINO_REPOSITORY_JSON_PATH = getenv("ARDUINO_REPOSITORY_JSON_PATH", "./plants/io/arduino.json")
FILE_REPOSITORY_JSON_PATH = getenv("FILE_REPOSITORY_JSON_PATH", "./plants/io/file.json")

# LLMs

OPENAI_BASE_URL = getenv("OPENAI_BASE_URL", "http://127.0.0.1:8080/v1")
OLLAMA_BASE_URL = getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")

# API KEYS

TREFLE_API_KEY = getenv("TREFLE_API_KEY")
PERUNIAL_API_KEY = getenv("PERUNIAL_API_KEY")
