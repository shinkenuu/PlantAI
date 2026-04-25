# PlantAI Repository Analysis

## Goal

- Understand and map the flow of inputs and outputs within the PlantAI repository.
- Identify all entrypoints and trace data propagation from ingestion to output generation.
- Create a narrative ("story") describing this flow for documentation or understanding purposes.

## Instructions

- Begin analysis from each identified entrypoint in the repository.
- Ensure the summary follows the specific template provided for agent handoffs (Goal, Instructions, Discoveries, Accomplished, Relevant files).
- Focus on actionable information that allows a subsequent agent to continue the analysis without redundancy.
- The user emphasized starting from "each entrypoint," implying a multi-path analysis may be required.

## Discoveries

- **Project Purpose**: PlantAI is about "Plants meet AI for self-caring, self-knowledge and improved human interfacing"
- **Main Agent**: "Carie" is the first agent responsible for caring for house plants
- **Entry Points Identified**:
  - `orange.py` - Runs Carie agent with Ollama LLM (OrangePi deployment)
  - `prototype.py` - Runs Demeter agent with a prompt about plant health
- **Architecture Components**:
  - **Agents**: Located in `plantai/agents/` (Demeter agent with graph-based workflow using LangGraph)
  - **LLMs**: Located in `plantai/llms/` (Ollama and OpenAI integrations)
  - **Plants Data Layer**: Located in `plants/` (IO and repositories for plant data)
  - **Knowledge**: Located in `knowledge/` (Care guides, database, schemas, tools)
- **Data Sources**:
  - Arduino serial communication for sensor data
  - File-based storage (JSON) for plant data
  - MongoDB for Dodder database
  - External APIs: Trefle.io, Perenual
- **Configurable Backend**: `REPOSITORY_BACKEND` can be set to "file" or "arduino"

## Accomplished

**Completed**:
- ✅ Identified repository root structure and main directories
- ✅ Located entrypoint files (`orange.py`, `prototype.py`)
- ✅ Reviewed configuration (`config.py`) - identified environment variables and backend options
- ✅ Mapped directory structure using `tree` command
- ✅ Identified project dependencies from `pyproject.toml` (LangGraph, Pydantic, PySerial, MongoDB, Ollama, OpenAI)
- ✅ Reviewed `README.md` for project context and external knowledge sources
- ✅ Examined `plantai/__init__.py` and `plantai/agents/__init__.py` for agent execution utilities
- ✅ Analyzed `plantai/agents/demeter/graph.py` - LangGraph-based workflow with LLM + tool calling loop
- ✅ Analyzed `plantai/agents/demeter/tools.py` - 8 tools: plant listing, sensor reading, care guides
- ✅ Analyzed `plants/io/arduino.py` - Serial communication with Arduino for real-time sensor data
- ✅ Analyzed `plants/io/file.py` - JSON file-based plant storage
- ✅ Analyzed `plants/repositories/` - Repository pattern with FilePlantRepository and ArduinoPlantRepository
- ✅ Analyzed `plants/schemas.py` - Plant and Sensor Pydantic models
- ✅ Analyzed `knowledge/care_guides.py` - 5 care guide tools fetching from MongoDB
- ✅ Analyzed `knowledge/database.py` - DodderDatabase (MongoDB) for PictureThisAI and Perenual data
- ✅ Analyzed `knowledge/schemas.py` - PlantWiki and SpeciesGuide Pydantic models
- ✅ Analyzed `plantai/llms/` - Ollama and OpenAI LLM abstractions
- ✅ Analyzed entrypoint execution flow (`orange.py`, `prototype.py`)

**Left**:
- [ ] Document complete input/output flow narrative

## Relevant files / directories

**Entrypoints**:
- `/home/shinkenuu/Projects/plantai/orange.py` - Carie agent entrypoint (Ollama)
- `/home/shinkenuu/Projects/plantai/prototype.py` - Demeter agent entrypoint

**Configuration**:
- `/home/shinkenuu/Projects/plantai/config.py` - Environment and backend configuration
- `/home/shinkenuu/Projects/plantai/pyproject.toml` - Dependencies and project metadata

**Agents (to be analyzed)**:
- `/home/shinkenuu/Projects/plantai/plantai/agents/` - Agent directory
- `/home/shinkenuu/Projects/plantai/plantai/agents/demeter/graph.py` - Agent workflow graph
- `/home/shinkenuu/Projects/plantai/plantai/agents/demeter/tools.py` - Agent tools

**LLM Layer (to be analyzed)**:
- `/home/shinkenuu/Projects/plantai/plantai/llms/` - LLM abstraction layer

**Plants Data Layer (to be analyzed)**:
- `/home/shinkenuu/Projects/plantai/plants/io/` - Input/output mechanisms (Arduino, File)
- `/home/shinkenuu/Projects/plantai/plants/repositories/` - Data storage layer
- `/home/shinkenuu/Projects/plantai/plants/schemas.py` - Plant data models

**Knowledge Layer (to be analyzed)**:
- `/home/shinkenuu/Projects/plantai/knowledge/` - Care guides, database, schemas, tools

**Documentation**:
- `/home/shinkenuu/Projects/plantai/README.md` - Project documentation
