import factory


class ArduinoPlantFactory(factory.DictFactory):
    id = factory.LazyAttribute(lambda name: f"_{name.name}_id")
    name = factory.Faker("first_name")
    soil_moisture = factory.Faker("pyfloat", min_value=0, max_value=1)
    temperature = factory.Faker("pyfloat", min_value=0, max_value=50)
    humidity = factory.Faker("pyfloat", min_value=0, max_value=1)
    light = factory.Faker("pyfloat", min_value=0, max_value=5_000)
