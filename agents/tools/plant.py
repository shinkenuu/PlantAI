import logging

from langchain_core.tools import tool


@tool
def sense() -> str:
    """How are you feeling your sensor signals"""
    logging.info(f"SENSE()")

    return """
    Air temperature: 25C
    Air Humidity: 20%
    Soil moisture: 44%
    Light level: 82%
    """
