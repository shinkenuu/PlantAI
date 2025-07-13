from langchain_ollama.chat_models import ChatOllama


QWEN3 = "qwen3:32b"
_DEFAULT_MODEL_NAME = QWEN3


def get_llm(model: str = _DEFAULT_MODEL_NAME, **kwargs) -> ChatOllama:
    llm = ChatOllama(model=model, **kwargs)
    return llm
