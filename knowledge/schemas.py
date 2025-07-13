from pydantic import BaseModel, Field

# PictureThisAI


class PlantWikiKeyFacts(BaseModel):
    toxicity: str | None
    lifespan: str | None
    plant_type: str | None
    bloom_time: str | None
    harvest_time: str | None
    plant_height: str | None
    spread: str | None
    leaf_color: str | None
    flower_size: str | None
    fruit_color: str | None
    flower_color: str | None
    stem_color: str | None
    dormancy: str | None
    leaf_type: str | None
    ideal_temperature: str | None
    growth_season: str | None
    growth_rate: str | None
    water: str | None
    sunlight: str | None


class PlantWikiCareGuides(BaseModel):
    water: str | None
    fertilize: str | None
    pruning: str | None
    propagation: str | None
    repotting: str | None


class PictureThisAIPlantWiki(BaseModel):
    id: dict[str, str] = Field(alias="_id")
    url: str
    scrapped_at: str
    scientific_name: str
    display_name: str
    common_names: list[str]
    introduction: str
    key_facts: PlantWikiKeyFacts
    care_guides: PlantWikiCareGuides
    identification_points: list[str]


# Perenual


class PerenualSpeciesGuide(BaseModel):
    id: str = Field(alias="_id")
    url: str
    scrapped_at: str
    common_name: str
    scientific_name: str
    summary: dict
    watering: str
    sunlight: str
    pruning: str
