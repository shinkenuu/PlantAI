import factory

from plants.schemas import Plant, Sensor


class SensorFactory(factory.Factory):
    class Meta:
        model = Sensor

    air_humidity = factory.Faker("pyfloat", min_value=0, max_value=100)
    air_temperature = factory.Faker("pyfloat", min_value=0, max_value=50)
    soil_humidity = factory.Faker("pyfloat", min_value=0, max_value=100)
    soil_ph = factory.Faker("pyfloat", min_value=1, max_value=14)
    light_level = factory.Faker("pyint", min_value=0, max_value=10_000)


class PlantFactory(factory.Factory):
    class Meta:
        model = Plant

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("first_name")
    scientific_name = factory.Faker("word")
    actual_sensor = factory.SubFactory(SensorFactory)
    ideal_min_sensor = factory.SubFactory(SensorFactory)
    ideal_max_sensor = factory.SubFactory(SensorFactory)
