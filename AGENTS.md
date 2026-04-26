# PlantAI - Agent Instructions

## Project Overview

PlantAI enables plants to meet AI for self-caring, self-knowledge, and improved human interfacing. The main agent "Carie" cares for house plants using LangGraph-based workflows.

## Dev Environment Tips

- **Package Manager**: Uses `uv` (not pnpm/npm)
- **Python Version**: 3.14.0 (check `.python-version`)
- Install dependencies: `uv sync`
- Run scripts in venv: `uv run <command>`
- Clean cache: `make clean-cache`


### Entrypoints

- `orange.py` - Carie agent with Ollama LLM (OrangePi deployment)
- `prototype.py` - Demeter agent demo with plant health prompts

## Testing Instructions

### Make Targets

- `make test-plants` - Run plant unit tests (excludes arduino)
- `make test-agents` - Run agent tests with deepeval
- `make lint` - Run ruff linter with auto-fix

### pytest Commands

- Run all tests: `pytest -vvv`
- Skip hardware tests: `pytest -m "not arduino"`
- Skip LLM tests: `pytest -m "not llm"`
- Focus on specific test: `pytest -k "<test name>"`

### Test Structure

- `tests/plants/` - Unit tests for plant data layer
- `tests/plantai/agents/` - Agent tests using deepeval
- `tests/plants/factories.py` - Factory fixtures for tests

## Linting

- Run linter: `ruff check .`
- Auto-fix: `ruff check . --fix`
- Or use: `make lint`

## Architecture

### Agents (`plantai/agents/`)

- LangGraph-based workflows with LLM + tool calling loops
- `demeter/` - Demeter agent with graph and tools
- Tools include: plant listing, sensor reading, care guides

### LLM Layer (`plantai/llms/`)

- Abstractions for Ollama and OpenAI
- Configurable via environment variables

### Plants Data Layer (`plants/`)

- `io/` - Input/output mechanisms (Arduino serial, JSON files)
- `repositories/` - Repository pattern for data storage
- `schemas.py` - Pydantic models for Plant and Sensor data

### Knowledge Layer (`knowledge/`)

- `care_guides.py` - Care guide tools from MongoDB
- `database.py` - DodderDatabase (MongoDB) for plant data
- `schemas.py` - PlantWiki and SpeciesGuide models
- `tools.py` - Knowledge retrieval tools

## Data Sources

- **Arduino**: Serial UART communication for sensor data
- **File**: JSON-based storage (`plants/io/local_plants.json`)
- **MongoDB**: Dodder database for PictureThisAI and Perenual data
- **External APIs**: Trefle.io, Perenual (requires API keys)

## External Knowledge Sources

See `README.md` for curated plant care resources:
- BBC Gardeners' World
- House Plant Journal
- Reddit Plant Clinic
- Various plant databases and APIs

## PR Instructions

- Title format: `[<module>] <Title>` (e.g., `[agents] Add new care guide tool`)
- Always run `make lint` and `make test-plants` before committing
- Add or update tests for code changes
