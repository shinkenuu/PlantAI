from datetime import datetime, UTC
import json
import logging
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import Progress, SpinnerColumn, TextColumn

from plants.repositories import get_plant_repository
from plants.schemas import Plant

# Setup rich console
console = Console()
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, console=console)],
)

app = typer.Typer(rich_markup_mode="rich")


def _append_to_sensor_reading_log(plants: list[Plant], sensor_reading_path: Path):
    logging.info(f"Dumping plants for logging into {sensor_reading_path}")

    now_timestamp = datetime.now(UTC).isoformat()
    sensor_reading_path.parent.mkdir(parents=True, exist_ok=True)

    with open(sensor_reading_path, "a", encoding="utf-8") as file:
        for plant in plants:
            reading = {
                "timestamp": now_timestamp,
                "plant": plant.model_dump(exclude_none=True),
            }

            line = json.dumps(reading)

            file.write(line + "\n")


@app.command()
def read_plants_sensors(
    backend: Annotated[str, typer.Option(help="Repository backend")] = "arduino",
    pins_path: Annotated[str, typer.Option(help="Arduino pinout")] = "plants/pins.json",
    log_path: Annotated[Path, typer.Option(help="Log path")] = Path("sensors.jsonl"),
):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description=f"Reading plants from {backend}...", total=None)

        plant_repository = get_plant_repository(backend=backend, pins_path=pins_path)
        plants = plant_repository.list_plants()

        if log_path:
            _append_to_sensor_reading_log(plants, log_path)

        return plants


if __name__ == "__main__":
    app()
