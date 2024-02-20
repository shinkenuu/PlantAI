from langchain_core.messages import AIMessage

from graphs.states import AgentState
from llms.vllm import get_llm

def eddie(state: AgentState):
    last_message = state['messages'][-1]

    llm = get_llm()
    ai_message = llm.invoke([last_message])

    return {"messages": [ai_message]}


def progmancer(state: AgentState):
    return {"messages": [AIMessage(content="Its 1 o'clock and time for lunch")]}
