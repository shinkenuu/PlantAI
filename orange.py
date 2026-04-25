import logging

from langchain_core.messages import HumanMessage

from config import settings
from plantai.llms import get_ollama_llm
from plantai.agents import demeter

logging.basicConfig(level=logging.INFO)


def main() -> None:
    llm = get_ollama_llm(
        base_url=settings.ollama_base_url,
        temperature=0,
    )
    state = {"messages": [HumanMessage("How is Violet doing today?")]}
    demeter.talk(thread_id="test", llm=llm, state=state)


if __name__ == "__main__":
    main()
