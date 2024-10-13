from abc import abstractmethod, ABCMeta

from plants.schemas import Plant


class BasePlantRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_plant(self, name: str) -> Plant | None:
        raise NotImplementedError

    @abstractmethod
    def list_plants(self, *args) -> list[Plant]:
        raise NotImplementedError

    def create(self, plant: Plant) -> Plant:
        raise NotImplementedError

    def delete(self, name: str) -> Plant | None:
        raise NotImplementedError
