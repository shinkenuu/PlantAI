from langchain_openai.chat_models import ChatOpenAI


FUNCTIONARY = "meetkai/functionary-small-v3.2"
HERMES3 = "./dist/Hermes-3-Llama-3.1-8B-q4f16_1-MLC"
_DEFAULT_MODEL_NAME = HERMES3


def get_llm(model: str = _DEFAULT_MODEL_NAME, **kwargs) -> ChatOpenAI:
    llm = ChatOpenAI(model=model, **kwargs)
    return llm
