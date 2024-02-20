import logging

from langchain_core.tools import tool


@tool
def summarize_activity(query: str, n: int = 5) -> str:
    """Lists your top N latest activities"""
    logging.info(f"SUMMARIZE_ACTIVITY({query}, {n})")

    activities = [
        "I got bored",
        "I got lazy",
        "I got sad",
        "I got inspired",
        "I got unmotivated",
    ]
    return activities[-1] + " lately"


# TODO This is not a tool
@tool
def personalize(query: str, agent_name: str = "Vincent") -> str:
    """Mimics your character's feelings, emotions, judgments and opnions"""
    logging.info(f"personalize(query={query}, agent_name={agent_name})")

    agent_description = "assertive, pragmatic, kind and sharp-minded"

    return f"""{agent_name} is {agent_description}. What are {agent_name} thoughts about '{query}'?"""
