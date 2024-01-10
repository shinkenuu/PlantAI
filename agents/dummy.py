from dataclasses import dataclass


@dataclass
class Plant:
    # Typical Range: 0% (completely dry) to 100% (completely saturated with moisture).
    # Vary widely depending on the climate and location.
    air_humidity: float = 0.8

    # Typical Range: -40°C to 50°C (-40°F to 122°F).
    # This range covers most terrestrial environments
    air_temperature: float = 20.0

    # Typical Range: 0% (completely dry) to 100% (saturated soil).
    # Vary significantly based on soil type, location, and recent precipitation.
    soil_moisture: float = 0.8

    # Typical Range: 0 (highly acidic) to 14 (highly alkaline).
    # Most plants thrive in a pH range of 5.5 to 7
    soil_ph: float = 6.0

    # Typical Range: 0 lux (complete darkness) to 100,000 lux (bright sunlight).
    # Extend beyond 100,000 lux in direct sunlight.
    light_level: int = 10000

    def sense(self):
        pass
