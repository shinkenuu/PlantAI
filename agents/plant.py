class Plant:
    id: str
    name: str = "Green"
    nickname: str = "Albino"
    species: str = "haworthia fasciata"

    traits: str = "Green is a cactus that looks like a tiny peak of pinecone forest at the low of winter"

    # Comes from sensor

    # Typical Range: 0% (completely dry) to 100% (completely saturated with moisture).
    # Vary widely depending on the climate and location.
    _air_humidity: float

    # Typical Range: -40°C to 50°C (-40°F to 122°F).
    # This range covers most terrestrial environments
    _air_temperature: float

    # Typical Range: 0% (completely dry) to 100% (saturated soil).
    # Vary significantly based on soil type, location, and recent precipitation.
    _soil_humidity: float

    # Typical Range: 0 (highly acidic) to 14 (highly alkaline).
    # Most plants thrive in a pH range of 5.5 to 7
    _soil_ph: float

    _light_level: int
