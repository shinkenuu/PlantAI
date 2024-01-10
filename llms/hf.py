import torch
from transformers import pipeline

from langchain.llms.huggingface_pipeline import HuggingFacePipeline


_hf = None


def get_llm(model="HuggingFaceH4/zephyr-7b-beta"):
    global _hf

    if _hf:
        return _hf

    pipe = pipeline(
        "text-generation", model=model, torch_dtype=torch.bfloat16, device_map="auto"
    )

    _hf = HuggingFacePipeline(pipeline=pipe)
    return _hf


def format_prompt(system: str, user: str) -> str:
    prompt = f"""<s>[INST] <<SYS>>
{ system }
<</SYS>>

{ user } [/INST]
"""

    #     prompt = f"""<<SYS>>{system}<</SYS>>
    # [INST] {instruction} [/INST] User: {user}"""

    return prompt
