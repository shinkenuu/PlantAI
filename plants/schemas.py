from pydantic import BaseModel, Field

from plants.constants import LAST_PIN_INDEX


class Pinout(BaseModel):
    """Arduino sensor pins setup."""

    soil: int | None = Field(
        default=None,
        description="Analog pin for soil moisture",
        ge=0,
        le=LAST_PIN_INDEX,
    )
    dht: int | None = Field(
        default=None,
        description="Digital pin for DHT sensor",
        ge=0,
        le=LAST_PIN_INDEX,
    )
    light: int | None = Field(
        default=None,
        description="Analog pin for light sensor",
        ge=0,
        le=LAST_PIN_INDEX,
    )


class Plant(BaseModel):
    """Arduino's model of a plant."""

    name: str

    soil_moisture: float | None = Field(
        default=None,
        description="0% (completely dry) to 100% (saturated soil)",
    )
    temperature: float | None = Field(
        default=None,
        description="air temperature, measured in Celsius",
    )
    humidity: float | None = Field(
        default=None,
        description="0% (completely dry) to 100% (completely saturated with moisture)",
    )
    light: float | None = Field(
        default=None,
        description="amount of light, measured in lux",
    )

    pinout: Pinout | None = Field(
        default=None,
        description="Arduino's model has no 'pinout'",
    )
