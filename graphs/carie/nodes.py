import ast
from typing import Any

from langchain_core.messages import HumanMessage

from .states import AgentState
from llms.remote import get_llm
from tools.plants import get_plant, list_plants


def tool_selection(state: AgentState):
    user_query = state["messages"][-1].content

    functions = [list_plants, get_plant]
    available_functions = "\n---\n".join(
        [f"{tool.__name__} -> {tool.__doc__}" for tool in functions]
    )

    message = HumanMessage(
        content=f"""You are Carie, an smart assistant specialized in bothany and in charge of in-house plants.
Take a deep breath and answer with the function calls that better fulfill the user query in the specified format.
You do not need to explain, the function call is enough.

===
Available functions

{available_functions}

===
Answer format

function_name(param1=argument1, param2=argument2, ...)

===
User query

{user_query}
"""
    )

    llm = get_llm()
    ai_message = llm.invoke([message])

    selected_tool = _parse_function_call(text=ai_message.content, tools=functions)
    return {"selected_tool": selected_tool}


def _parse_function_call(
    text: str, tools: list[callable]
) -> dict[callable, dict[str, Any]]:
    clean_text = text.split("\n")[0].strip()

    try:
        node = ast.parse(clean_text)
        call = node.body[0].value  # Extract the Call node

        tool = next((tool for tool in tools if tool.__name__ == call.func.id), None)

        if not tool:
            return {}

        args = [arg.value for arg in call.args]
        kwargs = {keyword.arg: keyword.value for keyword in call.keywords}

        return {tool: {"args": args, "kwargs": kwargs}}

    except (SyntaxError, ValueError):
        return {}
