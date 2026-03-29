import logging

from langchain_core.messages import HumanMessage

from config import OLLAMA_BASE_URL
from plantai.llms import (
    get_ollama_llm,
)
from plantai.agents import demeter


logging.basicConfig(level=logging.INFO)

carie_state = {"messages": [HumanMessage("How is Violet doing today?")]}


llm = get_ollama_llm(
    base_url=OLLAMA_BASE_URL,
    temperature=0,
)


demeter.talk(thread_id="test", llm=llm, state=carie_state)
