import logging

from langchain.agents import tool


@tool
def prog_rock_search(query: str) -> str:
    """useful when answering about progressive rock topics"""
    logging.info("Prog Rock Search | query: %s", query)
    return "Genesis is great"


@tool
def read_news(query: str) -> list[str]:
    """Read online personaly relevant news"""
    print(f"READ_NEWS({query})")

    return [
        "Armageddon countdown is set tonight!",
        "President is about to sell the White House",
    ]


@tool
def summarize_activity(query: str, n: int = 5) -> str:
    """Lists your top N latest activities"""
    print(f"SUMMARIZE_ACTIVITY({query}, {n})")

    activities = [
        "I got bored",
        "I got lazy",
        "I got sad",
        "I got inspired",
        "I got unmotivated",
    ]
    return activities[-1] + " lately"


@tool
def sense() -> str:
    """How are you feeling your sensor signals"""
    print(f"SENSE()")

    return """
    Air temperature: 25C
    Air Humidity: 20%
    Soil moisture: 44%
    Light level: 82%
    """


@tool
def personalize(query: str, agent_name: str = "Vincent") -> str:
    """Mimics your character's feelings, emotions, judgments and opnions"""
    print(f"ANALYSE({query})")

    agent_description = "assertive, pragmatic, kind and sharp-minded"

    return f"""{agent_name} is {agent_description}. How this character would respond to '{query}'?"""


@tool
def search_online(query: str) -> str:
    """Search online for updated information"""
    print(f"SEARCH_ONLINE({query})")

    return "Based on YukDukPaul we're screwed :D"


TOOLS = [prog_rock_search, read_news, summarize_activity, sense, search_online]
