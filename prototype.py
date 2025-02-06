import logging

from plantai.agents import demeter

logging.basicConfig(level=logging.INFO)

# carie_state = {"messages": [HumanMessage("How is Violet doing today?")]}
# run_carie(thread_id="test", llm=llm, state=carie_state)

demeter.talk("What is the best place for Lillian to be?", trace=True)
