from pydantic import BaseModel

# PictureThisAI


class PlantWikiKeyFacts(BaseModel):
    toxicity: str | None = None
    lifespan: str | None = None
    plant_type: str | None = None
    bloom_time: str | None = None
    harvest_time: str | None = None
    plant_height: str | None = None
    spread: str | None = None
    leaf_color: str | None = None
    flower_size: str | None = None
    fruit_color: str | None = None
    flower_color: str | None = None
    stem_color: str | None = None
    dormancy: str | None = None
    leaf_type: str | None = None
    ideal_temperature: str | None = None
    growth_season: str | None = None
    growth_rate: str | None = None
    water: str | None = None
    sunlight: str | None = None

    class Config:
        extra = "ignore"


class PlantWikiCareGuides(BaseModel):
    water: str | None = None
    fertilize: str | None = None
    pruning: str | None = None
    propagation: str | None = None
    repotting: str | None = None

    class Config:
        extra = "ignore"


class PictureThisAIPlantWiki(BaseModel):
    # id: str = Field(alias="_id")
    url: str
    scrapped_at: str
    scientific_name: str
    display_name: str
    common_names: list[str]
    introduction: str
    key_facts: PlantWikiKeyFacts
    care_guides: PlantWikiCareGuides
    identification_points: list[str]

    class Config:
        extra = "ignore"


# Perenual


class PerenualSpeciesGuide(BaseModel):
    # id: str = Field(alias="_id")
    url: str
    scrapped_at: str
    common_name: str
    scientific_name: str
    summary: dict
    watering: str
    sunlight: str
    pruning: str

    class Config:
        extra = "ignore"
