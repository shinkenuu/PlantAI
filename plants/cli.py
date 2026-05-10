from datetime import datetime, UTC
import json
import logging
from pathlib import Path
from typing import Annotated

import typer

from plants.repositories import get_plant_repository
from plants.schemas import Plant

logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
)

app = typer.Typer()


def _append_to_log(plants: list[Plant], log_path: Path):
    logging.info(f"Logging read plants into {log_path}")

    now_timestamp = datetime.now(UTC).isoformat()
    log_path.parent.mkdir(parents=True, exist_ok=True)

    with open(log_path, "a", encoding="utf-8") as file:
        for plant in plants:
            reading = {
                "timestamp": now_timestamp,
                "plant": plant.model_dump(exclude_none=True),
            }

            line = json.dumps(reading)

            file.write(line + "\n")


@app.command()
def snapshot_plants(
    backend: Annotated[str, typer.Option(help="Repository backend")] = "arduino",
    pinout_path: Annotated[
        Path, typer.Option(help="Plants with pinout configuration")
    ] = Path("plants/plants.json"),
    log_path: Annotated[
        Path | None, typer.Option(help="File to append read plants")
    ] = None,
):
    try:
        plant_repository = get_plant_repository(
            backend=backend, plants_path=pinout_path
        )
    except FileNotFoundError:
        logging.error("Sensor config not found: %s", pinout_path)
        raise typer.Exit(code=1)

    try:
        plants = plant_repository.list_plants()
    except Exception:
        logging.exception("Failed to read sensors from %s backend", backend)
        raise typer.Exit(code=1)

    if log_path:
        _append_to_log(plants=plants, log_path=log_path)

    return plants


if __name__ == "__main__":
    app()
