from dataclasses import dataclass
from functools import lru_cache

import numpy as np


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
    id: str = 1
    name: str = "Eddie"
    nickname: str = "Eddie"
    species: str = "haworthia fasciata"
    sensor = Sensor(
        air_humidity=0.36,
        air_temperature=0.26,
        soil_humidity=0.63,
        soil_ph=6.5,
        light_level=0.77,
    )
    ideal_min_sensor = Sensor(
        air_humidity=0.25,
        air_temperature=0.17,
        soil_humidity=0.3,
        soil_ph=5.8,
        light_level=0.0,
    )
    ideal_max_sensor = Sensor(
        air_humidity=0.85,
        air_temperature=0.35,
        soil_humidity=0.98,
        soil_ph=6.7,
        light_level=0.95,
    )

    visual_description: str = "a skull with a cactus inside. the cactus looks like a tiny pinecone canupy with snow"
    personality: str = "lazy, easily bored and forever curious"
    # Comes from sensor

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
        ideal_mean_air_temperature = np.mean(
            [self.ideal_min_sensor, self.ideal_max_sensor]
        )
        ideal_std_air_temperature = np.std(
            [self.ideal_min_sensor, self.ideal_max_sensor]
        )

        warmness_score = (
            self.air_temperature - ideal_mean_air_temperature
        ) / ideal_std_air_temperature

        return warmness_score > warmness_baseline

    @property
    def is_hungry(self, baseline_soil_ph=1):
        ideal_mean_soil_ph = np.mean([self.ideal_min_sensor, self.ideal_max_sensor])

        soil_ph_score = abs(abs(self.soil_ph) - ideal_mean_soil_ph)
        return soil_ph_score > baseline_soil_ph

    # @property
    # def in_the_dark(self, baseline_light_level: float=.4) -> bool:
    #     return self.sensor.light_level > baseline_light_level

    @property
    def feeling(self) -> str:
        im_feeling = []

        if self.is_thirsty:
            im_feeling.append("thirsty")

        if self.is_cold:
            im_feeling.append("cold")

        elif not self.is_warm:
            im_feeling.append("chilly")

        else:
            im_feeling.append("warm")

        if self.is_hungry:
            im_feeling.append("hungry")
        else:
            im_feeling.append("fed")

        if not im_feeling:
            return "Im feeling nothing"

        _ = f"Im feeling {', '.join(im_feeling)}"
        return _

    def introduce(self):
        return f"I'm {self.name}. They call me {self.nickname}."
