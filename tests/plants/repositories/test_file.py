import json
from pathlib import Path

import pytest

from plants.schemas import Pinout, Plant
from plants.repositories.file import FilePlantRepository


@pytest.fixture
def sample_plants(tmp_path: Path) -> tuple[Path, list[Plant]]:
    """Create a JSON file with two plants and return (path, plants)."""
    plants = [
        Plant(
            name="Fern",
            pinout=Pinout(soil=34, dht=2, light=15),
            soil_moisture=45.0,
        ),
        Plant(
            name="Cactus",
            pinout=Pinout(soil=35, dht=3, light=16),
            soil_moisture=10.0,
        ),
    ]
    file_path = tmp_path / "plants.json"
    file_path.write_text(json.dumps([p.model_dump() for p in plants]))
    return file_path, plants


@pytest.fixture
def empty_plants_file(tmp_path: Path) -> Path:
    file_path = tmp_path / "plants.json"
    file_path.write_text("[]")
    return file_path


# -- Init --


def test_init_raises_on_missing_file(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        FilePlantRepository(file_path=tmp_path / "nonexistent.json")


# -- list_plants --


def test_list_plants_returns_all(sample_plants):
    file_path, expected = sample_plants
    repo = FilePlantRepository(file_path=file_path)
    plants = repo.list_plants()
    assert len(plants) == 2
    assert plants[0].name == "Fern"
    assert plants[1].name == "Cactus"


def test_list_plants_empty_file(empty_plants_file):
    repo = FilePlantRepository(file_path=empty_plants_file)
    plants = repo.list_plants()
    assert plants == []


# -- get_plant --


def test_get_plant_by_name(sample_plants):
    file_path, _ = sample_plants
    repo = FilePlantRepository(file_path=file_path)
    plant = repo.get_plant("Fern")
    assert plant is not None
    assert plant.name == "Fern"


def test_get_plant_returns_none_for_missing(sample_plants):
    file_path, _ = sample_plants
    repo = FilePlantRepository(file_path=file_path)
    plant = repo.get_plant("Nonexistent")
    assert plant is None


# -- create --


def test_create_adds_plant(sample_plants):
    file_path, _ = sample_plants
    repo = FilePlantRepository(file_path=file_path)
    new_plant = Plant(name="Orchid", pinout=Pinout(soil=40, dht=4, light=17))
    repo.create(new_plant)
    plants = repo.list_plants()
    assert len(plants) == 3
    assert any(p.name == "Orchid" for p in plants)


def test_create_raises_without_pinout(sample_plants):
    file_path, _ = sample_plants
    repo = FilePlantRepository(file_path=file_path)
    plant_no_pinout = Plant(name="NoPinout")
    with pytest.raises(ValueError, match="pinout"):
        repo.create(plant_no_pinout)


# -- delete --


def test_delete_removes_plant(sample_plants):
    file_path, _ = sample_plants
    repo = FilePlantRepository(file_path=file_path)
    repo.delete("Fern")
    plants = repo.list_plants()
    assert len(plants) == 1
    assert plants[0].name == "Cactus"


def test_delete_noop_for_missing_plant(sample_plants):
    file_path, _ = sample_plants
    repo = FilePlantRepository(file_path=file_path)
    repo.delete("Nonexistent")
    plants = repo.list_plants()
    assert len(plants) == 2


# -- persistence --


def test_persistence_survives_reload(sample_plants):
    file_path, _ = sample_plants
    repo = FilePlantRepository(file_path=file_path)
    new_plant = Plant(name="Orchid", pinout=Pinout(soil=40, dht=4, light=17))
    repo.create(new_plant)

    # Fresh repo instance reads from disk
    repo2 = FilePlantRepository(file_path=file_path)
    plants = repo2.list_plants()
    assert len(plants) == 3
    assert any(p.name == "Orchid" for p in plants)
