# plants/ — Documentation Plan

## Goal

Produce `README.md` and `AGENTS.md` for the `plants/` package so that both human developers and coding agents can quickly understand its purpose, structure, and APIs.

## Deliverables

1. **`README.md`** — Human-friendly overview: what the package does, directory layout, data models, repository pattern, I/O backends, and configuration.
2. **`AGENTS.md`** — Agent-focused reference: import paths, public API surface, schema field details, wiring to `plantai/`, and gotchas for code generation.

## Scope Summary (what to document)

| Module | Key Artifacts |
|---|---|
| `plants/schemas.py` | `Plant`, `Sensor` Pydantic models — fields, constraints, `identity` property |
| `plants/io/file.py` | File-based I/O — `list_plants()`, `get_plant(name)` reading from JSON |
| `plants/io/arduino.py` | Serial UART I/O — Singleton Serial, `Command` enum, CRUD via JSON over UART |
| `plants/repositories/_base.py` | `BasePlantRepository` ABC — `get_plant`, `list_plants`, `create`, `delete` |
| `plants/repositories/file.py` | `FilePlantRepository` — delegates to `io/file.py` |
| `plants/repositories/arduino.py` | `ArduinoPlantRepository` — in-memory cache + Arduino serial, `restore_plants_from_json`, `merge_plant_with_arduino_plant` |
| `plants/repositories/__init__.py` | `get_plant_repository()` — LRU-cached factory, selects backend via config |
| `plants/io/local_plants.json` | Sample plant data (file backend) |
| `plants/io/arduino.json` | Sample plant data with sensor ranges (Arduino backend) |
| `plants/my-plants.md` | Human-readable plant catalog with images and links |

## Cross-cutting concerns

- **Configuration**: `config.settings.repository_backend` controls which backend is active (`"file"` or `"arduino"`).
- **Dependency on `knowledge/`**: None — `plants/` is a pure data layer. `plantai/agents/` consumes it.
- **Testing**: `tests/plants/` uses `factory-boy` factories and pytest markers (`arduino`).

## Notes for Writers

- Keep `README.md` narrative and high-level; keep `AGENTS.md` structured and precise (import paths, signatures, return types).
- Call out the Arduino Singleton anti-pattern and the MCU reset-on-connect issue.
- Clarify that `Sensor` carries both *readings* and *Arduino pin assignments*.
