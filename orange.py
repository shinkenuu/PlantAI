import logging

from langchain_core.messages import HumanMessage

from config import OLLAMA_BASE_URL
from plantai.llms import (
    get_ollama_llm,
)
from plantai.agents import run_carie


logging.basicConfig(level=logging.INFO)

carie_state = {"messages": [HumanMessage("How is Iduna doing today?")]}


llm = get_ollama_llm(
    base_url=OLLAMA_BASE_URL,
    temperature=0,
)


run_carie(thread_id="test", llm=llm, state=carie_state)