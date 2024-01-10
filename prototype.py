from langchain.agents import AgentExecutor, XMLAgent

from llms.hf import get_llm
from agents.tools import TOOLS

prompt = XMLAgent.get_default_prompt()

llm = get_llm()


def convert_intermediate_steps(intermediate_steps):
    log = ""

    for action, observation in intermediate_steps:
        log += (
            f"<tool>{action.tool}</tool><tool_input>{action.tool_input}"
            f"</tool_input><observation>{observation}</observation>"
        )

    return log


agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: convert_intermediate_steps(
            x["intermediate_steps"]
        ),
    }
    | prompt
    | llm.bind(stop=["</tool_input>", "</final_answer>"])
    | XMLAgent.get_default_output_parser()
)


agent_executor = AgentExecutor(agent=agent, tools=TOOLS, verbose=True)


agent_executor.invoke(
    {
        "input": "Can you tell me how much experience is neeed to go from level 1 to level 99 in any RuneScape skill?"
    }
)
