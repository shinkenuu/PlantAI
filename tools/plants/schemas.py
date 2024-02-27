from dataclasses import dataclass
from functools import lru_cache

from numpy import mean, std


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
        return f"#{self.id} {self.name}"

    @property
    def is_thirsty(self):
        return (
            self.ideal_min_sensor.soil_humidity
            <= self.sensor.soil_humidity
            < self.ideal_max_sensor.soil_humidity
        )

    @property
    def is_cold(self):
        return self.ideal_min_sensor.air_temperature <= self.sensor.soil_humidity

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
        ideal_std_air_temperature = std(
            [
                self.ideal_min_sensor.air_temperature,
                self.ideal_max_sensor.air_temperature,
            ]
        )

        warmness_score = (
            self.sensor.air_temperature - ideal_mean_air_temperature
        ) / ideal_std_air_temperature

        return warmness_score > warmness_baseline

    @property
    def is_hungry(self, soil_ph_baseline: float = 1):
        ideal_mean_soil_ph = mean(
            [self.ideal_min_sensor.soil_ph, self.ideal_max_sensor.soil_ph]
        )

        soil_ph_score = abs(abs(self.sensor.soil_ph) - ideal_mean_soil_ph)
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

        elif not self.is_warm:
            feelings.append("chilly")

        else:
            feelings.append("warm")

        if self.is_hungry:
            feelings.append("hungry")

        if not feelings:
            return "Im feeling nothing"

        _ = f"Im feeling {', '.join(feelings)}"
        return _

    def introduce(self):
        return f"I'm {self.name}. They call me {self.nickname}."