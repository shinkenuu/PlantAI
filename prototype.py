import logging

from langchain_core.messages import HumanMessage

from plantai.llms import (
    # get_openai_llm,
    get_ollama_llm,
)
from plantai.agents import run_carie

logging.basicConfig(level=logging.INFO)

carie_state = {"messages": [HumanMessage("How is Violet doing today?")]}


# llm = get_openai_llm(
#     base_url="http://192.168.1.201:8080/v1",
#     openai_api_key="sk-whatever",
# )
llm = get_ollama_llm()


run_carie(thread_id="test", llm=llm, state=carie_state)
