from langchain.llms import Ollama

llm: Ollama = None


def get_llm(model: str = "zephyr") -> Ollama:
    global _llm

    if not _llm:
        _llm = Ollama(model=model)

    return _llm

