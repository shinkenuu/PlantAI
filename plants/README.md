# Plants — physical world interface

The `plants` package is one of the **data layer** of PlantAI, responsible for interfacing with physical plants via Arduino. Repository pattern abstracts accessing I/O backends (file-based JSON and Arduino serial)

This package has **zero dependencies on AI/LLM code** — it is a pure data abstraction.

---

## Plant Repositories & Backends

Backends define where the Repositories will access data.
The active backend is selected via `PLANT_IO__REPOSITORY_BACKEND`:

### File Repository & Backend (`repositories/file.py`)

Reads and writes to local file defined by `PLANT_IO__PLANTS_JSON_PATH`. Its also used to configure Arduino's pinout when initializing the MCU.

### Arduino Repository (`repositories/arduino.py`)

Abstracts the serial communication with Arduino with a CRUD interface exposing plants.

### Arduino Backend (`arduino.py`)

Communicates with a connected Arduino board via serial port. The connected Arduino must be running code defined in [Arduino PlantAI](https://github.com/shinkenuu/arduino/blob/master/plantai/plantai.ino)

---

## Linting & Testing

Lint only `plants`:

```bash
uv tool run ruff format plants/
uv tool run ty check plants/
```

Tests live in `tests/plants/`:

```bash
# Run all plant tests (skip Arduino hardware tests)
make test-plants

# Run with Arduino hardware
pytest -vvv tests/plants -m arduino
```
