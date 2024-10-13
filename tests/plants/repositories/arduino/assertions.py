from plants.schemas import Plant
from plants.io.arduino import ArduinoPlant


def plant_equals_arduino_plant(plant: Plant, arduino_plant: ArduinoPlant):
    assert plant.name == arduino_plant["name"]
    assert plant.actual_sensor.soil_humidity == arduino_plant["soil_moisture"]
    assert plant.actual_sensor.air_temperature == arduino_plant["temperature"]
    assert plant.actual_sensor.soil_humidity == arduino_plant["humidity"]
    assert plant.actual_sensor.light_level == arduino_plant["light"]
