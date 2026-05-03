from plants.schemas import Plant, Sensor
from tests.plants.factories import PlantFactory, SensorFactory


def test_plant_factory_produces_valid_plant():
    plant = PlantFactory()
    assert isinstance(plant, Plant)
    assert plant.name is not None
    assert plant.scientific_name is not None


def test_plant_factory_has_no_extra_fields():
    plant = PlantFactory()
    # Ensure no phantom fields leaked into the model
    assert not hasattr(plant, "id")


def test_sensor_factory_produces_valid_sensor():
    sensor = SensorFactory()
    assert isinstance(sensor, Sensor)
