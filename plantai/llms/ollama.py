from langchain_ollama.chat_models import ChatOllama


HERMES3 = "hermes3"
_DEFAULT_MODEL_NAME = HERMES3


def get_llm(model: str = _DEFAULT_MODEL_NAME, **kwargs) -> ChatOllama:
    llm = ChatOllama(model=model, **kwargs)
    return llm
