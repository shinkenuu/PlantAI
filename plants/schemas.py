from statistics import mean, stdev

from pydantic import BaseModel, Field


class Sensor(BaseModel):
    air_humidity: float = Field(
        description="0% (completely dry) to 100% (completely saturated with moisture)"
    )
    air_temperature: float = Field(description="measured in Celsius")
    soil_humidity: float = Field(
        description="0% (completely dry) to 100% (saturated soil)"
    )
    soil_ph: float = Field(description="0 (highly acidic) to 14 (highly alkaline)")
    light_level: int = Field(description="measured in lux")


class Plant(BaseModel):
    name: str
    scientific_name: str
    actual_sensor: Sensor | None = None
    ideal_min_sensor: Sensor | None = None
    ideal_max_sensor: Sensor | None = None

    def __str__(self):
        model_dump = self.model_dump_json(exclude_none=True)
        return model_dump

    def __repr__(self) -> str:
        return f"Plant(name={self.name!r}, scientific_name={self.scientific_name!r})"

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
