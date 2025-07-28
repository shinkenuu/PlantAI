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
    sensor: Sensor | None = None
    actual_sensor: Sensor | None = None
    ideal_min_sensor: Sensor | None = None
    ideal_max_sensor: Sensor | None = None

    def __str__(self):
        model_dump = self.model_dump_json(exclude_none=True)
        return model_dump

    def __repr__(self) -> str:
        return f"Plant(name={self.name!r}, scientific_name={self.scientific_name!r})"

    @property
    def identity(self) -> str:
        return f"{self.scientific_name} called {self.name}."
