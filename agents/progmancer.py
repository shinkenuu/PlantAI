import logging

from langchain_core.tools import tool


@tool
def prog_rock_search(query: str) -> str:
    """vast and complete knowledge-base about progressive rock"""
    logging.info("Prog Rock Search | query: %s", query)
    return "Genesis is great"
