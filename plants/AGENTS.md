# plants/ — Agent Reference

> Quick-reference for the `plants` data layer. This package handles plant data storage, sensor readings, and hardware I/O.

## What This Package Does

`plants/` is the data layer for PlantAI. It provides:

- **Plant models** — Pydantic schemas for plant identity and sensor data
- **Repository pattern** — Abstract backend-agnostic access to plant data
- **Multiple backends** — File-based (JSON) and Arduino (serial UART) storage
- **Sensor merging** — Live hardware readings merged into cached plant state

## Key Concepts

### Repository Factory

`get_plant_repository()` (from `plants.repositories`) returns a per-backend singleton. The active backend is controlled by `config.settings.repository_backend` (`"file"` or `"arduino"`). Override via environment variable `REPOSITORY_BACKEND`.

### Sensor Pin Sharing

Sensors can be shared across multiple plants (e.g., one room sensor serving several plants). Multiple plants may reference the same sensor pin — the Arduino reports the same reading for each.

### Backend Differences

| Backend | Source | Notes |
|---------|--------|-------|
| `file` | JSON file on disk | Default for dev/testing |
| `arduino` | Serial UART + JSON cache | Live sensor readings; in-memory cache keyed by plant name |

## Exploring This Package

When you need details, explore these entry points rather than relying on stale docs:

- **`plants/schemas.py`** — Plant and Sensor Pydantic models, pin constraints
- **`plants/repositories/_base.py`** — Abstract repository contract (abstract vs optional methods)
- **`plants/repositories/file.py`** — JSON-backed implementation
- **`plants/repositories/arduino.py`** — Serial-backed implementation with live reading merge logic
- **`plants/io/arduino.py`** — Serial protocol, command enum, `ArduinoPlant` TypedDict
- **`plants/io/file.py`** — JSON read helpers
- **`tests/plants/factories.py`** — Factory fixtures for tests

## Wiring to `plantai/`

Agent tools in `plantai/agents/demeter/tools.py` use `get_plant_repository()` to access plant data. Key tools:

- `get_all_my_plants()` — lists all plants
- `get_plant_scientific_name()` — resolves name → scientific name
- `read_soil_humidity_sensor()` — reads live soil humidity
- `read_air_temperature_sensor()` — reads live air temperature

## Configuration

All settings via `config.settings`. Key knobs:

- `repository_backend` — which backend to use (`"file"` or `"arduino"`)
- `file_repository_json_path` — JSON file path for file backend
- `arduino_repository_json_path` — JSON cache path for arduino backend

Override via environment variables (e.g., `REPOSITORY_BACKEND=arduino`).

## Testing

- `make test-plants` — run plant unit tests (excludes Arduino hardware)
- `pytest tests/plants -m arduino` — include hardware tests
- Factory fixtures in `tests/plants/factories.py` for generating test data
