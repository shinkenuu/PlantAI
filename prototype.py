import logging


from plantai.agents import demeter

logging.basicConfig(level=logging.INFO)

# carie_state = {"messages": [HumanMessage("How is Violet doing today?")]}


# llm = get_openai_llm(
#     base_url="http://192.168.1.201:8080/v1",
#     openai_api_key="sk-whatever",
# )
# llm = get_ollama_llm()


# run_carie(thread_id="test", llm=llm, state=carie_state)

demeter.talk("What is the best place for Lillian to be?", trace=True)
