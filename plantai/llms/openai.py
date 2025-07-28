from langchain_openai.chat_models import ChatOpenAI

QWEN3 = "qwen3:32b"
_DEFAULT_MODEL_NAME = QWEN3


def get_llm(model: str = _DEFAULT_MODEL_NAME, **kwargs) -> ChatOpenAI:
    llm = ChatOpenAI(model=model, **kwargs)
    return llm


def get_local_llm(
    model=_DEFAULT_MODEL_NAME,
    base_url: str = "http://localhost:11434/v1",
    **kwargs,
) -> ChatOpenAI:
    llm = get_llm(
        model=model,
        **{"base_url": kwargs.pop("base_url", base_url), **kwargs},
    )

    return llm
