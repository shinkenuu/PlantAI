from pydantic import BaseModel, Field

from plants.io.arduino import Plant as ArduinoPlant


MAX_ARDUINO_PIN = 69


class Sensor(BaseModel):
    air_humidity: float | None = Field(
        default=None,
        description="0% (completely dry) to 100% (completely saturated with moisture)",
    )
    air_temperature: float | None = Field(
        default=None,
        description="measured in Celsius",
    )
    soil_humidity: float | None = Field(
        default=None,
        description="0% (completely dry) to 100% (saturated soil)",
    )
    soil_ph: float | None = Field(
        default=None,
        description="0 (highly acidic) to 14 (highly alkaline)",
    )
    light_level: int | None = Field(
        default=None,
        description="measured in lux",
    )

    soil_pin: int | None = Field(
        default=None,
        description="Arduino analog pin for soil moisture",
        ge=0,
        le=MAX_ARDUINO_PIN,
    )
    dht_pin: int | None = Field(
        default=None,
        description="Arduino digital pin for DHT sensor",
        ge=0,
        le=MAX_ARDUINO_PIN,
    )
    light_pin: int | None = Field(
        default=None,
        description="Arduino analog pin for light sensor",
        ge=0,
        le=MAX_ARDUINO_PIN,
    )

    def dump_pins(self) -> dict[str, int | None]:
        pins = {
            "dht": self.dht_pin,
            "soil": self.soil_pin,
            "light": self.light_pin,
        }

        return pins

    def update_from(self, arduino_plant: ArduinoPlant):
        self.soil_humidity = arduino_plant["soil_moisture"]
        self.air_temperature = arduino_plant["temperature"]
        self.air_humidity = arduino_plant["humidity"]
        self.light_level = arduino_plant["light"]


class Plant(BaseModel):
    name: str
    scientific_name: str
    sensor: Sensor | None = None

    def __str__(self):
        model_dump = self.model_dump_json(exclude_none=True)
        return model_dump

    def __repr__(self) -> str:
        return f"Plant(name={self.name!r}, scientific_name={self.scientific_name!r})"

    @property
    def identity(self) -> str:
        return f"{self.scientific_name} called {self.name}."
