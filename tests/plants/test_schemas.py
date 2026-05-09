import pytest

from plants.schemas import Pinout, Plant


# -- Pinout validation --


def test_pinout_valid_pins():
    pinout = Pinout(soil=34, dht=2, light=15)
    assert pinout.soil == 34
    assert pinout.dht == 2
    assert pinout.light == 15


def test_pinout_all_optional():
    pinout = Pinout()
    assert pinout.soil is None
    assert pinout.dht is None
    assert pinout.light is None


def test_pinout_rejects_negative_pin():
    with pytest.raises(Exception):
        Pinout(soil=-1)


def test_pinout_rejects_pin_above_69():
    with pytest.raises(Exception):
        Pinout(soil=70)


def test_pinout_boundary_pin_69():
    pinout = Pinout(soil=69)
    assert pinout.soil == 69


# -- Plant validation --


def test_plant_minimal_name_only():
    plant = Plant(name="Fern")
    assert plant.name == "Fern"
    assert plant.soil_moisture is None
    assert plant.temperature is None
    assert plant.humidity is None
    assert plant.light is None
    assert plant.pinout is None


def test_plant_with_all_sensor_readings():
    plant = Plant(
        name="Fern",
        soil_moisture=45.0,
        temperature=22.5,
        humidity=60.0,
        light=1200.0,
    )
    assert plant.soil_moisture == 45.0
    assert plant.temperature == 22.5
    assert plant.humidity == 60.0
    assert plant.light == 1200.0


def test_plant_with_pinout():
    pinout = Pinout(soil=34, dht=2, light=15)
    plant = Plant(name="Fern", pinout=pinout)
    assert plant.pinout.soil == 34
    assert plant.pinout.dht == 2
    assert plant.pinout.light == 15


def test_plant_full():
    pinout = Pinout(soil=34, dht=2, light=15)
    plant = Plant(
        name="Fern",
        soil_moisture=45.0,
        temperature=22.5,
        humidity=60.0,
        light=1200.0,
        pinout=pinout,
    )
    assert plant.name == "Fern"
    assert plant.soil_moisture == 45.0
    assert plant.pinout.soil == 34
