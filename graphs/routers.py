from langchain_core.messages import HumanMessage

from graphs.states import AgentState
from llms.remote import get_llm


def nop(state: AgentState):
    pass


def query_router(state: AgentState):
    """Define which plant the query is best handled by"""
    last_message = state["messages"][-1]

    message = HumanMessage(
        content=f"""You are an efficient manager.
Your task is to decide which team member can best handle the user query.
Output ONLY the selected team member name and nothing else, your life depends on it.

===
Team members

Eddie: General assistant
Progmancer: Progressive rock expert

===
User query

{last_message}
"""
    )

    llm = get_llm()
    ai_message = llm.invoke([message])

    team_member_name = ai_message.content.replace(".", "").strip().lower()
    return team_member_name
