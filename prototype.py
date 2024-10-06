from langchain_core.messages import HumanMessage


from plantai.llms import (
    get_openai_llm,
    # get_ollama_llm,
)
from plantai.agents import run_carie


carie_state = {"messages": [HumanMessage("How is Violet doing today?")]}


openai_llm = get_openai_llm(
    base_url="http://192.168.1.201:8080/v1", openai_api_key="sk-whatever"
)
# ollama_llm = get_ollama_llm()


run_carie(thread_id="test", llm=openai_llm, state=carie_state)
