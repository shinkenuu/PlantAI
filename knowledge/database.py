import logging

import pymongo

from knowledge.schemas import PictureThisAIPlantWiki, PerenualSpeciesGuide
from config import DODDER_DATABASE_URI


class DodderDatabase:
    def __init__(self, uri: str = DODDER_DATABASE_URI):
        self._client = pymongo.MongoClient(uri)
        self.picturethisai = self._client["picturethisai"]
        self.penerual = self._client["perenual"]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._client:
            self._client.close()

    def get_picturethisai_plant_wiki(
        self, scientific_name: str
    ) -> PictureThisAIPlantWiki | None:
        logging.info(
            "Querying DodderDB for PictureThisAI plant wiki '%s'", scientific_name
        )
        plant_wiki_document = self.picturethisai.plant_wikis.find_one(
            {"scientific_name": scientific_name}
        )

        if plant_wiki_document:
            logging.info("Found PictureThisAI plant wiki for '%s'", scientific_name)
            return PictureThisAIPlantWiki.model_validate(
                plant_wiki_document, by_alias=True
            )

        logging.warning("No PictureThisAI plant wiki found for '%s'", scientific_name)
        return None

    def get_perenual_species_guides(
        self, scientific_name: str
    ) -> PerenualSpeciesGuide | None:
        logging.info(
            "Querying DodderDB for Perenual species guide '%s'", scientific_name
        )
        species_guide_document = self.penerual.species_guides.find_one(
            {"scientific_name": scientific_name}
        )

        if species_guide_document:
            logging.info("Found Perenual species guide for '%s'", scientific_name)
            return PerenualSpeciesGuide.model_validate(species_guide_document)

        logging.warning("No Perenual species guide found for '%s'", scientific_name)
        return None
