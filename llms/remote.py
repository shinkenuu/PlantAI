from langchain_openai.chat_models import ChatOpenAI


_llm: ChatOpenAI = None


def get_llm(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    openai_api_base="http://localhost:8000/v1",
    openai_api_key="wtv",
    **kwargs
):
    global _llm

    if _llm:
        return _llm

    _llm = ChatOpenAI(
        model_name=model,
        openai_api_key=openai_api_key,
        openai_api_base=openai_api_base,
        **kwargs
    )

    return _llm
