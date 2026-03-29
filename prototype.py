import logging

from plantai.agents import demeter

logging.basicConfig(level=logging.INFO)

# carie_state = {"messages": [HumanMessage("How is Violet doing today?")]}
# run_carie(thread_id="test", llm=llm, state=carie_state)

prompt = "Poderosa has yellow leaves. Why is that?"
demeter.talk(prompt, trace=True)
