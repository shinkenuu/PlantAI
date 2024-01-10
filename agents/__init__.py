from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad.openai_functions import (
    format_to_openai_functions,
)
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools.convert_to_openai import format_tool_to_openai_function
from langchain.schema.messages import HumanMessage, AIMessage


# from.llms.ollama import get_llm
from llms.openai import get_llm
from agents.tools import TOOLS


def create_agent_executor(
    system_message: str = "You are a very powerful assistant", tools=TOOLS
):
    llm = get_llm()
    llm_with_tools = llm.bind(
        functions=[format_tool_to_openai_function(t) for t in tools]
    )

    MEMORY_KEY = "chat_history"
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_message,
            ),
            MessagesPlaceholder(variable_name=MEMORY_KEY),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_functions(
                x["intermediate_steps"]
            ),
            "chat_history": lambda x: x[MEMORY_KEY],
        }
        | prompt
        | llm_with_tools
        | OpenAIFunctionsAgentOutputParser()
    )

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor


def execute_agent_with_memory(
    input: str,
    agent_executor: AgentExecutor,
    chat_history: list[HumanMessage | AIMessage] = None,
):
    chat_history = chat_history or []
    result = agent_executor.invoke({"input": input, "chat_history": chat_history[-10:]})

    chat_history.extend(
        [
            HumanMessage(content=input),
            AIMessage(content=result["output"]),
        ]
    )

    return result
