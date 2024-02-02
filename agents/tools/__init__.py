from typing import Annotated
import logging

from langchain_core.tools import tool

from . import plant, persona, progmancer


@tool
def read_news(query: Annotated[str, "query to select news"]) -> list[str]:
    """Read online personaly relevant news"""
    logging.info(f"READ_NEWS({query})")

    return [
        "Armageddon countdown is set tonight!",
        "President is about to sell the White House",
    ]


@tool
def search_online(query: str) -> str:
    """Search online for reliable and updated information"""
    logging.info(f"SEARCH_ONLINE({query})")

    return "Based on YukDukPal we're screwed :D"


TOOLS = [
    read_news,
    search_online,
    progmancer.prog_rock_search,
    persona.summarize_activity,
    plant.sense,
]
