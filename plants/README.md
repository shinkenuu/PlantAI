# plants — Plant Data Layer

The `plants` package is the **data layer** of PlantAI. It defines the core domain models (`Plant`, `Sensor`), provides I/O backends (file-based JSON and Arduino serial), and implements the Repository pattern for abstracting data access.

This package has **zero dependencies on AI/LLM code** — it is a pure data abstraction consumed by `plantai/agents/` and the `knowledge/` layer.

---

## Directory Layout

```
plants/
├── __init__.py
├── schemas.py              # Pydantic models: Plant, Sensor
├── my-plants.md            # Human-readable plant catalog with images
├── io/                     # I/O backends (raw data access)
│   ├── __init__.py
│   ├── file.py             # File-based I/O (JSON)
│   ├── arduino.py          # Arduino serial UART I/O
│   ├── local_plants.json   # Sample data for file backend
│   └── arduino.json        # Sample data for Arduino backend
└── repositories/           # Repository pattern (abstracted data access)
    ├── __init__.py         # get_plant_repository() factory
    ├── _base.py            # BasePlantRepository ABC
    ├── file.py             # FilePlantRepository
    └── arduino.py          # ArduinoPlantRepository
```

---

## Core Models

### `Plant` (`plants.schemas.Plant`)

A Pydantic model representing a named houseplant with optional sensor data.

| Field | Type | Description |
|---|---|---|
| `name` | `str` | Given name (e.g., "Luna") |
| `scientific_name` | `str` | Botanical name (e.g., "Spathiphyllum wallisii") |
| `sensor` | `Sensor \| None` | Static sensor config (pin assignments, baseline readings) |
| `actual_sensor` | `Sensor \| None` | Live sensor readings from hardware |
| `ideal_min_sensor` | `Sensor \| None` | Lower bounds for ideal conditions |
| `ideal_max_sensor` | `Sensor \| None` | Upper bounds for ideal conditions |

**Property**: `identity` → `str` — Returns `"<scientific_name> called <name>."`

### `Sensor` (`plants.schemas.Sensor`)

A Pydantic model for environmental sensor readings and Arduino pin configuration.

| Field | Type | Description |
|---|---|---|
| `air_humidity` | `float` | 0–100% |
| `air_temperature` | `float` | Celsius |
| `soil_humidity` | `float` | 0–100% |
| `soil_ph` | `float` | 0–14 |
| `light_level` | `int` | Lux |
| `soil_pin` | `int \| None` | Arduino analog pin for soil moisture (0–69) |
| `dht_pin` | `int \| None` | Arduino digital pin for DHT sensor (0–69) |
| `light_pin` | `int \| None` | Arduino analog pin for light sensor (0–69) |

**Method**: `dump_pins()` → `dict[str, int]` — Returns `{"dht": ..., "soil": ..., "light": ...}`

---

## Repository Pattern

The repository layer provides a uniform interface regardless of the underlying data source.

### `BasePlantRepository` (Abstract)

| Method | Return | Description |
|---|---|---|
| `get_plant(name: str)` | `Plant \| None` | Lookup by given name (case-insensitive) |
| `list_plants()` | `list[Plant]` | List all plants |
| `create(plant: Plant)` | `Plant` | Create a new plant record |
| `delete(name: str)` | `Plant \| None` | Delete a plant by name |

### `FilePlantRepository`

Reads from a JSON file (`plants/io/local_plants.json` by default). Simple, no hardware required. Ideal for development and testing.

### `ArduinoPlantRepository`

Communicates with an Arduino over serial UART. Maintains an in-memory cache of `Plant` objects and merges live sensor readings on each `get_plant()` / `list_plants()` call.

**Key behavior**:
- `restore_plants_from_json()` — Loads plant definitions from `arduino.json` on startup
- `_update_cache()` — Merges Arduino sensor readings into cached `Plant` objects via `merge_plant_with_arduino_plant()`
- Arduino connection is a **singleton** — instantiating `Serial` resets the MCU, so the module guards against reconnection

---

## I/O Backends

### File I/O (`plants.io.file`)

- `list_plants()` → `list[Plant]` — Reads and parses the JSON file
- `get_plant(name: str)` → `Plant \| None` — Case-insensitive lookup

### Arduino I/O (`plants.io.arduino`)

Serial communication with an Arduino MCU. Uses a simple command protocol:

| Command | Character | Description |
|---|---|---|
| `LIST` | `?` | List all plants |
| `RETRIEVE` | `=` | Get a specific plant |
| `CREATE` | `+` | Create a new plant with pin config |
| `DELETE` | `-` | Delete a plant |

**Configuration** (in module):
- `PORT` — Serial port (default: `/dev/ttyACM0`)
- `BAUD_RATE` — Baud rate (default: `115200`)
- `TIMEOUT` — Read timeout in seconds (default: `5`)
- `RESET_DELAY` — Delay after connection to let MCU stabilize (default: `1`)

---

## Configuration

The active backend is selected via `config.settings.repository_backend`:

```python
# config.py
repository_backend: Literal["file", "arduino"] = "file"
```

Override via environment variable: `REPOSITORY_BACKEND=arduino`

The factory function `plants.repositories.get_plant_repository()` is **LRU-cached** (singleton per backend), so repeated calls return the same instance.

---

## Data Files

- **`io/local_plants.json`** — Plant definitions for the file backend. Contains 7 plants with sensor readings.
- **`io/arduino.json`** — Plant definitions for the Arduino backend. Includes `actual_sensor`, `ideal_min_sensor`, and `ideal_max_sensor` ranges.
- **`my-plants.md`** — Human-readable catalog with species links, common names, and images.

---

## Testing

Tests live in `tests/plants/`:

```bash
# Run all plant tests (skip Arduino hardware tests)
make test-plants

# Run with Arduino hardware
pytest -vvv tests/plants -m arduino
```

**Factory fixtures** (`tests/plants/factories.py`):
- `PlantFactory` — Generates random `Plant` objects
- `SensorFactory` — Generates random `Sensor` objects
- `ArduinoPlantFactory` (`tests/plants/io/factories.py`) — Generates `ArduinoPlant` dicts
