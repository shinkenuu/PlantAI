import factory

from plants.schemas import Pinout, Plant


class PinoutFactory(factory.Factory):
    class Meta:
        model = Pinout

    soil = factory.Faker("pyint", min_value=0, max_value=69)
    dht = factory.Faker("pyint", min_value=0, max_value=69)
    light = factory.Faker("pyint", min_value=0, max_value=69)


class PlantFactory(factory.Factory):
    class Meta:
        model = Plant

    name = factory.Faker("first_name")
    pinout = factory.SubFactory(PinoutFactory)
