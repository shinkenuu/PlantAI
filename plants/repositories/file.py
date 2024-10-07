from plants.io import file as _file
from plants.repositories._base import BasePlantRepository
from plants.schemas import Plant


class FilePlantRepository(BasePlantRepository):
    def get_plant(self, name: str) -> Plant | None:
        plant = _file.get_plant(name)
        return plant

    def list_plants(self, *args) -> list[Plant]:
        plants = _file.list_plants(*args)
        return plants
