from enum import StrEnum

from langchain_core.tools import tool

from knowledge.database import DodderDatabase
from knowledge.schemas import PictureThisAIPlantWiki, PerenualSpeciesGuide


class GuideType(StrEnum):
    WATER = "water"
    SUNLIGHT = "sunlight"
    FERTILIZE = "fertilize"
    PRUNING = "pruning"
    PROPAGATION = "propagation"
    REPOTTING = "repotting"


@tool
def get_watering_guide(
    scientific_name: str,
) -> str:
    """Provides guidance on when and how much watering plants need"""
    plant_wiki, species_guide = _get_plant_documents(scientific_name)

    plant_wiki_guide = plant_wiki.care_guides.water if plant_wiki else None
    species_guide = species_guide.watering if species_guide else None

    return _format_care_guides(plant_wiki_guide, species_guide, GuideType.WATER)


@tool
def get_sunlight_guide(
    scientific_name: str,
) -> str:
    """Provides guidance on how much sunlight is best for plants"""
    plant_wiki, species_guide = _get_plant_documents(scientific_name)

    plant_wiki_guide = plant_wiki.key_facts.sunlight if plant_wiki else None
    species_guide = species_guide.sunlight if species_guide else None

    return _format_care_guides(plant_wiki_guide, species_guide, GuideType.SUNLIGHT)


@tool
def get_fertilizing_guide(
    scientific_name: str,
) -> str:
    """Provides guidance on how and when to fertilize plants"""
    plant_wiki, _ = _get_plant_documents(scientific_name)

    plant_wiki_guide = plant_wiki.care_guides.fertilize if plant_wiki else None

    return _format_care_guides(plant_wiki_guide, None, GuideType.FERTILIZE)


@tool
def get_pruning_guide(
    scientific_name: str,
) -> str:
    """Provides guidance on when and how to prune plants"""
    plant_wiki, species_guide = _get_plant_documents(scientific_name)

    plant_wiki_guide = plant_wiki.care_guides.pruning if plant_wiki else None
    species_guide = species_guide.pruning if species_guide else None

    return _format_care_guides(plant_wiki_guide, species_guide, GuideType.PRUNING)


@tool
def get_propagation_guide(
    scientific_name: str,
) -> str:
    """Provides guidance on propagating plants"""
    plant_wiki, _ = _get_plant_documents(scientific_name)

    plant_wiki_guide = plant_wiki.care_guides.propagation if plant_wiki else None

    return _format_care_guides(plant_wiki_guide, None, GuideType.PROPAGATION)


def _get_plant_documents(
    scientific_name: str,
) -> tuple[PictureThisAIPlantWiki | None, PerenualSpeciesGuide | None]:
    with DodderDatabase() as db:
        plant_wiki = db.get_picturethisai_plant_wiki(scientific_name)
        species_guide = db.get_perenual_species_guides(scientific_name)

    return plant_wiki, species_guide


def _format_care_guides(guide_1: str, guide_2: str, guide_type: GuideType) -> str:
    if guide_1 and guide_2:
        return (
            f"<{guide_type.value}_guide_source_a>{guide_1}</{guide_type.value}_guide_source_a>\n"
            f"<{guide_type.value}_guide_source_b>{guide_2}</{guide_type.value}_guide_source_b>"
        )

    elif guide_1:
        return f"<{guide_type.value}_guide>{guide_1}</{guide_type.value}_guide>"

    elif guide_2:
        return f"<{guide_type.value}_guide>{guide_2}</{guide_type.value}_guide>"

    else:
        return f"<{guide_type.value}_guide>No {guide_type.value} guide available</{guide_type.value}_guide>"
