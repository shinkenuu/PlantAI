from langchain_openai.chat_models import ChatOpenAI

QWEN3 = "qwen3:32b"
_DEFAULT_MODEL_NAME = QWEN3


def get_llm(model: str = _DEFAULT_MODEL_NAME, **kwargs) -> ChatOpenAI:
    llm = ChatOpenAI(model=model, **kwargs)
    return llm
