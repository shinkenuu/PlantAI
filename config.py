from typing import Literal

from pydantic import Field, MongoDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Plant I/O
    repository_backend: Literal["file", "arduino"] = "file"
    arduino_repository_json_path: str = "./plants/io/arduino.json"
    file_repository_json_path: str = "./plants/io/local_plants.json"

    # LLM endpoints
    openai_base_url: str = "http://127.0.0.1:8080/v1"
    ollama_base_url: str = "http://127.0.0.1:11434"

    # External API keys (None = not configured)
    trefle_api_key: str | None = None
    perenual_api_key: str | None = None  # fixed typo: was PERUNIAL

    # Database
    dodder_database_uri: MongoDsn = Field(
        default="mongodb://root:toor@127.0.0.1:27017/?authSource=admin",
        description="MongoDB connection URI. Override via DODDER_DATABASE_URI env var.",
    )


# Module-level singleton — import this everywhere instead of the bare constants.
settings = Settings()
