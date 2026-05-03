# plants/ — Agent Reference

> Coding agent quick-reference for the `plants` data layer package.

## Quick Start

```python
# Get the configured repository (file or arduino, LRU-cached singleton)
from plants.repositories import get_plant_repository
repo = get_plant_repository()

# List all plants
plants: list[Plant] = repo.list_plants()

# Get a specific plant (case-insensitive)
plant: Plant | None = repo.get_plant("Luna")

# Access sensor data
if plant and plant.actual_sensor:
    print(plant.actual_sensor.soil_humidity)
    print(plant.actual_sensor.air_temperature)
```

---

## Package Structure

```
plants/
├── schemas.py              # Plant, Sensor (Pydantic BaseModel)
├── io/
│   ├── file.py             # list_plants(), get_plant(name)
│   └── arduino.py          # list_(), retrieve(), create(), delete()
└── repositories/
    ├── __init__.py         # get_plant_repository() [LRU-cached factory]
    ├── _base.py            # BasePlantRepository (ABC)
    ├── file.py             # FilePlantRepository
    └── arduino.py          # ArduinoPlantRepository
```

---

## Public API

### `plants.schemas`

#### `Sensor` (Pydantic BaseModel)

```python
from plants.schemas import Sensor

# Fields
Sensor(
    air_humidity: float,       # 0-100%
    air_temperature: float,    # Celsius
    soil_humidity: float,      # 0-100%
    soil_ph: float,            # 0-14
    light_level: int,          # lux
    soil_pin: int | None = None,   # Arduino analog pin (0-69)
    dht_pin: int | None = None,    # Arduino digital pin (0-69)
    light_pin: int | None = None,  # Arduino analog pin (0-69)
)

# Methods
sensor.dump_pins() -> dict[str, int]  # {"dht": ..., "soil": ..., "light": ...}
```

**Constraint**: Pin values must be `0 <= pin <= 69` (`MAX_ARDUINO_PIN = 69`).

#### `Plant` (Pydantic BaseModel)

```python
from plants.schemas import Plant

Plant(
    name: str,
    scientific_name: str,
    sensor: Sensor | None = None,
    actual_sensor: Sensor | None = None,
    ideal_min_sensor: Sensor | None = None,
    ideal_max_sensor: Sensor | None = None,
)

# Properties
plant.identity -> str  # "<scientific_name> called <name>."

# Serialization
str(plant) -> str  # model_dump_json(exclude_none=True)
repr(plant) -> str  # "Plant(name='...', scientific_name='...')"
```

---

### `plants.repositories`

#### Factory

```python
from plants.repositories import get_plant_repository

# Uses config.settings.repository_backend ("file" or "arduino")
repo = get_plant_repository()

# Explicit backend override
repo = get_plant_repository(repository_backend="arduino")
```

**Note**: This function is `@lru_cache(maxsize=1)` — returns the same instance per backend.

#### `BasePlantRepository` (Abstract)

```python
from plants.repositories._base import BasePlantRepository

# Abstract methods (must implement)
def get_plant(self, name: str) -> Plant | None: ...
def list_plants(self, *args) -> list[Plant]: ...

# Concrete (optional overrides)
def create(self, plant: Plant) -> Plant: ...
def delete(self, name: str) -> Plant | None: ...
```

#### `FilePlantRepository`

```python
from plants.repositories.file import FilePlantRepository

repo = FilePlantRepository()
plant = repo.get_plant("Luna")        # reads from io/local_plants.json
plants = repo.list_plants()           # returns all plants from JSON
```

Reads from `config.settings.file_repository_json_path` (default: `./plants/io/local_plants.json`).

#### `ArduinoPlantRepository`

```python
from plants.repositories.arduino import ArduinoPlantRepository

repo = ArduinoPlantRepository()
repo.restore_plants_from_json()       # load from io/arduino.json into cache
plant = repo.get_plant("Luna")        # fetches live readings from Arduino
plants = repo.list_plants()           # fetches live readings for all cached plants
repo.create(plant)                    # sends CREATE command to Arduino
repo.delete("Luna")                   # sends DELETE command to Arduino
```

**Key internals**:
- `_cache: dict[str, Plant]` — In-memory cache keyed by plant name
- `_update_cache(arduino_plant)` — Merges live readings into cached Plant via `merge_plant_with_arduino_plant()`
- `merge_plant_with_arduino_plant(plant, arduino_plant)` — Module-level function that updates `plant.actual_sensor` fields

---

### `plants.io.file`

```python
from plants.io import file as io_file

io_file.list_plants() -> list[Plant]
io_file.get_plant(name: str) -> Plant | None
```

Reads from `config.settings.file_repository_json_path`. Lookup is case-insensitive on `name`.

---

### `plants.io.arduino`

```python
from plants.io import arduino as io_arduino

# CRUD operations
io_arduino.list_() -> list[ArduinoPlant]
io_arduino.retrieve(name: str) -> ArduinoPlant | None
io_arduino.create(name: str, pins: dict[str, int] | None) -> ArduinoPlant
io_arduino.delete(name: str) -> ArduinoPlant

# Command enum
from plants.io.arduino import Command
Command.LIST       # "?"
Command.RETRIEVE   # "="
Command.CREATE     # "+"
Command.DELETE     # "-"
```

#### `ArduinoPlant` (TypedDict)

```python
class ArduinoPlant(TypedDict):
    id: str
    name: str
    soil_moisture: float
    temperature: float
    humidity: float
    light: float
```

#### Configuration Constants

```python
from plants.io.arduino import PORT, BAUD_RATE, TIMEOUT, RESET_DELAY

PORT         = "/dev/ttyACM0"
BAUD_RATE    = 115200
TIMEOUT      = 5       # seconds
RESET_DELAY  = 1       # seconds (after Serial instantiation)
```

**Gotcha**: `Serial` instantiation resets the Arduino MCU. The module uses a module-level `_serial` singleton to avoid repeated resets.

---

## Configuration

All settings via `config.settings`:

```python
from config import settings

settings.repository_backend           # "file" or "arduino"
settings.file_repository_json_path    # "./plants/io/local_plants.json"
settings.arduino_repository_json_path # "./plants/io/arduino.json"
```

Override via environment variables (e.g., `REPOSITORY_BACKEND=arduino`).

---

## Wiring to `plantai/`

The `plantai/agents/demeter/tools.py` module uses `get_plant_repository()` to access plant data:

```python
from plants.repositories import get_plant_repository

repository = get_plant_repository()
plant = repository.get_plant(plant_name)
```

Tools that depend on this pattern:
- `get_all_my_plants()` — calls `repository.list_plants()`
- `get_plant_scientific_name(plant_name)` — calls `repository.get_plant()`
- `read_soil_humidity_sensor(plant_name)` — calls `repository.get_plant()`, reads `actual_sensor.soil_humidity`
- `read_air_temperature_sensor(plant_name)` — calls `repository.get_plant()`, reads `actual_sensor.air_temperature`

---

## Testing

```bash
# Skip hardware tests
make test-plants          # pytest tests/plants -m "not arduino"

# Include Arduino hardware tests
pytest tests/plants -m arduino
```

### Factory Fixtures

```python
from tests.plants.factories import PlantFactory, SensorFactory
from tests.plants.io.factories import ArduinoPlantFactory

# Generate test data
plant = PlantFactory()
sensor = SensorFactory()
arduino_plant = ArduinoPlantFactory()
```
