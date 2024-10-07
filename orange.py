import logging

from langchain_core.messages import HumanMessage

from config import OPENAI_BASE_URL
from plantai.llms import (
    get_openai_llm,
)
from plantai.agents import run_carie


logging.basicConfig(level=logging.INFO)

carie_state = {"messages": [HumanMessage("How is Iduna doing today?")]}


llm = get_openai_llm(
    base_url=OPENAI_BASE_URL,
    openai_api_key="sk-whatever",
    temperature=0,
)


run_carie(thread_id="test", llm=llm, state=carie_state)