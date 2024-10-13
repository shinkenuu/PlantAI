from dataclasses import dataclass
import json
from functools import lru_cache
from statistics import mean, stdev


@dataclass
class Sensor:
    # Typical Range: 0% (completely dry) to 100% (completely saturated with moisture).
    # Vary widely depending on the climate and location.
    air_humidity: float

    # Typical Range: -40°C to 50°C (-40°F to 122°F).
    # This range covers most terrestrial environments
    air_temperature: float

    # Typical Range: 0% (completely dry) to 100% (saturated soil).
    # Vary significantly based on soil type, location, and recent precipitation.
    soil_humidity: float

    # Typical Range: 0 (highly acidic) to 14 (highly alkaline).
    # Most plants thrive in a pH range of 5.5 to 7
    soil_ph: float

    light_level: int

    @lru_cache
    def compare(self, other: "Sensor") -> dict:
        diff = {
            "air_humidity_diff": self.air_humidity - other.air_humidity,
            "air_temperature_diff": self.air_temperature - other.air_temperature,
            "soil_humidity_diff": self.soil_humidity - other.soil_humidity,
            "soil_ph_diff": self.soil_ph - other.spoil_ph,
            "light_level_diff": self.light_level - other.light_level,
        }

        return diff

    def to_dict(self):
        return {
            "air_humidity": self.air_humidity,
            "air_temperature": self.air_temperature,
            "soil_humidity": self.soil_humidity,
            "soil_ph": self.soil_ph,
            "light_level": self.light_level,
        }

    def __sub__(self, other: "Sensor") -> float:
        comparison = self.compare(other)

        diff = sum(
            [
                comparison["air_humidity_diff"],
                comparison["air_temperature_diff"],
                comparison["soil_humidity_diff"],
                comparison["soil_ph_diff"],
                comparison["light_level_diff"],
            ]
        )

        return diff

    def __eq__(self, __value: object) -> bool:
        diff = self - __value
        return diff == 0


@dataclass
class Plant:
    id: int
    name: str
    scientific_name: str
    actual_sensor: Sensor
    ideal_min_sensor: Sensor
    ideal_max_sensor: Sensor

    def __str__(self):
        self_dict = self.to_dict()
        return json.dumps(self_dict)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "scientific_name": self.scientific_name,
            "actual_sensor": self.actual_sensor.to_dict(),
            "ideal_min_sensor": self.ideal_min_sensor.to_dict(),
            "ideal_max_sensor": self.ideal_max_sensor.to_dict(),
        }

    @classmethod
    def from_dict(cls, plant_dict: dict):
        actual_sensor = Sensor(**plant_dict["actual_sensor"])
        ideal_min_sensor = Sensor(**plant_dict["ideal_min_sensor"])
        ideal_max_sensor = Sensor(**plant_dict["ideal_max_sensor"])

        return cls(
            id=plant_dict["id"],
            name=plant_dict["name"],
            scientific_name=plant_dict["scientific_name"],
            actual_sensor=actual_sensor,
            ideal_min_sensor=ideal_min_sensor,
            ideal_max_sensor=ideal_max_sensor,
        )

    @property
    def is_thirsty(self):
        return self.actual_sensor.soil_humidity < self.ideal_min_sensor.soil_humidity

    @property
    def is_cold(self):
        return (
            self.actual_sensor.air_temperature < self.ideal_min_sensor.air_temperature
        )

    @property
    def is_warm(self, warmness_baseline: float = 0.3):
        """
        air temperature <= z_score([min, max], self)
        """
        ideal_mean_air_temperature = mean(
            [
                self.ideal_min_sensor.air_temperature,
                self.ideal_max_sensor.air_temperature,
            ]
        )
        ideal_std_air_temperature = stdev(
            [
                self.ideal_min_sensor.air_temperature,
                self.ideal_max_sensor.air_temperature,
            ]
        )

        warmness_score = (
            self.actual_sensor.air_temperature - ideal_mean_air_temperature
        ) / ideal_std_air_temperature

        return warmness_score > warmness_baseline

    @property
    def is_hungry(self, soil_ph_baseline: float = 1):
        ideal_mean_soil_ph = mean(
            [self.ideal_min_sensor.soil_ph, self.ideal_max_sensor.soil_ph]
        )

        soil_ph_score = abs(abs(self.actual_sensor.soil_ph) - ideal_mean_soil_ph)
        return soil_ph_score > soil_ph_baseline

    # @property
    # def in_the_dark(self, baseline_light_level: float=.4) -> bool:
    #     return self.sensor.light_level > baseline_light_level

    @property
    def feeling(self) -> str:
        feelings = []

        if self.is_thirsty:
            feelings.append("thirsty")

        if self.is_cold:
            feelings.append("cold")

        elif self.is_warm:
            feelings.append("warm")

        else:
            feelings.append("chilly")

        if self.is_hungry:
            feelings.append("hungry")

        if not feelings:
            return "Im feeling nothing"

        _ = f"Im feeling {', '.join(feelings)}"
        return _

    @property
    def identity(self) -> str:
        return f"{self.scientific_name} called {self.name}."
