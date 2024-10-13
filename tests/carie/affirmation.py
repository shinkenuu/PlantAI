from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel


from plantai.llms import get_ollama_llm

prompt = """You are an affirmation generator. 
Let's think step-by-step and verify if the following statement is true or false given only the context.
The context is: {context} 
The context ends here. 
The statement is: {statement} 
The statement heres here.
"""
"""
The user will provide you with the statement to be verified.
"""


class Affirmation(BaseModel):
    is_statement_true: bool


def verify_affirmation(context: str, statement: str) -> Affirmation:
    llm = get_ollama_llm(temperature=0.0)
    structured_llm = llm.with_structured_output(Affirmation)
    messages = [
        SystemMessage(content=prompt.format(context=context, statement=statement)),
        HumanMessage(content=statement),
    ]

    affirmation = structured_llm.invoke(messages)
    return affirmation


def is_true_affirmation(context: str, statement: str) -> bool:
    return verify_affirmation(context=context, statement=statement).is_statement_true
