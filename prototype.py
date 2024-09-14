from langchain_core.messages import HumanMessage


from plantai.agents import run_carie


carie_state = {"messages": [HumanMessage("How is Violet doint today?")]}


run_carie(thread_id="test", state=carie_state)
