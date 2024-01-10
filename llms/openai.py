from langchain.chat_models import ChatOpenAI

_llm: ChatOpenAI = None


def get_llm(model="gpt-3.5-turbo", temperature=0, **kwargs):
    global _llm

    if _llm:
        return _llm

    _llm = ChatOpenAI(
        model=model,
        temperature=temperature,
        openai_api_key="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",
        **kwargs
    )
    return _llm
