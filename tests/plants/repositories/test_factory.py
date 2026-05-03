from unittest import mock

from plants.repositories import get_plant_repository, reset_plant_repository
from plants.repositories.file import FilePlantRepository
from plants.repositories.arduino import ArduinoPlantRepository


def test_returns_file_repository_by_default():
    reset_plant_repository()
    repo = get_plant_repository()
    assert isinstance(repo, FilePlantRepository)


def test_returns_same_instance_on_repeated_calls():
    reset_plant_repository()
    repo1 = get_plant_repository()
    repo2 = get_plant_repository()
    assert repo1 is repo2


def test_returns_arduino_repository_when_requested():
    reset_plant_repository()
    with mock.patch.object(ArduinoPlantRepository, "setup_plant_pins"):
        repo = get_plant_repository(backend="arduino")
    assert isinstance(repo, ArduinoPlantRepository)


def test_per_backend_singletons_are_independent():
    reset_plant_repository()
    file_repo = get_plant_repository(backend="file")
    file_repo2 = get_plant_repository(backend="file")
    assert file_repo is file_repo2


def test_reset_clears_cache():
    reset_plant_repository()
    repo1 = get_plant_repository()
    reset_plant_repository()
    repo2 = get_plant_repository()
    assert repo1 is not repo2
